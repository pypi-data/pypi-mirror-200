# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pysz']

package_data = \
{'': ['*'], 'pysz': ['.pytest_cache/*', '.pytest_cache/v/cache/*']}

install_requires = \
['numpy>=1.24.2,<2.0.0',
 'pandas>=1.5.3,<2.0.0',
 'pystreamvbyte',
 'zstandard==0.19.0']

setup_kwargs = {
    'name': 'pysz',
    'version': '0.1.0',
    'description': 'Package for reading and writing svb-zstd compressed data',
    'long_description': None,
    'author': 'Jinyang Zhang',
    'author_email': 'zhangjinyang@biols.ac.cn',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
