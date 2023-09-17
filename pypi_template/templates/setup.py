import os
import re
import setuptools

NAME             = "{{ package_name }}"
AUTHOR           = "{{ your_name }}"
AUTHOR_EMAIL     = "{{ your_email_address }}"
DESCRIPTION      = "{{ a_description_for_the_package }}"
LICENSE          = "{{ license }}"
KEYWORDS         = "{{ keywords_describing_the_package }}"
URL              = "https://github.com/{{ github_account }}/" + NAME
README           = "{{ readme }}"
CLASSIFIERS      = [
  {% for classifier in classifiers %}"{{ classifier }}",
  {% endfor %}
]
INSTALL_REQUIRES = [
  {% for required in requires %}"{{ required }}",
  {% endfor %}
]
ENTRY_POINTS = {
  {% if console_scripts %}"console_scripts" : [
    {% for script in console_scripts %}"{{ script }}",
    {% endfor %}
  ]{% endif %}
}
SCRIPTS = [
  {% if scripts %}{% for script in scripts %}"{{ script }}",
  {% endfor %}{% endif %}
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
