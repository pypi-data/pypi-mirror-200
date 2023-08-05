# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['edgedb_orm']

package_data = \
{'': ['*']}

install_requires = \
['black',
 'devtools',
 'edgedb>=1.2.0,<2.0.0',
 'fastapi',
 'orjson>=3.6,<4.0',
 'pydantic[email]']

setup_kwargs = {
    'name': 'edgedb-orm',
    'version': '1.0.10',
    'description': '',
    'long_description': 'None',
    'author': 'Jeremy Berman',
    'author_email': 'jerber@sas.upenn.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
