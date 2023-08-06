# Code128 library's python extension


[![pypi](https://img.shields.io/pypi/v/pycode128.svg)](https://pypi.org/project/pycode128/)
[![python](https://img.shields.io/pypi/pyversions/pycode128.svg)](https://pypi.org/project/pycode128/)
[![Build Status](https://github.com/gpongelli/pycode128/actions/workflows/complete.yml/badge.svg)](https://github.com/gpongelli/pycode128/actions/workflows/complete.yml)
[![codecov](https://codecov.io/gh/gpongelli/pycode128/branch/main/graphs/badge.svg)](https://codecov.io/github/gpongelli/pycode128)



Python extension for Code128 barcode generator library


* Documentation: <https://gpongelli.github.io/pycode128>
* GitHub: <https://github.com/gpongelli/pycode128>
* PyPI: <https://pypi.org/project/pycode128/>
* Free software: MIT


## Features

* [Code128 library](https://github.com/fhunleth/code128) python wrapper, included as submodule
  and build when creating python extension
* Poetry managed project
* C code checked via [check tool](https://libcheck.github.io/check/), compiled and run through pytst on all python version under Ubuntu OS
* Multiple OS (Linux, Windows, MacOS) and Python compilation via [cibuildwhel](https://github.com/pypa/cibuildwheel)
* [cibuildwheel manylinux_2_28 custom images](https://hub.docker.com/r/gpongelli/manylinux_python) with pre-built python from source,
  to being able to compile check against correct python version
* ~~[ARM-runner action](https://github.com/pguyot/arm-runner-action) custom [images](https://github.com/gpongelli/arm-runner-python/releases)
  with pre-built python from source, to build RPI wheels~~

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [gpongelli/cookiecutter-pypackage](https://github.com/gpongelli/cookiecutter-pypackage) project template.
