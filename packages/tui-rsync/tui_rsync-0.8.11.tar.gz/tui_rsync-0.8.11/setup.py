# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tui_rsync',
 'tui_rsync.cli',
 'tui_rsync.cli.groups',
 'tui_rsync.cli.source',
 'tui_rsync.config',
 'tui_rsync.models']

package_data = \
{'': ['*']}

install_requires = \
['peewee>=3.15.4,<4.0.0',
 'platformdirs>=3.1.1,<4.0.0',
 'pyfzf>=0.3.1,<0.4.0',
 'rich>=13.3.1,<14.0.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['tui-rsync = tui_rsync.main:main']}

setup_kwargs = {
    'name': 'tui-rsync',
    'version': '0.8.11',
    'description': 'tui-rsync will help you to manage yours backups.',
    'long_description': 'tui-rsync\n=========\n\n|PyPI version|\n\ntui-rsync is the application that will help you to manage yours backups.\nIt uses rsync for syncing backups.\n\nDependencies\n============\n\n-  rsync\n-  fzf\n\nAuthor\n======\n\nKostiantyn Klochko (c) 2023\n\nLicense\n=======\n\nUnder GNU GPL v3 license\n\n.. |PyPI version| image:: https://badge.fury.io/py/tui-rsync.svg\n   :target: https://badge.fury.io/py/tui-rsync\n',
    'author': 'Kostiantyn Klochko',
    'author_email': 'kostya_klochko@ukr.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/KKlochko/tui-rsync',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
