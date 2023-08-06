# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drive']

package_data = \
{'': ['*']}

install_requires = \
['numpy==1.19.5', 'pandas==1.1.5', 'python-igraph==0.9.6']

entry_points = \
{'console_scripts': ['drive = drive.drive:main']}

setup_kwargs = {
    'name': 'drive-ibd',
    'version': '0.9.3',
    'description': 'cli tool to identify networks of individuals who share IBD segments overlapping loci of interest',
    'long_description': '',
    'author': 'James Baker',
    'author_email': 'james.baker@vanderbilt.edu',
    'maintainer': 'James Baker',
    'maintainer_email': 'james.baker@vanderbilt.edu',
    'url': 'https://github.com/belowlab/drive',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
