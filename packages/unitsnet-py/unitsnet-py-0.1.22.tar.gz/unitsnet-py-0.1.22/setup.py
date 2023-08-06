# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['unitsnet_py', 'unitsnet_py.units']

package_data = \
{'': ['*']}

install_requires = \
['jinja2>=3.1.2,<4.0.0']

setup_kwargs = {
    'name': 'unitsnet-py',
    'version': '0.1.22',
    'description': 'A better way to hold unit variables and easily convert to the destination unit',
    'long_description': '# unitsnet_py\n\nA better way to hold unit variables and easily convert to the destination unit \n',
    'author': 'Haim Kastner',
    'author_email': 'haim.kastner@gmail.com',
    'maintainer': 'Haim Kastner',
    'maintainer_email': 'haim.kastner@gmail.com',
    'url': 'https://github.com/haimkastner/unitsnet-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

