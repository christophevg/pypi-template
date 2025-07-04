import os
import re
import setuptools

NAME             = "pypi-template"
AUTHOR           = "Christophe VG"
AUTHOR_EMAIL     = "contact@christophe.vg"
DESCRIPTION      = "Template-based common/best practices for managing a Python package on PyPi"
LICENSE          = "MIT"
KEYWORDS         = "python pypi package management template"
URL              = "https://github.com/christophevg/" + NAME
README           = ".github/README.md"
CLASSIFIERS      = [
  "Environment :: Console",
  "Development Status :: 5 - Production/Stable",
  "Intended Audience :: Developers",
  "Intended Audience :: System Administrators",
  "Topic :: Software Development",
  "Programming Language :: Python",
  "Programming Language :: Python :: 3.9",
  "Programming Language :: Python :: 3.10",
  "Programming Language :: Python :: 3.11",
  "Programming Language :: Python :: 3.12",
  
]
INSTALL_REQUIRES = [
  "jinja2",
  "pyyaml",
  "prompt-toolkit",
  "colorama",
  "fire",
  "importlib-resources",
  "requests",
  "packaging",
  
]
ENTRY_POINTS = {
  "console_scripts" : [
    "pypi-template=pypi_template.__main__:cli",
    
  ]
}
SCRIPTS = [
  
]

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
  setuptools.setup(
    name=NAME,
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
    scripts=SCRIPTS,
    include_package_data=True    
  )
