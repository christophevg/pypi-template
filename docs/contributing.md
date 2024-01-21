# Contributing

This is Open Source software, so [given enough eyeballs, all bugs are shallow](https://en.wikipedia.org/wiki/Linus%27s_Law). Your contributions are more than welcome.

This project is hosted on [GitHub](https://githhub.com/christophevg/pypi-template) and these (common) rules apply:

* Do use the [issues tracker](https://githhub.com/christophevg/pypi-template/issues).
* Let's discuss any proposed change or fix in an issue, so your work is not done in vain - I hate to reject pull requests...
* Create [pull requests](https://githhub.com/christophevg/pypi-template/pulls) against `next` branch if it is currently actively used, else use the `master` branch.
* Try to keep pull requests "atomic", and if possible related to an issue.

## My Development Workflow

I try to develop pypi-template in a self-hosting way, which means that I run it from the repository on the repository itself.

Running pypi-template from the repository can be done according to the following steps:

### Setup an Environment with Dependencies

PyPi Template is (highly optionated) convention driven and relies on Pyenv to keep everything nicely tucked away in [virtual environments](virtual-environments). So at this point avoiding Pyenv is not really an option.

```console
$ git clone https://github.com/christophevg/pypi-template.git
$ cd pypi-template
$ pyenv virtualenv pypi-template
$ pyenv local pypi-template
$ pip install -r requirements.txt
$ make install
$ make run
```

And if everything goes well, PyPi Template is run on itself, reporting every file is up2date.

### Running pypi-template from the Repository

As shown in the final command above, the `Makefile` allows for running the application/package. The default `RUN_CMD` is `python -m package_name` without any arguments. Using `RUN_ARGS` additional arguments can be added, which in case of PyPi Template itself is done in `Makefile.mak`: `RUN_ARGS = verbose debug apply`.

So, we can replace these to first edit alle variables and then actually apply them:

```console
% make run RUN_ARGS="verbose edit all apply"
pyenv local pypi-template-run
python -m `cat .pypi-template | grep "^package_module_name" | cut -d":" -f2` verbose edit all apply
A description for the package: Template-based common/best practices for managing a Python package on PyPi
Current classifiers:
- Environment :: Console
- Development Status :: 4 - Beta
- Intended Audience :: Developers
- Intended Audience :: System Administrators
- Topic :: Software Development
- License :: OSI Approved :: MIT License
- Programming Language :: Python
- Programming Language :: Python :: 3.8
- Programming Language :: Python :: 3.9
- Programming Language :: Python :: 3.10
- Programming Language :: Python :: 3.11
Select classifiers: 
Current console scripts:
- pypi-template=pypi_template.__main__:cli
Select console scripts: 
First year of publication: 2018
Github account: christophevg
Github repo name: pypi-template
Keywords describing the package: python pypi package management template
License: MIT
Package module name: pypi_template
Package name: pypi-template
Package tagline: Template-based common/best practices for managing a Python package on PyPi
Package title: PyPi Template
Readme: .github/README.md
Current requires:
- jinja2
- pyyaml
- prompt-toolkit
- colorama
- fire
- importlib-resources
Select requires: 
Select scripts: 
Current skip:
- MANIFEST.in
- tests
- docs
- (package_module_name)
Select skip: 
Your author name: Christophe VG
Your email address: contact@christophe.vg
Your full name: Christophe VG
Your name: Christophe VG
🔨 applying templates
✅ requirements.txt has no changes
✅ requirements.docs.txt has no changes
✅ Makefile has no changes
✅ .github/workflows/test.yaml has no changes
✅ .github/workflows/__init__.py has no changes
✅ .github/README.md has no changes
✅ .gitignore has no changes
⏭  skipping 'tests' due to skipped 'tests'
⏭  skipping MANIFEST.in
⏭  skipping 'docs' due to skipped 'docs'
⏭  skipping 'docs/_static' due to skipped 'docs'
✅ setup.py has no changes
⏭  skipping '(package_module_name)' due to skipped '(package_module_name)'
✅ tox.ini has no changes
✅ LICENSE.txt has no changes
🛑 not rendering excluded base/classifiers.txt
🛑 not rendering excluded base/index.md
✅ .readthedocs.yaml has no changes
```
