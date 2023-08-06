# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gstargets']

package_data = \
{'': ['*']}

install_requires = \
['packaging>=23.0,<24.0', 'volprofile>=0.1.8,<0.2.0', 'zigzag>=0.3.2,<0.4.0']

setup_kwargs = {
    'name': 'gstargets',
    'version': '0.2.5',
    'description': '',
    'long_description': None,
    'author': 'sajad faghfoor maghrebi',
    'author_email': 'sajad.faghfoor@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
