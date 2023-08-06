# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qctrlvisualizer']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.3', 'numpy>=1.23.5,<2.0.0', 'qctrl-commons>=18.0.0,<19.0.0']

setup_kwargs = {
    'name': 'qctrl-visualizer',
    'version': '5.0.0',
    'description': 'Q-CTRL Visualizer',
    'long_description': "# Q-CTRL Visualizer\n\nProvides visualization of data for Q-CTRL's Python products.\n",
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
