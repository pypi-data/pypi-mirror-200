import asyncio
import json
import logging
import os
import signal
import time
from datetime import datetime
from enum import Enum
from functools import wraps
from inspect import signature
from typing import Callable, List, Optional, Union

import httpx
from confluent_kafka import KafkaException
from confluent_kafka import Message as ConfluentMessage
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError

from .agent import Agent, KafkaEvent
from .kafka_adapter import KafkaAdapter, KafkaConfig, KafkaRole
from .topic import Topic, TopicDir
from .utils import CitizenKError

logger = logging.getLogger(__name__)


class AppType(Enum):
    SOURCE = 1
    SINK = 2
    TRANSFORM = 3


class CitizenK(FastAPI):
    def __init__(
        self,
        kafka_config: KafkaConfig,
        app_name: str,
        app_type: AppType = AppType.SOURCE,
        consumer_group_init_offset: str = "latest",
        schema_registry_url: Optional[str] = None,
        auto_generate_apis: bool = True,
        max_processing_cycle_ms: int = 5 * 1000,
        api_router_prefix: str = "",
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.app_name = app_name
        self.app_type = app_type
        self.kafka_config = kafka_config
        self.consumer_group_init_offset = consumer_group_init_offset
        self.schema_registry_url = schema_registry_url
        self.auto_generate_apis = auto_generate_apis
        self.max_processing_cycle_ms = max_processing_cycle_ms
        self.api_router_prefix = api_router_prefix
        self.producer = None
        self.consumer = None
        self.started = datetime.utcnow()

        self.total_batch_size = 0
        self.consumer_topics = set()
        self.topics = {}
        self.agents = {}
        self.main_consumer_loop_task = None
        self.monitor_loop_task = None

        self.add_event_handler("startup", self.startup)
        self.add_event_handler("shutdown", self.shutdown)
        if auto_generate_apis:
            self._generate_apis()

    def _generate_apis(self):
        @self.get(
            f"{self.api_router_prefix}/stats/producer", response_class=JSONResponse
        )
        def get_producer_stats():
            """Get the producer stats"""
            if self.producer is not None:
                return self.producer.last_stats
            return {}

        @self.get(
            f"{self.api_router_prefix}/stats/consumer", response_class=JSONResponse
        )
        def get_consumer_stats():
            """Get the producer stats"""
            if self.consumer is not None:
                return self.consumer.last_stats
            return {}

        @self.get(f"{self.api_router_prefix}/info", response_class=JSONResponse)
        def get_service_info():
            """Get the service info"""
            hosts = {}
            assignments = {}
            lag = {}
            if self.consumer is not None:
                hosts = self.consumer.get_group_members()
                assignments = self.consumer.assigned_partitions
                lag = self.consumer.get_group_lag()
            return {
                "started": self.started,
                "app": {
                    "name": self.app_name,
                    "title": self.title,
                    "description": self.description,
                    "version": self.version,
                },
                "topics": {
                    "in": [
                        t.name
                        for t in self.topics.values()
                        if t.topic_dir != TopicDir.OUTPUT
                    ],
                    "out": [
                        t.name
                        for t in self.topics.values()
                        if t.topic_dir != TopicDir.INPUT
                    ],
                },
                "lag": lag,
                "assignments": assignments,
                "agents": {a.name: a.cycles for a in self.agents.values()},
                "hosts": {f"{tp[0]}-{tp[1]}": h for tp, h in hosts.items()},
            }

    def is_sink(self) -> bool:
        return self.app_type == AppType.SINK

    def fast_status(self) -> bool:
        """Return the status without actively checking Kafka connectivity"""
        if self.consumer is not None:
            if self.consumer.kafka_error is not None:
                return False

        if self.producer is not None:
            if self.producer.kafka_error is not None:
                return False

        return True

    def status(self) -> bool:
        """Return the status, plus actively checking Kafka connectivity"""
        if self.consumer is not None:
            if self.consumer.kafka_error is not None:
                return False
            # Use list topics to see if the broker is still up
            try:
                self.consumer.get_all_broker_topics()
            except KafkaException:
                logger.error("Failed to get topics from broker")
                return False

        if self.producer is not None:
            if self.producer.kafka_error is not None:
                return False
            # Use list topics to see if the broker is still up
            try:
                self.producer.get_all_broker_topics()
            except KafkaException:
                logger.error("Failed to get topics from broker")
                return False
        return True

    def startup(self):
        """CitizenK startup. Called on FastAPI startup"""
        logger.debug("CitizenK Starting up...")

        # Find all consumer topics
        for agent in self.agents.values():
            self.consumer_topics.update({t.name for t in agent.topics})
            self.total_batch_size += agent.batch_size
            for t in agent.topics:
                if t.topic_dir == TopicDir.OUTPUT:
                    raise CitizenKError("Trying to consume from an output topic")

        # Create consumer
        if len(self.consumer_topics) > 0:
            if self.app_type == AppType.SOURCE:
                raise CitizenKError("Trying to consume topics in a source app")
            self.consumer = KafkaAdapter(
                self.kafka_config,
                KafkaRole.CONSUMER,
                self.app_name,
                self.consumer_group_init_offset,
            )

        # Create producer
        if self.app_type in [AppType.SOURCE, AppType.TRANSFORM]:
            self.producer = KafkaAdapter(self.kafka_config, KafkaRole.PRODUCER)

        # Check that all topic exists in broker
        broker = self.producer if self.consumer is None else self.consumer
        broker_topics = broker.get_all_broker_topics()
        for topic_name in self.topics:
            if topic_name not in broker_topics:
                raise CitizenKError(f"Can't find topic {topic_name} in broker")

        # Start consumer
        if len(self.consumer_topics) > 0:
            self.consumer.start_consumer(list(self.consumer_topics))
            self.main_consumer_loop_task = asyncio.create_task(
                self._main_consumer_loop()
            )
            self.monitor_loop_task = asyncio.create_task(self._monitor_loop())

    def shutdown(self):
        """CitizenK shutdown Called on FastAPI shutown"""
        logger.debug("CitizenK Shutting down...")
        if self.consumer is not None:
            self.consumer.close()
            self.consumer = None
        if self.producer is not None:
            self.producer.close()
            self.producer = None
        if self.main_consumer_loop_task is not None:
            self.main_consumer_loop_task.cancel()

    def validate_messages(self, msgs: List[ConfluentMessage]) -> List[KafkaEvent]:
        """Validate the incoming Kafka messages"""
        events = []
        for msg in msgs:
            topic_name = msg.topic()
            if topic_name not in self.consumer_topics:
                raise CitizenKError(
                    "Weird, got a message from an unexpected topic", topic_name
                )
            topic = self.topics[topic_name]
            try:
                value = topic.value_type(**json.loads(msg.value()))
            except json.decoder.JSONDecodeError as e:
                logger.error("For now, CitizenK only supports JSON values %s", e)
                continue
            except ValidationError as e:
                logger.error("Error while validating received value %s", e.json())
                continue

            events.append(
                KafkaEvent(
                    key=msg.key(),
                    value=value,
                    topic=topic,
                    partition=msg.partition(),
                    offset=msg.offset(),
                    timestamp=msg.timestamp()[1],
                    headers=msg.headers(),
                )
            )
        return events

    async def _monitor_loop(self):
        """Periodic task that checks Kafka status, and kills the process"""
        logger.debug("CitizenK Main monitor loop started...")
        while True:
            await asyncio.sleep(10)
            if not self.status():
                self.shutdown()
                os.kill(os.getpid(), signal.SIGINT)
                await asyncio.sleep(60)
                os.kill(os.getpid(), signal.SIGKILL)

    async def _main_consumer_loop(self):
        """Main Kafka consumer loop which invokes the process agents"""
        logger.debug("CitizenK Main processing loop started...")
        while True:
            if self.consumer is None:
                break
            try:
                msgs = self.consumer.consume(
                    num_messages=self.total_batch_size, timeout=0.1
                )
                if len(msgs) == 0:
                    logger.debug("No kafka events, sleeping")
                    await asyncio.sleep(1)
                else:
                    start_time = time.time()

                    events = self.validate_messages(msgs)
                    for agent in self.agents.values():
                        await agent.process(events)

                    duration = 1000 * (time.time() - start_time)
                    if duration > self.max_processing_cycle_ms:
                        logger.error(
                            "Processing cycle took %s ms > %s",
                            duration,
                            self.max_processing_cycle_ms,
                        )
                    # Just to give other tasks opportunity to run
                    await asyncio.sleep(0)
                if self.app_type == AppType.TRANSFORM:
                    self.producer.poll()
            except Exception as e:
                logger.exception("Exception in main loop: %s", str(e))
                await asyncio.sleep(3)

    def topic(self, name: str, value_type: BaseModel, topic_dir: TopicDir) -> Topic:
        if name in self.topics:
            raise CitizenKError(f"Topic {name} already exists")
        t = Topic(self, name=name, value_type=value_type, topic_dir=topic_dir)
        self.topics[name] = t
        logger.debug("Adding topic %s", name)
        return t

    def agent(
        self,
        topics: Union[Topic, List[Topic]],
        batch_size: int = 1,
        websocket_route: Optional[str] = None,
    ) -> Callable:
        """
        decorates a function of this type:
        async def processing_agent(events: List[KafkaEvent])

        Or this type:
        async def processing_agent(values: List[BaseModel])

        Both of these functions consumes from in_topics and produce to out_topics
        """

        if isinstance(topics, Topic):
            topics = [topics]

        def decorator(f):
            @wraps(f)
            async def wrapper(*args, **kwargs):
                return await f(*args, **kwargs)

            agent_name = f.__name__
            if "values" in signature(f).parameters:
                return_type = "values"
            elif "events" in signature(f).parameters:
                return_type = "events"
            else:
                raise CitizenKError("Agents can only accept values and events")
            self.agents[agent_name] = Agent(
                self, agent_name, f, topics, batch_size, return_type, websocket_route
            )
            logger.debug("Adding agent %s %s", agent_name, topics)
            return wrapper

        return decorator

    def topic_router(self,topic: Topic,match_info: str) -> Callable:
        """
        routes the request to the right worker based on topic, key:
        assumes default partitioner... Used mainly for statefule services where
        Each worker holds some state / key
        """

        def decorator(f):
            @wraps(f)
            async def wrapper(*args, **kwargs):
                if self.consumer is None or self.consumer.consumer_group_name is None:
                    raise CitizenKError(
                        "Topic routing doesn't make sense without a consumer group"
                    )

                if "request" not in kwargs or not isinstance(
                    kwargs["request"], Request
                ):
                    raise CitizenKError(
                        "Topic routing endpoint must include a request object"
                    )

                if match_info is not None and match_info not in kwargs:
                    raise CitizenKError(
                        "Topic routing endpoint must include the match_info key"
                    )

                # Try to convert key to string... to support int as well
                key = str(kwargs[match_info])
                # Get the partition for this key and topic
                if topic.partitioner is not None:
                    partition_id = topic.partitioner(key)
                else:
                    partition_id = self.consumer.get_partition_id(topic.name, key)
                if partition_id is None:
                    raise CitizenKError("Failed to get partition id from key")

                logger.debug(
                    "Partition id for topic %s and key %s is %s",
                    topic.name,
                    key,
                    partition_id,
                )

                # Check if this worker is assigned to this partition
                if topic in self.consumer.assigned_partitions:
                    if partition_id in self.consumer.assigned_partitions[topic]:
                        return await f(*args, **kwargs)

                members = self.consumer.get_group_members()
                host = members.get((topic, partition_id), None)
                if host is None:
                    raise CitizenKError(f"Can't find a host for this request {topic}/{partition_id} {members}")

                # Route the request to the host
                request = kwargs["request"]
                params = dict(request.query_params)
                if "citizenk_stop_propogate" in params:
                    return await f(*args, **kwargs)
                params["citizenk_stop_propogate"] = True

                url = httpx.URL(str(request.url)).copy_with(host=host)
                async with httpx.AsyncClient() as client:
                    r = await client.request(
                        method=request.method,
                        url=url,
                        headers=request.headers.raw,
                        params=params,
                        content=await request.body(),
                        timeout=10.0,
                    )
                    try:
                        return r.json()
                    except  json.JSONDecodeError:
                        return r.text

            return wrapper

        return decorator

    def broadcast_router(self) -> Callable:
        """
        routes the request to the all the workers and aggregate the JSON response
        """

        def decorator(f):
            @wraps(f)
            async def wrapper(*args, **kwargs):
                if self.consumer is None or self.consumer.consumer_group_name is None:
                    raise CitizenKError(
                        "Broadcast routing doesn't make sense without a consumer group"
                    )

                if "request" not in kwargs or not isinstance(
                    kwargs["request"], Request
                ):
                    raise CitizenKError(
                        "Broadcast routing endpoint must include a request object"
                    )

                members = self.consumer.get_group_members()
                hosts = set(members.values())

                # Route the request to the host
                request = kwargs["request"]
                params = dict(request.query_params)
                if "citizenk_stop_propogate" in params:
                    return await f(*args, **kwargs)
                params["citizenk_stop_propogate"] = True

                response = {}
                async with httpx.AsyncClient() as client:
                    for host in hosts:
                        url = httpx.URL(str(request.url)).copy_with(host=host)
                        r = await client.request(
                            method=request.method,
                            url=url,
                            headers=request.headers.raw,
                            params=params,
                            content=await request.body(),
                            timeout=10.0,
                        )
                        response[host] = r.json()
                return response

            return wrapper

        return decorator
