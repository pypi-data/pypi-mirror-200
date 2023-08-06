# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['canopy', 'canopy.templates']

package_data = \
{'': ['*'], 'canopy': ['static/*']}

install_requires = \
['webint-ai>=0.0,<0.1',
 'webint-auth>=0.0,<0.1',
 'webint-code>=0.0,<0.1',
 'webint-data>=0.0,<0.1',
 'webint-editor>=0.0,<0.1',
 'webint-guests>=0.0,<0.1',
 'webint-live>=0.0,<0.1',
 'webint-media>=0.0,<0.1',
 'webint-mentions>=0.0,<0.1',
 'webint-owner>=0.0,<0.1',
 'webint-player>=0.0,<0.1',
 'webint-posts>=0.0,<0.1',
 'webint-search>=0.0,<0.1',
 'webint-sites>=0.0,<0.1',
 'webint-system>=0.0,<0.1',
 'webint-tracker>=0.0,<0.1',
 'webint>=0.1,<0.2']

entry_points = \
{'websites': ['canopy = canopy:app']}

setup_kwargs = {
    'name': 'canopy-platform',
    'version': '0.0.25',
    'description': 'a decentralized social web platform',
    'long_description': 'None',
    'author': 'Angelo Gladding',
    'author_email': 'angelo@ragt.ag',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://ragt.ag/code/projects/canopy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
