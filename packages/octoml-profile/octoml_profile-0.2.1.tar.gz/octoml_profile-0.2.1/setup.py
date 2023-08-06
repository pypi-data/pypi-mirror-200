# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['octoml_profile',
 'octoml_profile.interceptors',
 'octoml_profile.patches',
 'octoml_profile.protos']

package_data = \
{'': ['*']}

install_requires = \
['grpcio>=1.42.0,<2.0.0', 'onnx>=1.12.0,<2.0.0']

setup_kwargs = {
    'name': 'octoml-profile',
    'version': '0.2.1',
    'description': 'Client package for OctoML Profile service',
    'long_description': None,
    'author': 'Greg Bonik',
    'author_email': 'gbonik@octoml.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
