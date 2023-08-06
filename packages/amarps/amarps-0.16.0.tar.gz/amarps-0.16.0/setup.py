# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['amarps']

package_data = \
{'': ['*']}

install_requires = \
['click-log>=0.4.0,<0.5.0',
 'click>=8,<9',
 'dateparser>=1,<2',
 'requests>=2,<3',
 'selectorlib>=0.16,<0.17',
 'selenium-wire>=5,<6',
 'selenium>=4,<5',
 'webdriver-manager>=3,<4']

entry_points = \
{'console_scripts': ['amarps = amarps.main:main']}

setup_kwargs = {
    'name': 'amarps',
    'version': '0.16.0',
    'description': 'Download amazon product reviews and the reviewers profile information',
    'long_description': '[![Tests](https://github.com/joclement/amarps/workflows/Tests/badge.svg)](https://github.com/joclement/amarps/actions?workflow=Tests)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/joclement/amarps/main.svg)](https://results.pre-commit.ci/latest/github/joclement/amarps/main)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n[![Python Versions](https://img.shields.io/pypi/pyversions/amarps)](https://img.shields.io/pypi/pyversions/amarps)\n\n# Amazon Review Profile Scraper\n\nA very basic tool to scrape the user reviews of a product on Amazon the profiles that created those reviews.\n\nIt is intended to be used for research to analyze the quality of a user review based on\nother information belonging to the user.\n\n## Usage\n\n1. Install this tool `pip install amarps`.\n2. Run `python -m amarps --help` to check the usage\n3. Run e.g. `python -m amarps https://www.amazon.com/product-reviews/B07ZPL752N/`\n',
    'author': 'Joris Clement',
    'author_email': 'joclement@posteo.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/joclement/amarps',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4',
}


setup(**setup_kwargs)
