# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_docx']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.88.0']

setup_kwargs = {
    'name': 'fastapi-docx',
    'version': '0.1.9',
    'description': 'Extend a FastAPI OpenAPI spec to include all possible HTTPException or custom Exception response schemas.',
    'long_description': '# fastapi-docx\n\n<p align="center">\n  <a href="https://github.com/Saran33/fastapi-docx"><img src="https://saran33.github.io/fastapi-docx/img/fastapi-docx-logo-teal.png" alt="FastAPI"></a>\n</p>\n<p align="center">\n    <em>Add HTTPException responses to a FastAPI OpenAPI spec</em>\n</p>\n<p align="center">\n<a href="https://github.com/saran33/fastapi-docx/actions?query=workflow%3ACI+event%3Apush+branch%3Amain" target="_blank">\n    <img src="https://github.com/saran33/fastapi-docx/workflows/CI/badge.svg?event=push&branch=main" alt="CI">\n</a>\n<a href="https://saran33.github.io/fastapi-docx/coverage/coverage.html" target="_blank">\n    <img src="https://saran33.github.io/fastapi-docx/coverage/coverage-badge.svg" alt="Coverage">\n</a>\n<a href="https://pypi.org/project/fastapi-docx" target="_blank">\n    <img src="https://img.shields.io/pypi/v/fastapi-docx?color=%2334D058&label=pypi%20package" alt="Package version">\n</a>\n<a href="https://pypi.org/project/fastapi-docx" target="_blank">\n    <img src="https://img.shields.io/pypi/pyversions/fastapi-docx" alt="Supported Python versions">\n</a>\n</p>\n\n---\n\n**Documentation**: <a href="https://saran33.github.io/fastapi-docx" target="_blank">https://saran33.github.io/fastapi-docx</a>\n\n**Source Code**: <a href="https://github.com/Saran33/fastapi-docx" target="_blank">https://github.com/Saran33/fastapi-docx</a>\n\n---\n\nFastAPI-docx extends the FastAPI OpenAPI spec to include all possible `HTTPException` or custom Exception response schemas that may be raised within path operations.\n\nThe key features are:\n\n* **Document Exception Responses**: Automatically find all possible respones within path operations, whether they originate from a `HTTPException` raised by the endpoint function directly, in a nested function, class method, or callable class instance, or by the fastAPI dependency-injection system.\n* **Include Custom Exceptions**: Optionally find and document any custom Exception types if using custom Exception handlers in your FastAPI application.\n* **Generate Exception schemas**: A default `HTTPExceptionSchema` will be added to the OpenAPI specification. The default can be modified to use any other [Pydantic](*https://github.com/pydantic/pydantic) model. An additional schema for app-specific custom Exceptions can also be included.\n\n##### License\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'Saran Connolly',
    'author_email': 'saran@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Saran33/fastapi-docx',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0.0',
}


setup(**setup_kwargs)
