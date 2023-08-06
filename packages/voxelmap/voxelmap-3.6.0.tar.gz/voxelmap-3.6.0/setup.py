# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['voxelmap']

package_data = \
{'': ['*']}

install_requires = \
['colorcet>=3.0.1,<4.0.0',
 'matplotlib>=3.6.2,<4.0.0',
 'numpy>=1.24.1,<2.0.0',
 'opencv-python>=4.7.0.68,<5.0.0.0',
 'pandas>=1.5.2,<2.0.0',
 'pytest>=7.2.0,<8.0.0',
 'pyvista>=0.38.2,<0.39.0',
 'scikit-image>=0.19.3,<0.20.0',
 'scipy>=1.10.0,<2.0.0',
 'sphinx-rtd-theme>=1.2.0,<2.0.0',
 'sphinx>=6.1.3,<7.0.0']

setup_kwargs = {
    'name': 'voxelmap',
    'version': '3.6.0',
    'description': 'A Python library for making voxel and 3D models from NumPy arrays.',
    'long_description': '# voxelmap\n\n[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](https://raw.githubusercontent.com/andrewrgarcia/voxelmap/main/LICENSE)\n[![Documentation Status](https://readthedocs.org/projects/voxelmap/badge/?version=latest)](https://voxelmap.readthedocs.io/en/latest/?badge=latest)\n\nA Python library for making voxel and three-dimensional models from NumPy arrays. \n\n<a href="https://voxelmap.readthedocs.io/en/latest/">\n<img src="https://github.com/andrewrgarcia/voxelmap/blob/main/voxelmap.svg?raw=true" width="250"></a>\n\n## Installation and Local Usage \n\n```ruby\npip install voxelmap\n```\n\nIt is recommended you run voxelmap using a `virtualenv` virtual environment. To do so, follow the below simple protocol to create the virtual environment, run it, and install the package there:\n\n```ruby \nvirtualenv venv\nsource venv/bin/activate\npip install voxelmap\npython [your-voxelmap-script.py]\n```\nTo exit the virtual environment, simply type `deactivate`. To access it at any other time again, enter with the above `source venv...` command. \n\n## Just starting? Remote Usage with a Colab notebook (click below)\n\n<a href="https://colab.research.google.com/drive/1RMEMgZHlk_tKAzfS4QfXLJV9joDgdh8N?usp=sharing">\n<img src="https://raw.githubusercontent.com/andrewrgarcia/voxelmap/main/docs/img/colaboratory.png" width="500" ></a>\n\n\n## Disclaimer: Use At Your Own Risk\n\nThis program is free software. It comes without any warranty, to the extent permitted by applicable law. You can redistribute it and/or modify it under the terms of the MIT LICENSE, as published by Andrew Garcia. See LICENSE below for more details.\n\n**[MIT license](./LICENSE)** Copyright 2022 © <a href="https://github.com/andrewrgarcia" target="_blank">Andrew Garcia</a>.\n',
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
