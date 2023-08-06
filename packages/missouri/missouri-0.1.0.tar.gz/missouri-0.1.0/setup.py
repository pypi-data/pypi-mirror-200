# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['missouri']

package_data = \
{'': ['*']}

install_requires = \
['simplejson>=3,<4']

setup_kwargs = {
    'name': 'missouri',
    'version': '0.1.0',
    'description': 'Read and write JSON in one line',
    'long_description': 'None',
    'author': 'Paul Melnikow',
    'author_email': 'github@paulmelnikow.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/metabolize/missouri',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
