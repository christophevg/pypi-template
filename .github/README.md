# PyPi Template

> My take at a template repository that I can fork for every Python project I want to push to PyPi

[![Latest Version on PyPI](https://img.shields.io/pypi/v/pypi-template.svg)](https://pypi.python.org/pypi/pypi-template/)
[![Build Status](https://secure.travis-ci.org/christophevg/pypi-template.svg?branch=master)](http://travis-ci.org/christophevg/pypi-template)
[![Coverage Status](https://coveralls.io/repos/github/christophevg/pypi-template/badge.svg?branch=master)](https://coveralls.io/github/christophevg/pypi-template?branch=master)
[![Built with PyPi Template](https://img.shields.io/badge/PyPi_Template-v0.0.4-blue.svg)](https://github.com/christophevg/pypi-template)
[![Documentation Status](https://readthedocs.org/projects/pypi-template/badge/?version=latest)](https://pypi-template.readthedocs.io/en/latest/?badge=latest)

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

The repository also includes a small script that automates these steps. If you install the module, the script gets registered in your PATH, and allows for

```bash
$ pip install pypi-template

$ pypi-template create my-new-project git@github.com:my-account
Cloning into 'pypi-template'...
remote: Enumerating objects: 53, done.
remote: Counting objects: 100% (53/53), done.
remote: Compressing objects: 100% (24/24), done.
remote: Total 53 (delta 16), reused 50 (delta 13), pack-reused 0
Unpacking objects: 100% (53/53), done.

$ cd my-new-project/

$ ls
LICENSE.txt		pypi-template		tests
MANIFEST.in		requirements.txt	tox.ini
Makefile		setup.py

$ git remote -v
origin	git@github.com:my-account/my-new-project.git (fetch)
origin	git@github.com:my-account/my-new-project.git (push)
```

### How to upgrade to the lastest version of PyPi Template?

Currently PyPi Template is still very much a moving target. New commits to this project are not guaranteed to turn into conflicts. We'll consider PyPi Template a v1.0.0 project once we've found ways to clearly separate PyPi Template from your project. Until then, you'll have to hack it a bit by merging the changes and going through the conflicts manually.

The procedure will be:

```bash
$ git remote add template git@github.com:christophevg/pypi-template
$ git fetch template
$ git merge template
```

Or use the `pypi-template` script:

```bash
$ pypi-template upgrade
```

The latter can also be used to "upgrade" and existing project, but this will also often introduce a lot of manual conflict resolution work ;-)

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

### Publishing

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

If you want to publish your documentation (from the [docs/](docs/) folder) to e.g. [ReadTheDocs](https://readthedocs.org), import the repository over there also.
