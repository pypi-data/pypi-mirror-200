# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['illuminate',
 'illuminate.adapter',
 'illuminate.common',
 'illuminate.decorators',
 'illuminate.exceptions',
 'illuminate.exporter',
 'illuminate.interface',
 'illuminate.manager',
 'illuminate.meta',
 'illuminate.meta.type',
 'illuminate.observation',
 'illuminate.observer']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy[asyncio]>=1.4.42,<2.0.0',
 'aiofile>=3.8.1,<4.0.0',
 'alembic>=1.7.7,<2.0.0',
 'asyncmy>=0.2.5,<0.3.0',
 'asyncpg>=0.26.0,<0.27.0',
 'click>=8.1.2,<9.0.0',
 'loguru>=0.6.0,<0.7.0',
 'psycopg2>=2.9.3,<3.0.0',
 'tornado>=6.1,<7.0']

entry_points = \
{'console_scripts': ['illuminate = illuminate.cli:cli']}

setup_kwargs = {
    'name': 'illuminated',
    'version': '0.2.0',
    'description': 'Lightwieght ETL Framework',
    'long_description': None,
    'author': 'Nikola Milojica',
    'author_email': 'nikola.milojica@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nikolamilojica/illuminate',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
