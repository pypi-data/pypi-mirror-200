# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vams_cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['vams = vams_cli.cli:main']}

setup_kwargs = {
    'name': 'vams-cli',
    'version': '0.2.11',
    'description': '',
    'long_description': '# VAMS CLI\n\nCommands\n\n* `vams --help` - show available commands\n* `vams ping` - service health check\n* `vams login -u username` - login, username example `user@domain.com`\n* `vams download` - download all available data\n* `vams download --help` - show available download options\n',
    'author': 'Kuzin Stepan',
    'author_email': 'kossaress@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
