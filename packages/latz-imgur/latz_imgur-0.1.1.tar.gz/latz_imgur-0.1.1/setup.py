# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['latz_imgur']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.1,<0.24.0', 'latz==0.2.0', 'pydantic>=1.10.4,<2.0.0']

entry_points = \
{'latz': ['imgur = latz_imgur.main']}

setup_kwargs = {
    'name': 'latz-imgur',
    'version': '0.1.1',
    'description': 'Imgur plugin for the popular latz image search CLI tool',
    'long_description': '# latz-imgur\nImgur plugin for the popular latz image search CLI tool\n',
    'author': 'Travis Hathaway',
    'author_email': 'travis.j.hathaway@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
