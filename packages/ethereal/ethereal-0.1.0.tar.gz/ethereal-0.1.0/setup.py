# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ethereal']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ethereal',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Alex Euler',
    'author_email': '0xalexeuler@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
