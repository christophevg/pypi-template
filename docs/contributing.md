# Contributing

This is Open Source software, so [given enough eyeballs, all bugs are shallow](https://en.wikipedia.org/wiki/Linus%27s_Law). Your contributions are more than welcome.

This project is hosted on [GitHub](https://githhub.com/christophevg/pypi-template) and these (common) rules apply:

* Do use the [issues tracker](https://githhub.com/christophevg/pypi-template/issues).
* Let's discuss any proposed change or fix in an issue, so your work is not done in vain - I hate to reject pull requests...
* Create [pull requests](https://githhub.com/christophevg/pypi-template/pulls) against `next` branch.
* Try to keep pull requests "atomic", and if possible related to an issue.

## My Development Workflow

I try to develop pypi-template in a self-hosting way, which means that I run it on its own repository.

Running pypi-template from the repository can be done according to the following steps:

### Setup an Environment with Dependencies

```bash
$ make venv
virtualenv -p python3 venv
Running virtualenv with interpreter /Library/Frameworks/Python.framework/Versions/3.5/bin/python3
Using base prefix '/Library/Frameworks/Python.framework/Versions/3.5'
New python executable in /Users/xtof/Workspace/pypi-template/venv/bin/python3
Also creating executable in /Users/xtof/Workspace/pypi-template/venv/bin/python
Installing setuptools, pip, wheel...
done.

$ make requirements
. venv/bin/activate; pip install --upgrade -r requirements.txt > /dev/null 
```

### Running pypi-template from the Repository

```bash
$ . venv/bin/activate

(venv) $ python -m pypi_template
A description for the package: A managed template repository for PyPi packages
Current classifiers:
- Environment :: Console
- Development Status :: 4 - Beta
- Intended Audience :: Developers
- System Intended Audience :: System Administrators
- Topic :: Topic :: Software Development
- MIT License :: OSI Approved :: MIT License
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
Package module name: pypi_template
Package name: pypi-template
Package tagline: A managed template repository for maintaining PyPi packages
Package title: PyPi Template
Current requires:
- jinja2
- pyyaml
- prompt-toolkit
- colorama
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
backing up LICENSE.txt
writing LICENSE.txt
skipping docs/getting-started.md
skipping docs/contributing.md
skipping docs/Makefile
skipping MANIFEST.in
skipping docs/whats-in-the-box.md
skipping tests/test_example.py
skipping docs/make.bat
skipping docs/conf.py
skipping (package_module_name)/module.py
skipping docs/code.md
skipping docs/index.md
```
