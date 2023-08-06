# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chromat']

package_data = \
{'': ['*']}

install_requires = \
['rich>=13.3.3,<14.0.0']

setup_kwargs = {
    'name': 'chromat',
    'version': '0.0.1',
    'description': 'color palettes!',
    'long_description': '\ufeff# chromat: algorithmic color palettes\ncoming soon!\n\nhttps://github.com/hexbenjamin/chromat',
    'author': 'hex benjamin',
    'author_email': '64101028+hexbenjamin@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
