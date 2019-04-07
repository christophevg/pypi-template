# Getting Started

PyPi template is hosted on PyPi, so...

```bash
$ pip install pypi-template
```

## Use PyPi Template to setup a new package

```bash
$ mkdir my-new-project
$ cd my-new-project
$ git init
$ pypi-template

```

PyPi template will ask you to provide some basic information, which allows it to generate several files for your. All files that are written are reported. When ready, you have a fresh, customized source tree.

### Things to edit

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
