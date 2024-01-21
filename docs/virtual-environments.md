# A Word on Virtual Environments

You _really should_ use virtual environments and in fact, PyPi template requires you to use `pyenv`.

By convention create a virtualenv with pyenv named after your project's folder and install PyPi template in that environment. I will be your project management environment.

PyPi Template will make more environments for other use cases, such as running, testing and documentation generation. The `Makefile` provides targets to handle these environments, instantiating the right one when needed. So using the `Makefile` targets ensures you use a clean environment for each activity.

> Pro-Tip: when initializing a new project, PyPi Template will automagically use the Makefile to install the environments, as we'll see in a minute...

The environments in use in a project called "my-project" are:

* `my-project` - created by you, holding `pypi-template` and its requirments
* `my-project-run` - created by PyPi Template, holding you're projects requirements from requiremens.txt to run it
* `my-project-docs` - created by PyPi Template, holding requirements to build your project's documentation
* `my-project-test-"version"` - created by PyPi Template, holding requirements to build and test your project using Python "version"

## Pyenv

To use Pyenv, and test against multiple versions of Python, make sure to install Pyenv and its virtualenv support:

```console
% brew install pyenv
% git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv
% echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.zshrc
```

Next, install some Python versions:

```console
% pyenv install 3.11.5
% pyenv install 3.10.13
% pyenv install 3.9.18
% pyenv install 3.8.12
```

The `Makefile` will create virtual environments using these Python versions to keep everything nice and cleanly separated. You can have all the required envrionments create using `make install` and remove them using `make uninstall`:

```console
(pypi-template) % make install
👷‍♂️ creating virtual environment pypi-template-docs
pyenv local --unset
pyenv virtualenv pypi-template-docs > /dev/null
pyenv local pypi-template-docs
👷‍♂️ installing requirements in pypi-template-docs
pip install -U pip > /dev/null
👷‍♂️ creating virtual test environment pypi-template-test-3.8.12
pyenv local --unset
pyenv virtualenv 3.8.12 pypi-template-test-3.8.12 > /dev/null
pyenv local pypi-template-test-3.8.12
pip install -U pip > /dev/null
pip install -r requirements.test.txt > /dev/null
👷‍♂️ creating virtual test environment pypi-template-test-3.9.18
pyenv local --unset
pyenv virtualenv 3.9.18 pypi-template-test-3.9.18 > /dev/null
pyenv local pypi-template-test-3.9.18
pip install -U pip > /dev/null
pip install -r requirements.test.txt > /dev/null
👷‍♂️ creating virtual test environment pypi-template-test-3.10.13
pyenv local --unset
pyenv virtualenv 3.10.13 pypi-template-test-3.10.13 > /dev/null
pyenv local pypi-template-test-3.10.13
pip install -U pip > /dev/null
pip install -r requirements.test.txt > /dev/null
👷‍♂️ creating virtual test environment pypi-template-test-3.11.5
pyenv local --unset
pyenv virtualenv 3.11.5 pypi-template-test-3.11.5 > /dev/null
pyenv local pypi-template-test-3.11.5
pip install -U pip > /dev/null
pip install -r requirements.test.txt > /dev/null
👷‍♂️ installing requirements in pypi-template
pyenv local pypi-template
pip install -U pip > /dev/null
pip install -r requirements.pypi.txt > /dev/null

```

```console
(pypi-template) % make uninstall
👷‍♂️ deleting virtual environment pypi-template-docs
pyenv virtualenv-delete pypi-template-docs
pyenv-virtualenv: remove /Users/xtof/.pyenv/versions/3.8.12/envs/pypi-template-docs? y
👷‍♂️ deleting virtual environment pypi-template-test-3.8.12
pyenv virtualenv-delete pypi-template-test-3.8.12
pyenv-virtualenv: remove /Users/xtof/.pyenv/versions/3.8.12/envs/pypi-template-test-3.8.12? y
👷‍♂️ deleting virtual environment pypi-template-test-3.9.18
pyenv virtualenv-delete pypi-template-test-3.9.18
pyenv-virtualenv: remove /Users/xtof/.pyenv/versions/3.9.18/envs/pypi-template-test-3.9.18? y
👷‍♂️ deleting virtual environment pypi-template-test-3.10.13
pyenv virtualenv-delete pypi-template-test-3.10.13
pyenv-virtualenv: remove /Users/xtof/.pyenv/versions/3.10.13/envs/pypi-template-test-3.10.13? y
👷‍♂️ deleting virtual environment pypi-template-test-3.11.5
pyenv virtualenv-delete pypi-template-test-3.11.5
pyenv-virtualenv: remove /Users/xtof/.pyenv/versions/3.11.5/envs/pypi-template-test-3.11.5? y
pyenv local pypi-template
👷‍♂️ deleting all packages from current environment
pip freeze | cut -d"@" -f1 | cut -d'=' -f1 | xargs pip uninstall -y > /dev/null
```
