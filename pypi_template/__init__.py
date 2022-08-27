__version__ = "0.2.0"

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

style = Style.from_dict({ "underlined": "underline" })
init(autoreset=True)

class PyPiTemplate():

  """
  allows you to manage your PyPi-published Python project.
  
  It is essentially a set of templates, which you can customise using several
  variables. The variables are stored in a file called `.pypi-template` in the 
  root of the project. You can edit this file directly, or use the `edit`
  command to do it in an interactive way.
  
  Several commands can be issues at the same time. These are chainable commands
  and are as such indicated in the help description of each command.

  To actually `apply` your changes, end your sequence of commands with `apply`.
  
  Examples of usage:
  
      % pypi-template init           # to setup your project initially
      % pypi-template apply          # e.g. after an upgrade of pypi-template
      % pypi-template edit requires  # to add an additional dependency
  """
  
  def __init__(self):
    # operational setup
    self._started        = False
    self._be_verbose     = False
    self._show_debug     = False
    self._say_yes_to_all = False
  
    # setup Jinja Template Engine
    self._environment = Environment(
      loader=PackageLoader("pypi_template", "templates")
    )
    self._environment.keep_trailing_newline=True

    # substitution/template variables
    self._system_vars = {
      "now"                   : datetime.datetime.now().isoformat(),
      "current_year"          : datetime.datetime.now().year,
      "pypi_template_version" : __version__
    }
    self._var_lists = {
      "classifiers"     : self._load_classifiers(),
      "requires"        : None,
      "console_scripts" : None,
      "scripts"         : None,
      "skip"            : None
    }
    self._template_vars = {}
    self._templates     = {}
    self._changes        = {}
    
  # fire default output
  
  def __str__(self):
    if self._changes:
      return f"unapplied changes:\n{yaml.dump(self._changes)}"
    else:
      return ""

  # operational setup

  def verbose(self):
    """
    Explain everything that is done. (chainable)
    """
    self._be_verbose = True
    return self

  def _being_verbose(self, msg):
    if self._be_verbose or self._show_debug:
      print(msg)
      return True
    return False

  def debug(self):
    """
    Don't actually do it, but tell what would have been done. (chainable)
    """
    self._show_debug = True
    return self

  def _debugging(self, msg):
    if self._show_debug:
      print(msg)
      return True
    return False

  def _going_to(self, msg):
    prefix = ""
    # leading whitespace + icon
    while msg.startswith(" ") or msg[1] == " ":
      prefix += msg[0]
      msg = msg[1:]
    if not self._debugging(f"{prefix}not really {msg}"):
      self._being_verbose(f"{prefix}{msg}")
      return True
    return False

  def yes(self):
    """
    Accept all previous values for variables. Only not yet initialized variables
    need handling. (chainable)
    """
    self._say_yes_to_all = True
    return self

  # commands

  def version(self):
    """
    Output PyPiTemplate's version.
    """
    print(__version__)

  def path(self, p):
    """
    Set the path to the provided one. Defaults to the current working directory.
    (chainable)
    """
    os.chdir(p)
    return self

  def init(self):
    """
    Initialize a fresh project.
    """
    self.edit("all")
    self.apply()

  def variables(self):
    """
    Returns a list of all available template variables you can edit.
    """
    self._start()
    return list(self._template_vars.keys()) + list(self._var_lists.keys())

  def edit(self, variable):
    """
    Edit a variable (or provide "all") and apply the change. (chainable)
    """
    self._start()
    if variable == "all":
      self._collect_all_vars()
    else:
      self._collect_var(variable, force=True)

    return self

  def apply(self):
    """
    Apply the currently registered configuration.
    """
    self._start()
    self._save_var_values()
    self._render_files()

  # helper functions
  
  def _load_classifiers(self):
    return str(
      self._load_resource("base", "classifiers.txt"), "utf-8"
    ).split("\n")

  def _load_resource(self, *args):
    return resource_string(__name__, os.path.join("templates", *args))

  def _list_resources(self, package="pypi_template.templates"):
    excluded_ext = ".pyc"
    excluded     = [
      "__pycache__",
      "pypi_template.templates.__init__.py",
      "pypi_template.templates.(dot)github.__init__.py",
      "pypi_template.templates.base.__init__.py",
      "pypi_template.templates.docs._static.__init__.py"
    ]
    files = []
    for resource in resource_listdir(package, ""):
      if resource.endswith(excluded_ext) or \
         resource in excluded or \
         f"{package}.{resource}" in excluded:
        pass
      elif resource_isdir(package, resource):
        subfiles = self._list_resources(f"{package}.{resource}")
        files += [ os.path.join(resource, f) for f in subfiles ]
      else:
        files.append(resource)
    return files

  def _start(self):
    if not self._started:
      self._load_vars()
      self._collect_templates()
      self._started = True

  def _load_vars(self):
    try:
      with open(".pypi-template", encoding="utf-8") as fp:
        self._template_vars = yaml.safe_load(fp)
    except:
      pass

  def _collect_templates(self):
    for resource in self._list_resources():
      name = resource.replace("(dot)", ".")
      self._templates[name] = self._environment.get_template(resource)
      # extract template variables
      source = self._load_resource(resource)
      for var in meta.find_undeclared_variables(self._environment.parse(source)):
        self._debugging(f"🔎 found variable in {name} : {var}")
        if not var in self._template_vars and not var in self._system_vars:
          self._template_vars[var] = None

  def _collect_all_vars(self):
    for var in sorted(self._template_vars.keys()):
      self._collect_var(var)

  def _collect_var(self, var, force=False):
    try:
      current = self._template_vars[var]
      if not force and not current is None and self._say_yes_to_all:
        return
      if var in self._var_lists:
        self.__collect_var_selections(var, current)
      else:
        self.__collect_var_value(var, current)
      if self._template_vars[var] != current:
        self._changes[var] = {
          "old" : current,
          "new" : self._template_vars[var]
        }
    except KeyError:
      print(f"🚨 unknown template variable: {var}")

  def __collect_var_value(self, var, current):
    question = f"{var.replace('_', ' ').capitalize()}: "
    if current is None:
      current = ""
    self._template_vars[var] = prompt(
      [("class:underlined", question)], style=style, default=current
    )

  def __collect_var_selections(self, var, current=None):
    if not current:
      current = []
    if len(current) > 0:
      print(Fore.BLUE + f"Current {var.replace('_', ' ')}:")
      for selection in current:
        print(Fore.BLUE + f"- {selection}")
    question = f"Select {var.replace('_', ' ')}: "
    values   = self._var_lists[var]
    if values:
      completer = FuzzyWordCompleter(values)
    selections = list(current)
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
    self._template_vars[var] = selections
    

  def _save_var_values(self):
    if self._changes:
      if self._going_to(f"💾 saving variables"):
        with open(".pypi-template", "w", encoding="utf-8") as outfile:
          yaml.safe_dump(self._template_vars, outfile, default_flow_style=False)
    self.changes = {}

  def _render_files(self):
    excluded = [ "base/index.md", "base/classifiers.txt" ]
    for filename, template in self._templates.items():
      if filename in excluded:
        self._being_verbose(f"🛑 not rendering excluded {filename}")
        continue
      directory = os.path.dirname(filename)
      if "skip" in self._template_vars:
        if filename in self._template_vars["skip"] or directory in self._template_vars["skip"]:
          self._being_verbose(f"⏭  skipping {filename}")
          continue
      # TODO generalize?
      filename = filename.replace(
        "(package_module_name)", self._template_vars["package_module_name"]
      )
      directory = os.path.dirname(filename)
      if directory != "" and not os.path.exists(directory):
        self._mkdir(directory)
      applied_vars = self._template_vars.copy()
      applied_vars.update(self._system_vars)
      new_content = template.render(**applied_vars)
      if os.path.isfile(filename):
        with open(filename, encoding="utf-8") as file:
          original_content = file.read()
        if new_content == original_content:
          self._being_verbose(f"✅ {filename} has no changes")
          continue
        self._being_verbose(f"✍️  {filename} was changed")
        self._backup(filename)
      self._write_file(filename, new_content)

  def _mkdir(self, directory):
    if self._going_to(f"📁 creating directory {directory}"):
      os.makedirs(directory)

  def _backup(self, filename):
    if self._going_to(f"   💾 backing up {filename}"):
      os.rename(filename, filename + ".backup")

  def _write_file(self, filename, new_content):
    if self._going_to(f"   💾 writing {filename}"):
      with open(filename, "w", encoding="utf-8") as outfile:
        outfile.write(new_content)

def cli():
  try:
    Fire(PyPiTemplate(), name="pypi-template")
  except KeyboardInterrupt:
    pass

if __name__ == "__main__":
  cli()
