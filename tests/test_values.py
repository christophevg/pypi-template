from pathlib import Path
import os.path
from datetime import datetime

from pypi_template import PyPiTemplate, __version__

def test_version():
  assert PyPiTemplate().version == __version__

def test_variables():
  assert PyPiTemplate().variables == [
    "a_description_for_the_package",
    "classifiers",
    "console_scripts",
    "first_year_of_publication",
    "github_account",
    "github_repo_name",
    "keywords_describing_the_package",
    "license",
    "package_module_name",
    "package_name",
    "package_tagline",
    "package_title",
    "project_env",
    "readme",
    "requires",
    "scripts",
    "skip",
    "test_requires",
    "your_author_name",
    "your_email_address",
    "your_full_name",
    "your_name"
  ]

def test_defaults(monkeypatch):
  def mockreturn(_):
    return Path(__file__).resolve().parent / "home" / ".pypi-template"
  monkeypatch.setattr(os.path, "expanduser", mockreturn)
  
  assert PyPiTemplate().defaults == {
    "readme": ".github/README.md",
    "first_year_of_publication": str(datetime.now().year),
    "your_author_name": "Christophe VG",
    "your_full_name": "Christophe VG",
    "your_name": "Christophe VG",
    "github_account": "christophevg",
    "license": "MIT",
    'project_env': ""
  }
