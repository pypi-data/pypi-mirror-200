# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wrts', 'wrts.types']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'wrts',
    'version': '0.4.0',
    'description': 'A small lil library for using the WRTS API ',
    'long_description': 'still in development pls wait xdddzs\n',
    'author': 'BadPythonCoder',
    'author_email': 'no@no.no',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
