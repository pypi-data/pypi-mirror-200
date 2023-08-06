# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gitflow_pyproject_version_bumper']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.31,<4.0.0', 'tomlkit>=0.11.7,<0.12.0']

setup_kwargs = {
    'name': 'gitflow-pyproject-version-bumper',
    'version': '0.1.2',
    'description': 'Automatic pyproject.toml based app version bumper',
    'long_description': "![python version](https://img.shields.io/pypi/pyversions/gitflow-pyproject-version-bumper?style=for-the-badge) \n[![version](https://img.shields.io/pypi/v/gitflow-pyproject-version-bumper?style=for-the-badge)](https://pypi.org/project/gitflow-pyproject-version-bumper/)\n\n# gitflow-pyproject-version-bumper\n> A git hook to automatically update the application version \n> in pyproject.toml when a release is started using [gitflow](https://github.com/nvie/gitflow).\n\n# Installation\nFrom PyPi:\n\n```\npip3 install gitflow-pyproject-version-bumper\npython3 -m gitflow_pyproject_version_bumper install\n```\n\nIf you want to install it from sources, try this:\n\n```\npython3 -m pip install poetry\npython3 -m pip install .\npython3 -m gitflow_pyproject_version_bumper install\n```\n\n# Usage\nJust start a release, as you usually do:\n`git flow release start 1.2.3`\n\nThat's it.\nThe app version in pyproject.toml has already been updated, \nand the change has been committed.\n",
    'author': 'Grigory Bukovsky',
    'author_email': 'booqoffsky@yandex.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/booqoffsky/gitflow-pyproject-version-bumper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
