# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['typer_to_textual']

package_data = \
{'': ['*']}

install_requires = \
['rich>=13.3.2,<14.0.0', 'textual>=0.10.1,<0.11.0', 'typer>=0.7.0,<0.8.0']

extras_require = \
{':python_version >= "3.10" and python_version < "4.0"': ['xdotool>=0.4.0,<0.5.0']}

setup_kwargs = {
    'name': 'typer-to-textual',
    'version': '2.1.0',
    'description': '',
    'long_description': '# typer-to-texual',
    'author': 'palla98',
    'author_email': 'pallaria98@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
