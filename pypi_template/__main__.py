import os
import datetime
import argparse

from pkg_resources import resource_string, resource_listdir, resource_isdir

from jinja2 import Environment, PackageLoader, meta

import yaml

from prompt_toolkit.completion import FuzzyWordCompleter
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style
from colorama import init, Fore

from pypi_template import __version__

style = Style.from_dict({ "underlined": "underline" })
init(autoreset=True)

class CLI():

  def __init__(self, path=None, verbose=False, debug=False, edit=None, yes=False):
    if not path is None:
      os.chdir(path)
    self.be_verbose = verbose
    self.show_debug = debug
    self.edit       = edit
    self.yes        = yes
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

  def verbose(self, msg):
    if self.be_verbose or self.show_debug:
      print(msg)

  def load_classifiers(self):
    return str(
      self.load_resource("base", "classifiers.txt"), "utf-8"
    ).split("\n")

  def load_resource(self, *args):
    return resource_string(__name__, os.path.join("templates", *args))

  def list_resources(self, package="pypi_template.templates"):
    excluded_ext = ".pyc"
    excluded     = [ "__init__.py", "__pycache__" ]
    files = []
    for resource in resource_listdir(package, ""):
      if resource.endswith(excluded_ext) or resource in excluded:
        pass
      elif resource_isdir(package, resource):
        subfiles = self.list_resources(f"{package}.{resource}")
        files += [ os.path.join(resource, f) for f in subfiles ]
      else:
        files.append(resource)
    return files

  def load_vars(self):
    try:
      with open(".pypi-template", encoding="utf-8") as fp:
        self.template_vars = yaml.safe_load(fp)
    except:
      pass

  def collect_templates(self):
    for resource in self.list_resources():
      name = resource.replace("(dot)", ".")
      self.templates[name] = self.environment.get_template(resource)
      # extract template variables
      source = self.load_resource(resource)
      for var in meta.find_undeclared_variables(self.environment.parse(source)):
        self.verbose(f"found variable {name} : {var}")
        if not var in self.template_vars and not var in self.system_vars:
          self.template_vars[var] = None

  def collect_all_vars(self):
    for var in sorted(self.template_vars.keys()):
      self.collect_var(var)

  def collect_var(self, var, force=False):
    try:
      current = self.template_vars[var]
      if not force and not current is None and self.yes:
        return
      if var in self.list_vars:
        self.collect_var_selections(var, current)
      else:
        self.collect_var_value(var, current)
    except KeyError:
      print(f"unknown template variable: {var}")

  def collect_var_value(self, var, current):
    question = f"{var.replace('_', ' ').capitalize()}: "
    if current is None:
      current = ""
    self.template_vars[var] = prompt(
      [("class:underlined", question)], style=style, default=current
    )

  def collect_var_selections(self, var, current=None):
    if not current:
      current = []
    if len(current) > 0:
      print(Fore.BLUE + f"Current {var.replace('_', ' ')}:")
      for selection in current:
        print(Fore.BLUE + f"- {selection}")
    question = f"Select {var.replace('_', ' ')}: "
    values   = self.list_vars[var]
    if values:
      completer = FuzzyWordCompleter(values)
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
    with open(".pypi-template", "w", encoding="utf-8") as outfile:
      yaml.safe_dump(self.template_vars, outfile, default_flow_style=False)

  def render_files(self):
    excluded = [ "base/index.md", "base/classifiers.txt" ]
    for filename, template in self.templates.items():
      if filename in excluded:
        self.verbose(f"not rendering excluded {filename}")
        continue
      directory = os.path.dirname(filename)
      if "skip" in self.template_vars:
        if filename in self.template_vars["skip"] or directory in self.template_vars["skip"]:
          self.verbose(f"skipping {filename}")
          continue
      # TODO generalize?
      filename = filename.replace(
        "(package_module_name)", self.template_vars["package_module_name"]
      )
      directory = os.path.dirname(filename)
      if directory != "" and not os.path.exists(directory):
        self._mkdir(directory)
      applied_vars = self.template_vars.copy()
      applied_vars.update(self.system_vars)
      new_content = template.render(**applied_vars)
      if os.path.isfile(filename):
        with open(filename, encoding="utf-8") as file:
          original_content = file.read()
        if new_content == original_content:
          self.verbose(f"unchanged {filename}")
          continue
        self._backup(filename)
      self._write_file(filename, new_content)

  def _mkdir(self, directory):
    if self.show_debug:
      print(f"not really creating directory {directory}")
    else:
      self.verbose(f"creating directory {directory}")
      os.makedirs(directory)
      # TODO generalize?
      if directory == self.template_vars["package_module_name"]:
        with open(os.path.join(directory, "__init__.py"), "w", encoding="utf-8") as fp:
          fp.write('__version__ = "0.0.1"')

  def _backup(self, filename):
    if self.show_debug:
      print(f"not really backing up {filename}")
    else:
      self.verbose(f"backing up {filename}")
      os.rename(filename, filename + ".backup")

  def _write_file(self, filename, new_content):
    if self.show_debug:
      print(f"not really writing {filename}")
    else:
      self.verbose(f"writing {filename}")
      with open(filename, "w", encoding="utf-8") as outfile:
        outfile.write(new_content)

  def run(self):
    try:
      self.load_vars()
      self.collect_templates()
      if not self.edit is None:
        self.collect_var(self.edit, force=True)
      else:
        self.collect_all_vars()
      self.save_var_values()
      self.render_files()
    except KeyboardInterrupt:
      pass

def cli():
  parser = argparse.ArgumentParser(description="Manage a Python PyPi package.")
  parser.add_argument("path", type=str, nargs="?",
                      help="path to module (default=current)")
  parser.add_argument("--edit",    "-e", dest="edit",
                      help="edit a variable")
  parser.add_argument("--yes",     "-y", dest="yes",     action="store_true",
                      help="accept all current variable values")
  parser.add_argument("--debug",   "-d", dest="debug",   action="store_true",
                      help="don't do it, just say it")
  parser.add_argument("--verbose", "-v", dest="verbose", action="store_true",
                      help="do it and say it")
  parser.add_argument("--version", dest="version", action="store_true",
                      help="show version")

  args = parser.parse_args()
  if args.version:
    print(__version__)
  else:
    CLI(**vars(args)).run()

if __name__ == "__main__":
  cli()
