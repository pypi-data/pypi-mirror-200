# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['myctypes']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'myctypes',
    'version': '0.1.0',
    'description': 'Attempts to make a slightly nicer interface to ctypes',
    'long_description': None,
    'author': 'Zachary Farquharson',
    'author_email': 'PercyJackson235@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
