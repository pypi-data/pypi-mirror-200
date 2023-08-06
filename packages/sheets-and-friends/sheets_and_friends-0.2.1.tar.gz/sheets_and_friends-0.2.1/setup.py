# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sheets_and_friends', 'sheets_and_friends.converters']

package_data = \
{'': ['*']}

install_requires = \
['click_log',
 'glom>=23.1.1,<24.0.0',
 'linkml-runtime==1.4.5',
 'pandas>=1.3.4,<2.0.0',
 'pandasql>=0.7.3,<0.8.0',
 'pygsheets>=2.0.5,<3.0.0',
 'schemasheets>=0.1.21,<0.2.0']

entry_points = \
{'console_scripts': ['do_shuttle = sheets_and_friends.shuttle:do_shuttle',
                     'modifications_and_validation = '
                     'sheets_and_friends.modifications_and_validation:modifications_and_validation']}

setup_kwargs = {
    'name': 'sheets-and-friends',
    'version': '0.2.1',
    'description': 'Create a LinkML model with as-is imported slots, imported but modified slots (via yq), or newly minted slots (via schemasheets)',
    'long_description': 'None',
    'author': 'Mark Andrew Miller',
    'author_email': 'MAM@lbl.gov',
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
