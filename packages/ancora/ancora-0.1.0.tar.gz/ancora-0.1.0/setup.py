# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ancora']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ancora',
    'version': '0.1.0',
    'description': 'Stellar Anchor implementation using FastAPI',
    'long_description': 'Stellar Anchor implementation using FastAPI\n',
    'author': 'Yuri Escalianti',
    'author_email': 'yuriescl@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/talvezutil/ancora',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
