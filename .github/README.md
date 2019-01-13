# PyPi Template

> My take at a template repository that I can fork for every Python project I want to push to PyPi

[![Latest Version on PyPI](https://img.shields.io/pypi/v/pypi-template.svg)](https://pypi.python.org/pypi/pypi-template/)
[![Supported Implementations](https://img.shields.io/pypi/pyversions/pypi-template.svg)](https://pypi.python.org/pypi/pypi-template/)
[![Build Status](https://secure.travis-ci.org/christophevg/pypi-template.svg?branch=master)](http://travis-ci.org/christophevg/pypi-template)
[![Documentation Status](https://readthedocs.org/projects/pypi-template/badge/?version=latest)](https://pypi-template.readthedocs.io/en/latest/?badge=latest)
[![Coverage Status](https://coveralls.io/repos/github/christophevg/pypi-template/badge.svg?branch=master)](https://coveralls.io/github/christophevg/pypi-template?branch=master)
[![Built with PyPi Template](https://img.shields.io/badge/PyPi_Template-v0.0.5-blue.svg)](https://github.com/christophevg/pypi-template)

## Howto, the executive summary

1. fork it
2. rename it
3. edit it
4. extend it
5. use it

## Getting Started

Forking and renaming are the two first steps when using this repository. They are both actions you perform at GitHub, but...

### Fork without forking...

You don't have to go through the GitHub concept of forking and do everything from the command line...

```bash
$ git clone https://github.com/christophevg/pypi-template
$ mv pypi-template your-new-project
$ cd your-new-project
$ git remote remove origin
$ git remote add origin git@github.com:your-account/your-new-project.git
$ git push -u master origin
```

### Use the Command Line

The repository also includes a small script that copies the files from a clone of the repository. If you install the module, the script gets registered in your PATH, and allows for

```bash
$ pip install pypi-template

$ mkdir my-new-project
$ cd my-new-project

$ pypi-template

$ ls -la
total 40
drwxr-xr-x  11 xtof  staff   352 Nov 11 21:34 .
drwxr-xr-x  46 xtof  staff  1472 Nov 11 21:10 ..
drwxr-xr-x   3 xtof  staff    96 Nov 11 21:35 .github
-rw-r--r--   1 xtof  staff   144 Nov 11 21:31 .travis.yml
-rw-r--r--   1 xtof  staff  1067 Nov 11 21:34 LICENSE.txt
-rw-r--r--   1 xtof  staff   443 Nov 11 21:34 Makefile
drwxr-xr-x   6 xtof  staff   192 Nov 11 21:35 docs
drwxr-xr-x   3 xtof  staff    96 Nov 11 21:35 pypi_template
-rw-r--r--   1 xtof  staff  1830 Nov 11 21:34 setup.py
drwxr-xr-x   3 xtof  staff    96 Nov 11 21:35 tests
-rw-r--r--   1 xtof  staff   167 Nov 11 21:34 tox.ini
```

The script only copies files that don't exist yet, so it can also be used to upgrade to a new version of PyPi Template, and import new features based on added folders. For changes to existing files, a more elaborate copying function will be added later, probably ;-)

## Things to edit

1. module top-level folder

There is a placeholder top-level module folder. You'll probably want to rename that.

```bash
$ mv pypi_template your_new_project
```

2. LICENSE.txt

Change the license to whatever you feel is (more) appropriate.

3. .github/README.md

Replace this information with information regarding your project.

4. setup.py

Replace the Python package configuration with one appropriate to your project.

5. docs/

The `docs/` contains a copy of this README as a placeholder for additional documentation, that can be published to [ReadTheDocs](https://readthedocs.org). Edit `conf.py` to reflect your project's name and description.

## Things to do

### Testing

A basic testing setup has been prepared. To run it locally, issue...

```bash
$ make test
...
___________________________________ summary ____________________________________
  py27: commands succeeded
  congratulations :)
```

Head over to [https://travis-ci.org](https://travis-ci.org) and register your project. A basic CI configuration is also provided.

Head over to [https://coveralls.io](https://coveralls.io) and register your project to consult your code coverage reporting.

### Generate/Publish Documentation

```bash
$ make docs
```

This wil generate a HTML version of your `docs/` and open it in a browser.

If you want to publish your documentation (from the [docs/](docs/) folder) to e.g. [ReadTheDocs](https://readthedocs.org), import the repository over there also.

### Publishing to PyPi

Head over to [https://test.pypi.org](https://test.pypi.org) and register for an account. Next simply issue...

```bash
$ make publish-test
```

to publish your module to the test instance of PyPi.

or

```bash
$ make publish
```

to publish your module to the main instance of  [PyPi](https://pypi.org).
