# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycode128', 'pycode128.cli_tools']

package_data = \
{'': ['*']}

install_requires = \
['click==8.1.3', 'cloup>=2.0.0,<3.0.0', 'pillow>=9.4.0,<10.0.0']

entry_points = \
{'console_scripts': ['pycode128 = pycode128.cli_tools.cli:pycode128']}

setup_kwargs = {
    'name': 'pycode128',
    'version': '2.3.0',
    'description': 'Python extension for Code128 barcode generator library.',
    'long_description': "# Code128 library's python extension\n\n\n[![pypi](https://img.shields.io/pypi/v/pycode128.svg)](https://pypi.org/project/pycode128/)\n[![python](https://img.shields.io/pypi/pyversions/pycode128.svg)](https://pypi.org/project/pycode128/)\n[![Build Status](https://github.com/gpongelli/pycode128/actions/workflows/complete.yml/badge.svg)](https://github.com/gpongelli/pycode128/actions/workflows/complete.yml)\n[![codecov](https://codecov.io/gh/gpongelli/pycode128/branch/main/graphs/badge.svg)](https://codecov.io/github/gpongelli/pycode128)\n\n\n\nPython extension for Code128 barcode generator library\n\n\n* Documentation: <https://gpongelli.github.io/pycode128>\n* GitHub: <https://github.com/gpongelli/pycode128>\n* PyPI: <https://pypi.org/project/pycode128/>\n* Free software: MIT\n\n\n## Features\n\n* [Code128 library](https://github.com/fhunleth/code128) python wrapper, included as submodule\n  and build when creating python extension\n* Poetry managed project\n* C code checked via [check tool](https://libcheck.github.io/check/), compiled and run through pytst on all python version under Ubuntu OS\n* Multiple OS (Linux, Windows, MacOS) and Python compilation via [cibuildwhel](https://github.com/pypa/cibuildwheel)\n* [cibuildwheel manylinux_2_28 custom images](https://hub.docker.com/r/gpongelli/manylinux_python) with pre-built python from source,\n  to being able to compile check against correct python version\n* ~~[ARM-runner action](https://github.com/pguyot/arm-runner-action) custom [images](https://github.com/gpongelli/arm-runner-python/releases)\n  with pre-built python from source, to build RPI wheels~~\n\n## Credits\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [gpongelli/cookiecutter-pypackage](https://github.com/gpongelli/cookiecutter-pypackage) project template.\n",
    'author': 'Gabriele Pongelli',
    'author_email': 'gabriele.pongelli@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/gpongelli/pycode128',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<4.0',
}
from build_extension import *
build(setup_kwargs)

setup(**setup_kwargs)
