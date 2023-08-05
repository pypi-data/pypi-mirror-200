# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['unknowncode']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'unknowncode',
    'version': '0.1.0',
    'description': 'Small portions of code I use, gathered into one group for ease of access. Like a mod library for a game. Built with poetry',
    'long_description': None,
    'author': 'UnknownSources',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
