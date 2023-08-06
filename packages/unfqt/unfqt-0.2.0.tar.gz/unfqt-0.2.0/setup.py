# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['unfqt']

package_data = \
{'': ['*']}

install_requires = \
['detecta>=0.0.5,<0.0.6', 'numpy>=1.24.2,<2.0.0', 'pandas>=1.5.3,<2.0.0']

setup_kwargs = {
    'name': 'unfqt',
    'version': '0.2.0',
    'description': '',
    'long_description': 'None',
    'author': 'Joe Schr',
    'author_email': 'joe.vandelay@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
