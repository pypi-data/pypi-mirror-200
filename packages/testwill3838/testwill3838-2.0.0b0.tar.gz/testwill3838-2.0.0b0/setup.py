# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['testwill3838']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.0,<4.0', 'backoff>=2.0,<3.0', 'requests>=2.0,<3.0']

setup_kwargs = {
    'name': 'testwill3838',
    'version': '2.0.0b0',
    'description': '',
    'long_description': '# Example Package\n\nThis is a simple example package. You can use\n[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)\nto write your content.\n',
    'author': 'William',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
