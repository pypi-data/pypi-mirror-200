from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable, List

from fastapi import WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from .topic import Topic
from .utils import annotate_function

if TYPE_CHECKING:
    from .citizenk import CitizenK

logger = logging.getLogger(__name__)


@dataclass
class KafkaEvent:
    key: str | bytes
    value: BaseModel
    topic: Topic
    partition: int
    offset: int
    timestamp: int
    headers: list[tuple[str, Any]]


class Agent:
    def __init__(
        self,
        app: CitizenK,
        name: str,
        coroutine: Callable,
        topics: list[Topic] | None = None,
        batch_size: int = 1,
        return_type: str = "events",
        websocket_route: str | None = None,
    ):
        self.app = app
        self.name = name
        self.coroutine = coroutine
        self.topics = [] if topics is None else topics
        self.topic_names = [t.name for t in self.topics]
        self.batch_size = batch_size
        self.return_type = return_type
        self.websocket_route = websocket_route
        self.active_websocket_connections: list[WebSocket] = []
        self.cycles = 0
        if self.app.auto_generate_apis:
            self._generate_apis()

        if websocket_route:
            self._add_websocket_route()

    def _add_websocket_route(self):
        @self.app.websocket(self.websocket_route)
        async def w(websocket: WebSocket):
            await websocket.accept()
            self.active_websocket_connections.append(websocket)
            try:
                while True:
                    data = await websocket.receive_text()
                    logger.info("Received data from we socket %s: ignoring", data)
            except WebSocketDisconnect:
                self.active_websocket_connections.remove(websocket)

    def _generate_apis(self):
        for topic in self.topics:

            async def endpoint(values: int):
                result = await self.coroutine(values=values)
                await self.websocket_broadcast_result(result)
                return result

            annotate_function(
                endpoint,
                name=f"send_to_agent_{self.name}_from_{topic.name}",
                doc=f"This endpoint send value to agent {self.name} from topic {topic.name}",
                argument_types={"values": List[topic.value_type]},
            )

            self.app.add_api_route(
                path=f"{self.app.api_router_prefix}/agent/{self.name}/{topic.name}",
                response_class=JSONResponse,
                methods=["POST"],
                endpoint=endpoint,
            )

    async def websocket_broadcast_result(self, result: str):
        if result is None:
            return
        for connection in list(self.active_websocket_connections):
            try:
                await connection.send_text(result)
            except WebSocketDisconnect:
                logger.info("Websocket connection disconnected")
                self.active_websocket_connections.remove(connection)

    async def process(self, events: list[KafkaEvent]):
        filtered = []
        for event in events:
            if event.topic.name in self.topic_names:
                if self.return_type == "events":
                    filtered.append(event)
                else:
                    filtered.append(event.value)
        if len(filtered) > 0:
            self.cycles += 1
            arguments = {self.return_type: filtered}
            result = await self.coroutine(**arguments)
            await self.websocket_broadcast_result(result)

    def __str__(self) -> str:
        return self.name
