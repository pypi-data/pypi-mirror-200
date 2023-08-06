# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bnv']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0']

setup_kwargs = {
    'name': 'bnv',
    'version': '0.1.1a1',
    'description': 'semver based version management tool, for bumping next version.',
    'long_description': None,
    'author': 'Marco Bartel',
    'author_email': 'bsimpson888@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/bsimpson888/bnv',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
