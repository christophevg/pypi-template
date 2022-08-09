# Known Issues

This is (hopefully a small) list of issues encountered while using PyPi Template that aren't solved yet.

## Publishing to PyPi Fails

```console
$ make publish-test
python setup.py sdist bdist_wheel
usage: setup.py [global_opts] cmd1 [cmd1_opts] [cmd2 [cmd2_opts] ...]
   or: setup.py --help [cmd1 cmd2 ...]
   or: setup.py --help-commands
   or: setup.py cmd --help

error: invalid command 'bdist_wheel'
make: *** [dist] Error 1
```

### Solution

From [https://stackoverflow.com/questions/34819221/why-is-python-setup-py-saying-invalid-command-bdist-wheel-on-travis-ci](https://stackoverflow.com/questions/34819221/why-is-python-setup-py-saying-invalid-command-bdist-wheel-on-travis-ci)

```console
$ pip install wheel
Collecting wheel
  Downloading wheel-0.35.1-py2.py3-none-any.whl (33 kB)
Installing collected packages: wheel
Successfully installed wheel-0.35.1
```

## DocUtils is pinned to 0.16

This is due to an incompatible issue in recommonmark. See [https://github.com/sphinx-doc/sphinx/issues/9049](https://github.com/sphinx-doc/sphinx/issues/9049) for more info. 

I'll try to fix this ... in the near future ;-)
