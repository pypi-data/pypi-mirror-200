# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qctrlcommons',
 'qctrlcommons.graphql',
 'qctrlcommons.node',
 'qctrlcommons.validation']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.3,<4.0.0',
 'graphql-core>=3.2.1,<3.3.0',
 'inflection>=0.5.1,<0.6.0',
 'jsonschema>=4.17.3,<5.0.0',
 'networkx>=2.7.0,<3.0.0',
 'numpy>=1.23.5,<2.0.0',
 'python-forge>=18.6.0,<19.0.0',
 'scipy>=1.9.3',
 'sympy>=1.11.1,<2.0.0']

setup_kwargs = {
    'name': 'qctrl-commons',
    'version': '18.0.1',
    'description': 'Q-CTRL Commons',
    'long_description': '# Q-CTRL Commons\n\nQ-CTRL Commons is a collection of common libraries for the Python language.\n',
    'author': 'Q-CTRL',
    'author_email': 'support@q-ctrl.com',
    'maintainer': 'Q-CTRL',
    'maintainer_email': 'support@q-ctrl.com',
    'url': 'https://q-ctrl.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
