# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['citizenk']

package_data = \
{'': ['*']}

install_requires = \
['certifi>=2022.12.7,<2023.0.0',
 'confluent-kafka[schema-registry]>=2.0.2,<3.0.0',
 'fastapi-utils>=0.2.1,<0.3.0',
 'fastapi>=0.92.0,<0.93.0',
 'httpx>=0.23.3,<0.24.0',
 'websockets>=10.4,<11.0']

setup_kwargs = {
    'name': 'citizenk',
    'version': '0.1.21',
    'description': 'An async Kafka Python Framework based on FastAPI and Confluent Kafka',
    'long_description': None,
    'author': 'Valerann',
    'author_email': 'info@valerann.com',
    'maintainer': 'Valerann',
    'maintainer_email': 'info@valerann.com',
    'url': 'https://pypi.org/user/valerann/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
