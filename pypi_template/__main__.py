import os
import sys
import datetime

from pkg_resources import resource_string, resource_listdir, resource_isdir

from jinja2 import FileSystemLoader, Environment
from jinja2 import Template, Environment, meta

import yaml

from prompt_toolkit import prompt

from pypi_template import __version__

EXCLUDED_EXT = ".pyc"
EXCLUDED     = [ "__init__.py" ]

environment = Environment()
environment.keep_trailing_newline=True

def list_package(package="pypi_template.templates"):
  files = []
  for resource in resource_listdir(package, ""):
    if resource.endswith(EXCLUDED_EXT) or resource in EXCLUDED:
      pass
    elif resource_isdir(package, resource):
      files += [ os.path.join(resource, f) for f in list_package("{0}.{1}".format(package, resource)) ]
    else:
      files.append(resource)
  return files

def load(resource):
  return resource_string(__name__, os.path.join("templates", resource))

def list_variables(template):
  ast = environment.parse(template)
  return meta.find_undeclared_variables(ast)

# load variables cache
system_vars = {
  "current_year"          : datetime.datetime.now().year,
  "pypi_template_version" : __version__
}
try:    vars = yaml.safe_load(open(".pypi-template"))
except: pass
if vars is None: vars = {}

# collect templates from package, load and collect variables in them
files = {}
for f in dict((p, None) for p in list_package()):
  name = f.replace("(dot)", ".")
  files[name] = load(f)
  for var in list_variables(files[name]):
    if not var in vars and not var in system_vars: vars[var] = ""

# collect variable values
for var, current in vars.items():
  if current and "-y" in sys.argv: continue
  question = "{0}: ".format(var.replace("_", " ").capitalize())
  vars[var] = prompt(
    unicode(question, "utf-8"),
    default=unicode(current, "utf-8")
  )

# save new vars settings
with open(".pypi-template", "w") as outfile:
  yaml.safe_dump(vars, outfile, default_flow_style=False)

vars.update(system_vars)

# render all files
for f in files:
  if "skip" in vars and f in vars["skip"]:
    print("skipping {0}".format(f))
    continue
  print("writing {0}".format(f))
  directory = os.path.dirname(f)
  if directory != "" and not os.path.exists(directory): os.makedirs(directory)
  with open(f, "w") as outfile:
    outfile.write(environment.from_string(files[f]).render(**vars))
