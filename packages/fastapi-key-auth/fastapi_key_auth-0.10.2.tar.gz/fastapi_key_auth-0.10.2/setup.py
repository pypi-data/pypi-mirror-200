# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_key_auth',
 'fastapi_key_auth.dependency',
 'fastapi_key_auth.middleware']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.84.0', 'starlette>=0.25.0']

setup_kwargs = {
    'name': 'fastapi-key-auth',
    'version': '0.10.2',
    'description': 'API key validation Middleware',
    'long_description': '<br />\n<p align="center">\n  <h3 align="center">FastAPI-key-auth</h3>\n\n  <p align="center">\n    Secure your FastAPI endpoints using API keys.\n    <br />\n    <a href="https://github.com/iwpnd/fastapi-key-auth/issues">Report Bug</a>\n    ·\n    <a href="https://github.com/iwpnd/fastapi-key-auth/issues">Request Feature</a>\n  </p>\n</p>\n\n<!-- TABLE OF CONTENTS -->\n<details open="open">\n  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>\n  <ol>\n    <li>\n      <a href="#about-the-project">About The Project</a>\n      <ul>\n        <li><a href="#built-with">Built With</a></li>\n      </ul>\n    </li>\n    <li>\n      <a href="#getting-started">Getting Started</a>\n      <ul>\n        <li><a href="#installation">Installation</a></li>\n      </ul>\n    </li>\n    <li><a href="#usage">Usage</a></li>\n    <li><a href="#license">License</a></li>\n    <li><a href="#contact">Contact</a></li>\n  </ol>\n</details>\n\n<!-- ABOUT THE PROJECT -->\n\n## About The Project\n\nOn deployment inject API keys authorized to use your service. Every call to a private\nendpoint of your service has to include a `header[\'x-api-key\']` attribute that is\nvalidated against the API keys in your environment.\nIf it is present, a request is authorized. If it is not FastAPI return `401 Unauthorized`.\nUse this either as a middleware, or as Dependency.\n\n### Built With\n\n-   [starlette](https://github.com/encode/starlette)\n-   [fastapi](https://github.com/tiangolo/fastapi)\n\n<!-- GETTING STARTED -->\n\n## Getting Started\n\n### Installation\n\n1. Clone and install\n    ```sh\n    git clone https://github.com/iwpnd/fastapi-key-auth.git\n    poetry install\n    ```\n2. Install with pip\n    ```sh\n    pip install fastapi-key-auth\n    ```\n3. Install with poetry\n    ```sh\n    poetry add fastapi-key-auth\n    ```\n\n## Usage\n\nAs Middleware:\n\n```python\nfrom fastapi import FastAPI\nfrom fastapi_key_auth import AuthorizerMiddleware\n\napp = FastAPI()\n\napp.add_middleware(AuthorizerMiddleware, public_paths=["/ping"], key_pattern="API_KEY_")\n\n# optional use regex startswith\napp.add_middleware(AuthorizerMiddleware, public_paths=["/ping", "^/users"])\n```\n\nAs Dependency\n\n```python\nfrom fastapi import FastAPI, Depends\nfrom fastapi_key_auth import AuthorizerDependency\n\nauthorizer = AuthorizerDependency(key_pattern="API_KEY_")\n\n# either globally or in a router\napp = FastAPI(dependencies=[Depends(authorizer)])\n```\n\n## License\n\nDistributed under the MIT License. See `LICENSE` for more information.\n\n<!-- CONTACT -->\n\n## Contact\n\nBenjamin Ramser - [@imwithpanda](https://twitter.com/imwithpanda) - ahoi@iwpnd.pw  \nProject Link: [https://github.com/iwpnd/fastapi-key-auth](https://github.com/iwpnd/fastapi-key-auth)\n',
    'author': 'Benjamin Ramser',
    'author_email': 'legionaerr@googlemail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/iwpnd/fastapi-key-auth',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
