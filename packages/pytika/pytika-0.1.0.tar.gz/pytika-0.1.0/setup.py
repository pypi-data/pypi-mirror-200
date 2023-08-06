# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytika']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'pytika',
    'version': '0.1.0',
    'description': 'Apache Tika Server python client',
    'long_description': '# PyTika\n\n![Workflow status](https://github.com/agriplace/pytika/actions/workflows/main.yml/badge.svg)\n\n\nAn Apache Tika Server python client.\n',
    'author': 'RamiAwar',
    'author_email': 'rami.awar.ra@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
