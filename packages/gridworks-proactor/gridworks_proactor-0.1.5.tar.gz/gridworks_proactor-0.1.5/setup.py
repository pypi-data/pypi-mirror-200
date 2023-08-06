# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src',
 'gwproactor_test': 'src/gwproactor_test',
 'gwproactor_test.dummies': 'src/gwproactor_test/dummies',
 'gwproactor_test.dummies.child': 'src/gwproactor_test/dummies/child',
 'gwproactor_test.dummies.parent': 'src/gwproactor_test/dummies/parent'}

packages = \
['gwproactor',
 'gwproactor.config',
 'gwproactor_test',
 'gwproactor_test.dummies',
 'gwproactor_test.dummies.child',
 'gwproactor_test.dummies.parent']

package_data = \
{'': ['*'], 'gwproactor_test': ['config/*']}

install_requires = \
['gridworks-protocol>=0.3.6',
 'paho-mqtt>=1.6.1,<2.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'pydantic>=1.10.6,<2.0.0',
 'python-dotenv>=1.0.0,<2.0.0',
 'result>=0.9.0,<0.10.0',
 'xdg>=6.0.0,<7.0.0']

extras_require = \
{'tests': ['pytest>=7.2.0,<8.0.0', 'pytest-asyncio>=0.20.3,<0.21.0']}

setup_kwargs = {
    'name': 'gridworks-proactor',
    'version': '0.1.5',
    'description': 'Gridworks Proactor',
    'long_description': "# Gridworks Proactor\n\n[![PyPI](https://img.shields.io/pypi/v/gridworks-proactor.svg)][pypi status]\n[![Status](https://img.shields.io/pypi/status/gridworks-proactor.svg)][pypi status]\n[![Python Version](https://img.shields.io/pypi/pyversions/gridworks-proactor)][pypi status]\n[![License](https://img.shields.io/pypi/l/gridworks-proactor)][license]\n\n[![Read the documentation at https://gridworks-proactor.readthedocs.io/](https://img.shields.io/readthedocs/gridworks-proactor/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/thegridelectric/gridworks-proactor/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/thegridelectric/gridworks-proactor/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi status]: https://pypi.org/project/gridworks-proactor/\n[read the docs]: https://gridworks-proactor.readthedocs.io/\n[tests]: https://github.com/thegridelectric/gridworks-proactor/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/thegridelectric/gridworks-proactor\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Features\n\n- TODO\n\n## Requirements\n\n- TODO\n\n## Installation\n\nYou can install _Gridworks Proactor_ via [pip] from [PyPI]:\n\n```console\n$ pip install gridworks-proactor\n```\n\n## Usage\n\nPlease see the [Command-line Reference] for details.\n\n## Contributing\n\nContributions are very welcome. In order to develop, do this:\n\n```console\n$ poetry install --all-extras\n```\n\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_Gridworks Proactor_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/thegridelectric/gridworks-proactor/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/thegridelectric/gridworks-proactor/blob/main/LICENSE\n[contributor guide]: https://github.com/thegridelectric/gridworks-proactor/blob/main/CONTRIBUTING.md\n[command-line reference]: https://gridworks-proactor.readthedocs.io/en/latest/usage.html\n",
    'author': 'Jessica Millar',
    'author_email': 'jmillar@gridworks-consulting.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/thegridelectric/gridworks-proactor',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
