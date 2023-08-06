# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qcio']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.7,<2.0.0']

setup_kwargs = {
    'name': 'qcio',
    'version': '0.0.1',
    'description': 'A package for structured Quantum Chemistry data.',
    'long_description': '# qcio\n\n[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/charliermarsh/ruff)\n[![image](https://img.shields.io/pypi/v/qcio.svg)](https://pypi.python.org/pypi/qcio)\n[![image](https://img.shields.io/pypi/l/qcio.svg)](https://pypi.python.org/pypi/qcio)\n[![image](https://img.shields.io/pypi/pyversions/qcio.svg)](https://pypi.python.org/pypi/qcio)\n[![Actions status](https://github.com/coltonbh/qcio/workflows/Tests/badge.svg)](https://github.com/coltonbh/qcio/actions)\n[![Actions status](https://github.com/coltonbh/qcio/workflows/Basic%20Code%20Quality/badge.svg)](https://github.com/coltonbh/qcio/actions)\n\nA package for structured Quantum Chemistry data.\n\nInspired by [QCElemental](https://github.com/MolSSI/QCElemental). Build for ease of use and rapid development.\n',
    'author': 'Colton Hicks',
    'author_email': 'github@coltonhicks.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
