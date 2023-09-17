# Contributing

This is Open Source software, so [given enough eyeballs, all bugs are shallow](https://en.wikipedia.org/wiki/Linus%27s_Law). Your contributions are more than welcome.

This project is hosted on [GitHub](https://githhub.com/christophevg/pypi-template) and these (common) rules apply:

* Do use the [issues tracker](https://githhub.com/christophevg/pypi-template/issues).
* Let's discuss any proposed change or fix in an issue, so your work is not done in vain - I hate to reject pull requests...
* Create [pull requests](https://githhub.com/christophevg/pypi-template/pulls) against `next` branch.
* Try to keep pull requests "atomic", and if possible related to an issue.
-
## My Development Workflow

I try to develop pypi-template in a self-hosting way, which means that I run it from the repository on the repository itself.

Running pypi-template from the repository can be done according to the following steps:

### Setup an Environment with Dependencies

I started using PyEnv recently and the top-level Makefile in the repository is using that. So if you go down the PyEnv road, you can use it ;-)

Minimal survival commands: 

[https://github.com/pyenv/pyenv#installation](https://github.com/pyenv/pyenv#installation)

```console
$ make requirements
pypi-template (set by /Users/xtof/Workspace/pypi-template/.python-version)
```

If you want to use a different virtual evironment manager, or none, simply issue the usual...

```console
$ pip install -r requirements.txt
```

### Running pypi-template from the Repository

```console
% python -m pypi_template verbose edit all apply
A description for the package: A managed template repository for PyPi packages
Current classifiers:
- Environment :: Console
- Development Status :: 4 - Beta
- Intended Audience :: Developers
- Intended Audience :: System Administrators
- Topic :: Software Development
- License :: OSI Approved :: MIT License
- Programming Language :: Python
- Programming Language :: Python :: 3.7
Select classifiers: 
Current console scripts:
- pypi-template=pypi_template.__main__:cli
Select console scripts: 
First year of publication: 2018
Github account: christophevg
Github repo name: pypi-template
Keywords describing the package: pypi template
License: MIT
Package module name: pypi_template
Package name: pypi-template
Package tagline: A managed template repository for maintaining PyPi packages
Package title: PyPi Template
Current requires:
- jinja2
- pyyaml
- prompt-toolkit
- colorama
- fire
Select requires: 
Select scripts: 
Current skip:
- MANIFEST.in
- docs
- tests
- (package_module_name)
Select skip: 
Your author name: Christophe VG
Your email address: contact@christophe.vg
Your full name: Christophe Van Ginneken
Your name: Christophe VG
✅ requirements.txt has no changes
✅ Makefile has no changes
✅ .github/README.md has no changes
✅ .gitignore has no changes
⏭ skipping tests/test_example.py
⏭ skipping MANIFEST.in
⏭ skipping docs/Makefile
⏭ skipping docs/conf.py
⏭ skipping docs/whats-in-the-box.md
✅ docs/_static/.gitignore has no changes
⏭ skipping docs/getting-started.md
⏭ skipping docs/make.bat
⏭ skipping docs/index.md
⏭ skipping docs/contributing.md
⏭ skipping docs/code.md
✅ setup.py has no changes
⏭ skipping (package_module_name)/module.py
✅ tox.ini has no changes
✅ LICENSE.txt has no changes
✅ .travis.yml has no changes
🛑 not rendering excluded base/classifiers.txt
🛑 not rendering excluded base/index.md
```