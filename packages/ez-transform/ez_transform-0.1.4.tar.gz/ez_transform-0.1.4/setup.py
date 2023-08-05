# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ezt',
 'ezt.build',
 'ezt.build.dfmodel',
 'ezt.build.sqlmodel',
 'ezt.include',
 'ezt.include.starter_project',
 'ezt.include.starter_project.models',
 'ezt.util']

package_data = \
{'': ['*'], 'ezt.include': ['macros/*'], 'ezt.util': ['yaml_schemas/*']}

install_requires = \
['Jinja2>=3.0.3,<4.0.0',
 'PyYAML>=6.0,<7.0',
 'adlfs>=2023.1.0,<2024.0.0',
 'click>=8.0.3,<9.0.0',
 'deltalake>=0.7.0,<0.8.0',
 'graphlib-backport>=1.0.3,<2.0.0',
 'jsonschema>=4.14.0,<5.0.0',
 'polars>=0.15.17,<0.16.0',
 'pyarrow==11.0.0',
 'rich-click>=1.3.0,<2.0.0',
 'rich>=12.2.0,<13.0.0',
 's3fs>=2022.11.0,<2023.0.0']

entry_points = \
{'console_scripts': ['ezt = ezt.main_cli:ezt']}

setup_kwargs = {
    'name': 'ez-transform',
    'version': '0.1.4',
    'description': 'Analytics engineering for data lakes.',
    'long_description': '💥 ez-transform (Ezt)\n================\n\nAnalytics Engineering for Data Lakes powered by\n[polars](https://github.com/pola-rs/polars),\n[arrow](https://github.com/apache/arrow) and\n[delta-rs](https://github.com/delta-io/delta-rs).\n\n👉 Installation\n------------\n\nWe recommend first setting up a Python virtual environment and activating it.\n\n```bash\n$ python -m venv .venv\n```\n\n```bash\n$ source .venv/bin/activate\n```\n\nAnd then install Ezt with pip into your virtual environment.\n\n```bash\n$ pip install ez-transform\n```\n\n👉 Getting started\n------------\n\nYou can test out Ezt by creating a project from the command line.\n\n```bash\n$ ezt init myproject && cd myproject\n```\n\nNow you have created a project and can use your IDE of choice to start\ndeveloping your data models. 🥳\n\nCheck out the documentation at <https://ez-transform.github.io/ezt-core/> to learn more about how to develop data models with Ezt.\n',
    'author': 'John Kaustinen',
    'author_email': 'jokausti@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ez-transform/ezt-core',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
