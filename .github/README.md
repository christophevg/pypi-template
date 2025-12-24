# PyPi Template

> Template-based common/best practices for managing a Python package on PyPi

[![Latest Version on PyPI](https://img.shields.io/pypi/v/pypi-template.svg)](https://pypi.python.org/pypi/pypi-template/)
[![Supported Implementations](https://img.shields.io/pypi/pyversions/pypi-template.svg)](https://pypi.python.org/pypi/pypi-template/)
![Build Status](https://github.com/christophevg/pypi-template/actions/workflows/test.yaml/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/pypi-template/badge/?version=latest)](https://pypi-template.readthedocs.io/en/latest/?badge=latest)
[![Coverage Status](https://coveralls.io/repos/github/christophevg/pypi-template/badge.svg?branch=master)](https://coveralls.io/github/christophevg/pypi-template?branch=master)
[![Built with PyPi Template](https://img.shields.io/badge/PyPi_Template-v1.4.1-blue.svg)](https://github.com/christophevg/pypi-template)

## First Minutes with PyPi Template

PyPi Template aims to reduce the boilerplate overhead associated with setting up and maintaining a Python code base published on PyPI. It provides a set of templates to establish the essential and recommended best practice files.

In addition to setup and publishing support, it also offers automation through a Makefile for common development tasks, such as running and testing.

Below is a screenshot of your typical first minutes with PyPi Template, where you start from scratch and end up with a tested and published Python package.

```console
$ mkdir my-pypi-module
$ cd my-pypi-module

$ pyenv virtualenv pypi-template
$ pyenv local pypi-template
$ pip install pypi-template

$ pypi-template init
A description for the package: My PyPI Module
Select classifiers: Programming Language :: Python :: 3
Select classifiers: 
Select console scripts: 
First year of publication: 2025
Github account: christophevg
Github repo name: my-pypi-module
Keywords describing the package: best module ever
License: MIT
Package module name: my_pypi_module
Package name: my-pypi-module
Package tagline: showing off my best module
Package title: My PyPi Module
Project env: pypi-template
Readme: .github/README.md
Select requires: baseweb
Select requires: 
Select scripts: 
Select test requires: 
Your author name: Christophe VG
Your email address: contact@christophe.vg
Your full name: Christophe VG
Your name: Christophe VG
👷‍♂️ creating virtual environment my-pypi-module-run
👷‍♂️ creating virtual environment my-pypi-module-docs
👷‍♂️ creating virtual test environment my-pypi-module-test-3.9.18
👷‍♂️ creating virtual test environment my-pypi-module-test-3.10.13
👷‍♂️ creating virtual test environment my-pypi-module-test-3.11.12
👷‍♂️ creating virtual test environment my-pypi-module-test-3.12.10
👷‍♂️ activating project environment
👷‍♂️ installing requirements in my-pypi-module

$ ls -a
.                     .pypi-template        Makefile              requirements.test.txt
..                    .python-version       Makefile.backup       requirements.txt
.env                  .readthedocs.yaml     docs                  setup.py
.github               LICENSE.txt           my_pypi_module        tests
.gitignore            MANIFEST.in           requirements.docs.txt tox.ini

$ make run
👷‍♂️ activating run environment
👷‍♂️ running LOG_LEVEL=INFO python -m my_pypi_module 
hello Stranger

$ make coverage
👷‍♂️ activating test environments
All checks passed!
👷‍♂️ performing tests
========================================== test session starts ===========================================
platform darwin -- Python 3.11.12, pytest-8.4.0, pluggy-1.6.0
cachedir: .tox/py311/.pytest_cache
rootdir: /Users/xtof/Workspace/pypi-template/my-pypi-module
configfile: tox.ini
testpaths: tests
collected 1 item                                                                                         

tests/test_example.py .                                                                            [100%]

=========================================== 1 passed in 0.01s ============================================
py311: OK ✔ in 2.62 seconds
========================================== test session starts ===========================================
platform darwin -- Python 3.12.10, pytest-8.4.0, pluggy-1.6.0
cachedir: .tox/py312/.pytest_cache
rootdir: /Users/xtof/Workspace/pypi-template/my-pypi-module
configfile: tox.ini
testpaths: tests
collected 1 item                                                                                         

tests/test_example.py .                                                                            [100%]

=========================================== 1 passed in 0.01s ============================================
py312: OK ✔ in 1.57 seconds
========================================== test session starts ===========================================
platform darwin -- Python 3.10.13, pytest-8.4.0, pluggy-1.6.0
cachedir: .tox/py310/.pytest_cache
rootdir: /Users/xtof/Workspace/pypi-template/my-pypi-module
configfile: tox.ini
testpaths: tests
collected 1 item                                                                                         

tests/test_example.py .                                                                            [100%]

=========================================== 1 passed in 0.01s ============================================
py310: OK ✔ in 1.47 seconds
========================================== test session starts ===========================================
platform darwin -- Python 3.9.18, pytest-8.4.0, pluggy-1.6.0
cachedir: .tox/py39/.pytest_cache
rootdir: /Users/xtof/Workspace/pypi-template/my-pypi-module
configfile: tox.ini
testpaths: tests
collected 1 item                                                                                         

tests/test_example.py .                                                                            [100%]

=========================================== 1 passed in 0.01s ============================================
  py311: OK (2.62 seconds)
  py312: OK (1.57 seconds)
  py310: OK (1.47 seconds)
  py39: OK (1.45 seconds)
  congratulations :) (7.14 seconds)
👷‍♂️ creating coverage reports
Name                         Stmts   Miss  Cover
------------------------------------------------
my_pypi_module/__init__.py       1      0   100%
my_pypi_module/module.py        10      1    90%
tests/__init__.py                0      0   100%
tests/test_example.py            4      0   100%
------------------------------------------------
TOTAL                           15      1    93%
Wrote HTML report to htmlcov/index.html
Wrote LCOV report to coverage.lcov
👷‍♂️ activating project environment


$ make publish-test
👷‍♂️ activating project environment
👷‍♂️ building distribution
👷‍♂️ publishing to PyPI test
Uploading distributions to https://test.pypi.org/legacy/
Uploading my_pypi_module-0.0.1-py3-none-any.whl
100$ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 9.2/9.2 kB • 00:00 • ?
Uploading my_pypi_module-0.0.1.tar.gz
100$ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 8.5/8.5 kB • 00:00 • ?

View at:
https://test.pypi.org/project/my-pypi-module/0.0.1/
```


> [!NOTE]  
> Visit [Read the Docs](https://pypi-template.readthedocs.org) for the full documentation, including overviews and several examples.


