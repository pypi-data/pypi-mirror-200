# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jetblack_fixengine',
 'jetblack_fixengine.acceptor',
 'jetblack_fixengine.admin',
 'jetblack_fixengine.initiator',
 'jetblack_fixengine.managers',
 'jetblack_fixengine.persistence',
 'jetblack_fixengine.transports',
 'jetblack_fixengine.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=23.1,<24.0',
 'aiosqlite>=0.18.0,<0.19.0',
 'jetblack-fixparser>=2.3,<3.0',
 'pytz>=2022.7,<2023.0',
 'tzlocal>=4.3,<5.0']

setup_kwargs = {
    'name': 'jetblack-fixengine',
    'version': '1.0.0a1',
    'description': 'A pure Python implementation of the FIX protocol',
    'long_description': None,
    'author': 'Rob Blackbourn',
    'author_email': 'rob.blackbourn@googlemail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rob-blackbourn/jetblack-fixengine',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
