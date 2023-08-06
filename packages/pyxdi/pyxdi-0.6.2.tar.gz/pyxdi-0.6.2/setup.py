# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['pyxdi', 'pyxdi.ext', 'pyxdi.ext.starlette']

package_data = \
{'': ['*']}

install_requires = \
['anyio>=3.6.2,<4.0.0']

extras_require = \
{'docs': ['mkdocs>=1.4.2,<2.0.0', 'mkdocs-material>=9.0.12,<10.0.0']}

setup_kwargs = {
    'name': 'pyxdi',
    'version': '0.6.2',
    'description': 'Dependency Injection library',
    'long_description': '# PyxDI (in development)\n\n`PyxDI` is a modern, lightweight and async-friendly Python Dependency Injection library that leverages type annotations ([PEP 484](https://peps.python.org/pep-0484/))\nto effortlessly manage dependencies in your applications.\n\n[![CI](https://github.com/antonrh/pyxdi/actions/workflows/ci.yml/badge.svg)](https://github.com/antonrh/pyxdi/actions/workflows/ci.yml)\n[![codecov](https://codecov.io/gh/antonrh/pyxdi/branch/main/graph/badge.svg?token=67CLD19I0C)](https://codecov.io/gh/antonrh/pyxdi)\n[![Documentation Status](https://readthedocs.org/projects/pyxdi/badge/?version=latest)](https://pyxdi.readthedocs.io/en/latest/?badge=latest)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n---\nDocumentation\n\nhttp://pyxdi.readthedocs.io/\n\n---\n\n## Requirements\n\nPython 3.7+\n\nand requires [anyio](https://github.com/agronholm/anyio)\n\n## Installation\n\nInstall using `pip`:\n\n```shell\npip install pyxdi\n```\n\nor using `poetry`:\n\n```shell\npoetry add pyxdi\n```\n\n## Quick Example\n\n*app.py*\n\n```python\nimport pyxdi\n\ndi = pyxdi.PyxDI()\n\n\n@di.provider\ndef message() -> str:\n    return "Hello, world!"\n\n\n@di.inject\ndef say_hello(message: str = pyxdi.dep) -> None:\n    print(message)\n\n\nif __name__ == "__main__":\n    say_hello()\n```\n\n## TODO\n* Documentation (in progress)\n* Examples (in progress)\n',
    'author': 'Anton Ruhlov',
    'author_email': 'antonruhlov@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/antonrh/pyxdi',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<3.12',
}


setup(**setup_kwargs)
