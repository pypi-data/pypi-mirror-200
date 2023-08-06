# nd-core-lib

[![standard-readme compliant](https://img.shields.io/badge/standard--readme-OK-green.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

Core library for nDimensional. Currently this contains only add and sub method and it can be used like this,

```
import nDimensional as nD

print(nD.add(1, 2))
```

## Table of Contents

- [Install](#install)
- [Usage](#usage)

## Install

To test the package in local, go into `nd-core-lib` (root folder) and run

```
pip install -e .
```

## Usage

To create the distribution,

```
python setup.py sdist
```

Install twin
```
pip install twine
```

To upload the distribution to PyPI,

```
twine upload dist/* --verbose
```

To run unit tests,

```
pytest
```

To run the tests against all the supported Python versions,

```
tox
```
