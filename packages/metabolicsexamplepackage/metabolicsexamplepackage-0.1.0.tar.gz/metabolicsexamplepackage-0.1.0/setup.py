# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['metabolicsexamplepackage']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=2.0.0,<3.0.0', 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'metabolicsexamplepackage',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Ivan Thung',
    'author_email': 'ivanthung@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.09,<4.0',
}


setup(**setup_kwargs)
