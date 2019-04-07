import os
import re
import setuptools

NAME             = "{{ package_name }}"
AUTHOR           = "Christophe VG"
AUTHOR_EMAIL     = "{{ your_email_address }}"
DESCRIPTION      = "{{ a_description_for_the_package }}"
LICENSE          = "MIT"
KEYWORDS         = "{{ keywords_describing_the_package }}"
URL              = "https://github.com/{{ github_account }}/" + NAME
README           = ".github/README.md"
CLASSIFIERS      = [
  "Environment :: Console",
  "Development Status :: 4 - Beta",
  "Intended Audience :: Developers",
  "Intended Audience :: System Administrators",
  "Topic :: Software Development",
  "License :: OSI Approved :: MIT License",
  "Programming Language :: Python",
  "Programming Language :: Python :: 2.7",
  "Programming Language :: Python :: 3.7",
]
INSTALL_REQUIRES = []
ENTRY_POINTS     = {}
SCRIPTS          = []

HERE = os.path.dirname(__file__)

def read(file):
  with open(os.path.join(HERE, file), "r") as fh:
    return fh.read()

VERSION = re.search(
  r'__version__ = [\'"]([^\'"]*)[\'"]',
  read(NAME.replace("-", "_") + "/__init__.py")
).group(1)

LONG_DESCRIPTION = read(README)

if __name__ == "__main__":
  setuptools.setup(name=NAME,
        version=VERSION,
        packages=setuptools.find_packages(),
        author=AUTHOR,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        license=LICENSE,
        keywords=KEYWORDS,
        url=URL,
        classifiers=CLASSIFIERS,
        install_requires=INSTALL_REQUIRES,
        entry_points=ENTRY_POINTS,
        scripts=SCRIPTS)
