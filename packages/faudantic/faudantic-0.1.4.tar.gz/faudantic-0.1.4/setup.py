# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['faudantic']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.4,<4.0.0',
 'faunadb>=4.5.0,<5.0.0',
 'pydantic[dotenv]>=1.10.7,<2.0.0']

entry_points = \
{'console_scripts': ['pytest = pytest:main']}

setup_kwargs = {
    'name': 'faudantic',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'Oscar Bahamonde',
    'author_email': 'oscar.bahamonde.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
