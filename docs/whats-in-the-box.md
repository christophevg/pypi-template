# What's in The Box?

PyPi Template brings together common/best practices for managing a Python project and publishing it on the [Python Package Index](https://pypi.org).

It includes support for:
* building and publishing a package to PyPi  
* testing on several Python versions, using tox, pytest and coverage
* running those tests when pushed to GitHub
* generating documentation and publishing it on readthedocs

The main component of PyPi Template is a command line tool called `pypi-template`, which maintains several files in your project, based on templates and your answers to a set of questions.

The second component is a `Makefile` that orachestrates most actions, that are not actively driven by templates, but make use of the generated files.

A typical workflow, starting from scratch looks like:

```console
% mkdir my-new-project
% cd my-new-project
% git init
% pyenv virtualenv my-new-project
% pyenv local my-new-project
(my-new-project) % pip install pypi-template
(my-new-project) % pypi-template init
```

This creates a new project folder, activates a virtual environment, install PyPi Template and uses it to initialize the project. When done the folder looks like:

```console
(my-new-project) % ls -a
.                     .python-version       docs                  requirements.txt
..                    .readthedocs.yaml     my_brand_new_project  setup.py
.github               LICENSE.txt           requirements.docs.txt tests
.gitignore            MANIFEST.in           requirements.pypi.txt tox.ini
.pypi-template        Makefile              requirements.test.txt
```

Now using the `Makefile` targets, common activities can be executed:

```console
% make test
% make lint
% make doc
% make publish-test
% make publish
```

After configuring your project on [GitHub](https://github.com), [Read the Docs](https://readthedocs.org) and [Coveralls](https://coveralls.io), upon pushing your to your repository, tests will run, documentation will be updated online and test coverage results will be published.
