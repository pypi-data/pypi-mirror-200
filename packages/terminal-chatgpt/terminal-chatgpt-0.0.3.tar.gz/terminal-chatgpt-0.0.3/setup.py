# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['terminal_chatgpt']

package_data = \
{'': ['*']}

install_requires = \
['click==8.1.3',
 'halo==0.0.31',
 'openai==0.27.2',
 'prompt-toolkit>=3.0.38,<4.0.0',
 'pyreadline==2.1',
 'rich==13.3.3']

entry_points = \
{'console_scripts': ['gpt = terminal_chatgpt.gpt:gpt_entry_point']}

setup_kwargs = {
    'name': 'terminal-chatgpt',
    'version': '0.0.3',
    'description': '',
    'long_description': None,
    'author': 'Danylo Omelchenko',
    'author_email': 'dpixelstudio@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
