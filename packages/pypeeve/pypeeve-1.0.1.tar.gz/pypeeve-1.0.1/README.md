![PyPI](https://img.shields.io/pypi/v/pypeeve?style=flat-square)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/pypeeve/pypeeve/tests.yml?style=flat-square)
[![CodeQL](https://github.com/pypeeve/pypeeve/actions/workflows/codeql.yml/badge.svg)](https://github.com/pypeeve/pypeeve/actions/workflows/codeql.yml)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/pypeeve/pypeeve/pylint.yml?label=pylint&style=flat-square)
[![Upload Python Package](https://github.com/pypeeve/pypeeve/actions/workflows/python-publish.yml/badge.svg)](https://github.com/pypeeve/pypeeve/actions/workflows/python-publish.yml)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pypeeve?style=flat-square)
![GitHub](https://img.shields.io/github/license/pypeeve/pypeeve?style=flat-square)


# pypeeve
PyPeeve is a python library for python pet peeves! As a developer, you know how time-consuming and tedious it can be to write the same boilerplate code over and over again. The aim of this library is to provide a tool that helps developers to reduce their unnecessary effort in writing boilerplate codes repeatedly in every project, allowing you to focus on what really matters - solving problems and building new features.

## Installation
To install the latest version, run-
```
pip install pypeeve
```

## What PyPeeve Offers
There are the list of things pypeeve offers so far:
- [Logger](#logger)

## Logger
Pypeeve provides a set of pre-configured loggers. The simplest and
quickest way to use pypeeve logger and logger decorators is to import
a pre-configured logger that suit your need.

```python
from pypeeve.logger import logger

@logger.default
@logger.perf
def do_something():
    logger.info("Info logs")
    logger.error("Error logs")
```
Output-

```
[2023-03-27 02:28:47,680] - [DEBUG] - Entering do_something()
[2023-03-27 02:28:47,681] - [INFO] - Info logs
[2023-03-27 02:28:47,681] - [ERROR] - Error logs
[2023-03-27 02:28:47,682] - [DEBUG] - do_something() starting time: 91411.408944
[2023-03-27 02:28:47,682] - [DEBUG] - do_something() ending time: 91411.409873
[2023-03-27 02:28:47,683] - [INFO] - Total time taken to finish do_something(): 0.000929 second(s)
[2023-03-27 02:28:47,684] - [DEBUG] - Exiting do_something()
```

The detailed documentation about the pypeeve loggers can be found in
[logger readme](pypeeve/logger/README.md).

## License
Pypeeve is distributed under [MIT License](LICENSE). License details of all the third party tools used in pypeeve can be found in [Third Party Licenses](THIRD_PARTY_LICENSES).
