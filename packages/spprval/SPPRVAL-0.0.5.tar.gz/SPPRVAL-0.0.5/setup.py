# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spprval', 'spprval.validation']

package_data = \
{'': ['*'], 'spprval': ['data/*', 'data_for_val/*', 'val_datasets/*']}

setup_kwargs = {
    'name': 'spprval',
    'version': '0.0.5',
    'description': '',
    'long_description': None,
    'author': 'Roman223',
    'author_email': 'romius2001@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
