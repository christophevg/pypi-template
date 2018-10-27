import codecs
import os
import re
from setuptools import find_packages
from setuptools import setup

NAME             = "pypi-template"
AUTHOR           = "Christophe VG"
AUTHOR_EMAIL     = "contact@christophe.vg"
DESCRIPTION      = "PyPi template repository."
LICENSE          = "MIT"
KEYWORDS         = "pypi template"
URL              = "https://github.com/christophevg/" + NAME
LONG_DESCRIPTION = "See " + URL
CLASSIFIERS      = [
  "Environment :: Console",
  "Development Status :: 4 - Beta",
  "Intended Audience :: Developers",
  "Intended Audience :: System Administrators",
  "Topic :: Software Development",
  "License :: OSI Approved :: MIT License",
  "Programming Language :: Python",
  "Programming Language :: Python :: 2",
  "Programming Language :: Python :: 2.6",
  "Programming Language :: Python :: 2.7",
  "Programming Language :: Python :: 3",
  "Programming Language :: Python :: 3.3",
  "Programming Language :: Python :: 3.4",
  "Programming Language :: Python :: 3.5",
  "Programming Language :: Python :: 3.6",
]
INSTALL_REQUIRES = []
ENTRY_POINTS     = {}

HERE = os.path.dirname(__file__)
def read(*path):
  with codecs.open(os.path.join(HERE, *path), encoding="utf-8") as fp:
    return fp.read()

VERSION = re.search(
  r'^__version__ = [\'"]([^\'"]*)[\'"]',
  read(NAME + "/__init__.py")
).group(1)

if __name__ == "__main__":
  setup(name=NAME,
        version=VERSION,
        packages=find_packages(),
        author=AUTHOR,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        license=LICENSE,
        keywords=KEYWORDS,
        url=URL,
        classifiers=CLASSIFIERS,
        install_requires=INSTALL_REQUIRES,
        entry_points=ENTRY_POINTS)
