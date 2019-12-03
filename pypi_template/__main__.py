import os
import sys
import datetime

from pkg_resources import resource_string, resource_listdir, resource_isdir

from jinja2 import Environment, PackageLoader, meta

import yaml

from prompt_toolkit.completion import FuzzyWordCompleter
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style

style = Style.from_dict({
  "underlined": "underline"
})

from colorama import init, Fore
init(autoreset=True)

from pypi_template import __version__

class CLI(object):
  def __init__(self):
    self.environment = Environment(
      loader=PackageLoader("pypi_template", "templates")
    )
    self.environment.keep_trailing_newline=True
    self.system_vars = {
      "current_year"          : datetime.datetime.now().year,
      "pypi_template_version" : __version__
    }
    self.list_vars = {
      "classifiers"     : self.load_classifiers(),
      "requires"        : None,
      "console_scripts" : None,
      "scripts"         : None,
      "skip"            : None
    }
    self.template_vars = {}
    self.templates     = {}

  def load_classifiers(self):
    return str(
      self.load_resource("base", "classifiers.txt"), "utf-8"
    ).split("\n")

  def load_resource(self, *args):
    return resource_string(__name__, os.path.join("templates", *args))

  def list_resources(self, package="pypi_template.templates"):
    EXCLUDED_EXT = ".pyc"
    EXCLUDED     = [ "__init__.py", "__pycache__", "base" ]
    files = []
    for resource in resource_listdir(package, ""):
      if resource.endswith(EXCLUDED_EXT) or resource in EXCLUDED:
        pass
      elif resource_isdir(package, resource):
        subfiles = self.list_resources("{0}.{1}".format(package, resource))
        files += [ os.path.join(resource, f) for f in subfiles ]
      else:
        files.append(resource)
    return files

  def load_vars(self):
    try:    self.template_vars = yaml.safe_load(open(".pypi-template"))
    except: pass

  def collect_templates(self):
    for resource in self.list_resources():
      name = resource.replace("(dot)", ".")
      self.templates[name] = self.environment.get_template(resource)
      # extract template variables
      source = self.load_resource(resource) 
      for var in meta.find_undeclared_variables(self.environment.parse(source)):
        if not var in self.template_vars and not var in self.system_vars:
          self.template_vars[var] = None

  def collect_all_vars(self):
    for var in sorted(self.template_vars.keys()):
      self.collect_var(var)

  def collect_var(self, var, force=False):
    try:
      current = self.template_vars[var]
      if not force and not current is None and "-y" in sys.argv: return
      if var in self.list_vars:
        self.collect_var_selections(var, current)
      else:
        self.collect_var_value(var, current)
    except KeyError:
      print("unknown template variable: {0}".format(var))

  def collect_var_value(self, var, current):
    question = "{0}: ".format(var.replace("_", " ").capitalize())
    if current is None: current = ""
    self.template_vars[var] = prompt(
      [("class:underlined", question)], style=style, default=current
    )

  def collect_var_selections(self, var, current=[]):
    if not current: current = []
    if len(current) > 0:
      print(Fore.BLUE + "Current {}:".format(var.replace("_", " ")))
      for selection in current:
        print(Fore.BLUE + "- {0}".format(selection))
    question = "Select {0}: ".format(var.replace("_", " "))
    values   = self.list_vars[var]
    if values: completer = FuzzyWordCompleter(values)
    selections = current
    selection = None
    while selection != "":
      if values:
        selection = prompt(
          [("class:underlined", question)],
          style=style, 
          completer=completer,
          complete_while_typing=True
        )
      else:
        selection = prompt([("class:underlined", question)], style=style)
      if selection != "":
        if not selection in selections:
          selections.append(selection)
    self.template_vars[var] = selections

  def save_var_values(self):
    with open(".pypi-template", "w") as outfile:
      yaml.safe_dump(self.template_vars, outfile, default_flow_style=False)

  def render_files(self):
    for filename, template in self.templates.items():
      if "skip" in self.template_vars and filename in self.template_vars["skip"]:
        print("skipping {0}".format(filename))
        continue
      # TODO generalize?
      filename = filename.replace(
        "(package_module_name)", self.template_vars["package_module_name"]
      )
      directory = os.path.dirname(filename)
      if directory != "" and not os.path.exists(directory):
        os.makedirs(directory)
        # TODO generalize?
        if directory == self.template_vars["package_module_name"]:
          with open(os.path.join(directory, "__init__.py"), "w") as f:
            f.write('__version__ = "0.0.1"')
      vars = self.template_vars.copy()
      vars.update(self.system_vars)
      new_content = template.render(**vars)
      if os.path.isfile(filename):
        with open(filename, "r") as file: original_content = file.read()
        if new_content == original_content: continue
        print("backing up {0}".format(filename))
        os.rename(filename, filename + ".backup")
      print("writing {0}".format(filename))
      with open(filename, "w") as outfile: outfile.write(new_content)

  def run(self):
    try:
      self.load_vars()
      self.collect_templates()
      if "-e" in sys.argv:
        var = sys.argv[sys.argv.index("-e") + 1]
        self.collect_var(var, force=True)
      else:
        self.collect_all_vars()
      self.save_var_values()
      self.render_files()
    except KeyboardInterrupt:
      pass

def cli():
  CLI().run()

if __name__ == "__main__":
  cli()
