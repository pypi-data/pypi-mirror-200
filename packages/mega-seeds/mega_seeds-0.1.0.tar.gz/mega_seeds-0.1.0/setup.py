# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mega_seeds']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=23.1.0,<24.0.0',
 'anyio>=3.6.2,<4.0.0',
 'asyncclick>=8.1.3.4,<9.0.0.0',
 'asyncpg>=0.27.0,<0.28.0',
 'databases>=0.7.0,<0.8.0',
 'loguru>=0.6.0,<0.7.0',
 'mako>=1.2.4,<2.0.0',
 'shortuuid>=1.0.11,<2.0.0']

entry_points = \
{'console_scripts': ['seeds = seeds.cli:seeds']}

setup_kwargs = {
    'name': 'mega-seeds',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Dimash',
    'author_email': 'digisinov@megacom.kg',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
