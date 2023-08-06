# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydlj', 'pydlj.shorteners']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pydlj',
    'version': '0.0.3',
    'description': 'A url shortner',
    'long_description': None,
    'author': 'Tomy',
    'author_email': 'cyaeyz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
