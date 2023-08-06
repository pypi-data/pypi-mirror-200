# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['backup_collector']

package_data = \
{'': ['*'], 'backup_collector': ['services/*']}

install_requires = \
['dacite>=1.6.0,<2.0.0',
 'networktools>=1.5.1,<2.0.0',
 'numpy>=1.23.4,<2.0.0',
 'tasktools>=1.1.69,<2.0.0',
 'tomli>=2.0.1,<3.0.0',
 'typer>=0.6.1,<0.7.0',
 'watchdog>=2.1.9,<3.0.0']

entry_points = \
{'console_scripts': ['backup_collector = backup_collector.__main__:app']}

setup_kwargs = {
    'name': 'backup-collector',
    'version': '1.0.0',
    'description': '',
    'long_description': 'None',
    'author': 'David Pineda',
    'author_email': 'dahalpi@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
