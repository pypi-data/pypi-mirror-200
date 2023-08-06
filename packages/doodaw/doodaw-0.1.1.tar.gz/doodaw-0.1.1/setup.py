# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['doodaw']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'doodaw',
    'version': '0.1.1',
    'description': "A Discord bot\n\nThis is a Discord bot that will do stuff.\nRight now it only responds to '$hello' in the general channel of https://discord.gg/JPyHw558\n",
    'long_description': None,
    'author': 'The kids',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
