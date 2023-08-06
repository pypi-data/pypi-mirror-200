# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pg4j', 'pg4j.cli']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'SQLAlchemy>=1.4.27,<2.0.0',
 'psycopg2-binary>=2.9.2,<3.0.0',
 'pydantic[dotenv]>=1.10.7,<2.0.0',
 'typer>=0.4.0,<0.5.0',
 'types-PyYAML>=5.4.6,<6.0.0']

entry_points = \
{'console_scripts': ['pg4j = pg4j.__main__:app']}

setup_kwargs = {
    'name': 'pg4j',
    'version': '0.1.1',
    'description': 'A package designed to perform etl from a postgres database to a neo4j database.',
    'long_description': 'None',
    'author': 'Michael Statt',
    'author_email': 'michael.statt@modelyst.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
