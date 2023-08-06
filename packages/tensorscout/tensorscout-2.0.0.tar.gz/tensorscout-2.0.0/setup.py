# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tensorscout']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.7.1,<4.0.0',
 'numpy>=1.24.2,<2.0.0',
 'pathos>=0.3.0,<0.4.0',
 'scipy>=1.10.1,<2.0.0',
 'timethis>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'tensorscout',
    'version': '2.0.0',
    'description': 'A Python library for tensor operations powered by parallel processing',
    'long_description': '# tensorscout\n\n[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](https://raw.githubusercontent.com/andrewrgarcia/tensorscout/main/LICENSE)\n[![Documentation Status](https://readthedocs.org/projects/tensorscout/badge/?version=latest)](https://tensorscout.readthedocs.io/en/latest/?badge=latest)\n\nA Python library for tensor operations powered by parallel processing.\n\n<img src="https://raw.githubusercontent.com/andrewrgarcia/tensorscout/main/icon_scout.svg" width="400">\n\n\n## Installation\n\n```ruby\npip install tensorscout\n```\n\nIt is recommended you run voxelmap using a `virtualenv` virtual environment. To do so, follow the below simple protocol to create the virtual environment, run it, and install the package there:\n\n```ruby \nvirtualenv venv\nsource venv/bin/activate\npip install tensorscout\n```\nTo exit the virtual environment, simply type `deactivate`. To access it at any other time again, enter with the above `source venv...` command. \n',
    'author': 'andrewrgarcia',
    'author_email': 'garcia.gtr@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
