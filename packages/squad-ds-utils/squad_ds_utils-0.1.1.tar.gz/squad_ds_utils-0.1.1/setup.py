# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['squad_ds_utils']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.26.99,<2.0.0', 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'squad-ds-utils',
    'version': '0.1.1',
    'description': '',
    'long_description': '',
    'author': 'Ayush Shanker',
    'author_email': 'ayush+pypi@squadstack.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
