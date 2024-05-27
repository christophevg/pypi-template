__version__ = "0.6.0"

import os
import datetime

import importlib_resources

from jinja2 import Environment, PackageLoader, meta

import json
import yaml

from prompt_toolkit.completion import FuzzyWordCompleter
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style
from colorama import init, Fore

import subprocess

import requests
from packaging import version as packaging_version

style = Style.from_dict({ "underlined": "underline" })
init(autoreset=True)

class PyPiTemplate():

  """
  manage a PyPi-published Python project using templates.
  
  It is essentially a set of templates, which you can customise using several
  variables. The variables are stored in a file called `.pypi-template` in the 
  root of the project. You can edit this file directly, or use the `edit`
  command to do it in an interactive way.
  
  Several commands can be issued at the same time. These are chainable commands
  and are as such indicated in the help description of each command.

  To actually `apply` your changes, end your sequence of commands with `apply`.
  
  Examples of usage:
  
      % pypi-template init           # to setup your project initially
      % pypi-template apply          # e.g. after an upgrade of pypi-template
      % pypi-template edit requires  # to add an additional dependency
      % pypi-template yes edit all   # to edit any new variables
  """
  
  def __init__(self):
    # operational setup
    self._be_verbose     = False
    self._show_debug     = False
    self._say_yes_to_all = False
    self._as_json        = False
  
    # setup Jinja Template Engine
    self._environment = Environment(
      loader=PackageLoader("pypi_template", "templates")
    )
    self._environment.keep_trailing_newline = True

    # default, not exposed, system-style dynamic variables
    self._system_vars = {
      "now"                   : datetime.datetime.now().isoformat(),
      "current_year"          : str(datetime.datetime.now().year),
      "pypi_template_version" : __version__
    }
    # substitution/template variables that are lists, not single values
    self._var_lists = {
      "classifiers"     : self._load_classifiers(),
      "requires"        : None,
      "console_scripts" : None,
      "scripts"         : None,
      "skip"            : None
    }
    # key/value substitution/template variables
    self._template_vars  = {}

    # system vars that are in the .pypi-template
    self._system_template_vars = {
      "version" : __version__
    }

    # all templates
    self._templates      = {}
    
    # tracking changes applied to _template_vars
    self._changes        = {}

    # default default values
    self._default_values = {
      "readme"                    : ".github/README.md",
      "first_year_of_publication" : self._system_vars["current_year"],
    }
    
    # load personal default values, saved variables (from .pypi-template)
    # and discover all templates and variables that have been used on them
    self._load_personal_default_values()
    self._load_vars()
    self._collect_templates()
    
  # fire default output - if there are unapplied changes, notify them when
  # exiting - and thus losing them
  def __str__(self):
    if self._changes:
      return f"unapplied changes:\n{yaml.dump(self._changes)}"
    else:
      return ""

  # operational setup commands

  def verbose(self):
    """
    Explain everything that is done. (chainable)
    """
    self._be_verbose = True
    return self

  def debug(self):
    """
    Don't actually do it, but tell what would have been done. (chainable)
    """
    self._show_debug = True
    return self

  def yes(self):
    """
    Accept all previous values for variables. Only not yet initialized variables
    need handling. (chainable)
    """
    self._say_yes_to_all = True
    return self

  def json(self):
    """
    Format output as a JSON string
    """
    self._as_json = True
    return self

  # values

  @property
  def version(self):
    """
    Output PyPiTemplate's version.
    """
    return self._out(__version__)

  @property
  def variables(self):
    """
    Return a list of all available template variables you can edit.
    """
    return self._out(
      sorted(list(self._template_vars.keys()) + list(self._var_lists.keys()))
    )

  @property
  def defaults(self):
    """
    Return a list of all default template variables values.
    """
    return self._out(self._default_values)

  @property
  def uninitialized(self):
    """
    Return a list of template variables that don't have a value yet.
    """
    return self._out([ key for key in self.variables if self[key] is None ])

  # commands

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
    if self._going_to("👷‍♂️ performing post-init install (e.g. environments)"):
      subprocess.run(["make", "install"])

  def edit(self, variable):
    """
    Edit a variable (or provide "all") and apply the change. (chainable)
    """
    if variable == "all":
      self._collect_all_vars()
    else:
      self._collect_var(variable, force=True)

    return self

  def ignore(self, target):
    """
    Add a target to the list of skipped paths (folders recursively) (chainable)
    """
    self._being_verbose(f"🔎 ignoring {target}")
    self._append("skip", target)
    return self

  def apply(self):
    """
    Apply the currently registered configuration.
    """
    self.save()
    self._render_files()

  def save(self):
    """
    Save the current set of variables to `.pypi-template` (chainable)
    """
    if self._changes:
      if self._going_to("💾 saving variables"):
        with open(".pypi-template", "w", encoding="utf-8") as outfile:
          yaml.safe_dump(
            {**self._template_vars, **self._system_template_vars},
            outfile, default_flow_style=False
          )
      self._changes = {}
    return self

  def status(self):
    """
    Perform a few sanity checks (chainable)
    """
    if all([
      self._check_pypi_version(),
      self._check_uninitialized_variables(),
      self._check_config_version()
    ]):
      print("😎 everyhing is OK")
    return self

  # helper functions
  
  def _check_pypi_version(self):
    # notify of newer version
    response = requests.get("https://pypi.org/pypi/pypi-template/json")
    latest_version = response.json()['info']['version']
    if packaging_version.parse(self.version) < packaging_version.parse(latest_version):
      print(f"🚨 a newer version of pypi-template ({latest_version}) is available")
      print( "   👉 issue 'pip install -U pypi-template' to upgrade!")
      return False
    return True

  def _check_uninitialized_variables(self):
    # notify of uninitialized variables
    if self.uninitialized:
      plural = "s" if len(self.uninitialized) > 1 else ""
      print(f"🚨 uninitialized template variable{plural}: {', '.join(self.uninitialized)}")
      print( "   👉 issue 'yes edit all apply' to fix!")
      return False
    return True

  def _check_config_version(self):
    # notify if version in config isn't current
    config_version = self._system_template_vars["version"]
    if config_version != self.version:
      print(f"🚨 pypi-template config version {config_version} != {self.version}")
      print( "   👉 issue 'save' to update!")
      return False
    return True

  # template vars are items of self

  def __getitem__(self, key):
    try:
      return self._template_vars[key]
    except KeyError:
      pass
    return None

  def __setitem__(self, var, value):
    current = self[var]
    if value != current:
      self._debugging(f"👉 recording change {current} -> {value}")
      self._template_vars[var] = value
      self._changes[var] = {
        "old" : current,
        "new" : value
      }

  def __delitem__(self, key):
    del self._template_vars[key]

  # variables helpers

  def _load_vars(self):
    try:
      with open(".pypi-template", encoding="utf-8") as fp:
        self._template_vars = yaml.safe_load(fp)
      self._debugging("💾 loaded .pypy-template")
      for key, value in self._template_vars.items():
        self._debugging(f"  {key} = {value} {'⚙️' if key in self._system_template_vars else ''}")
      # move the version to the system_template_vars
      # since it isn't a real (template) var
      for key in self._system_template_vars.keys():
        self._system_template_vars[key] = self._template_vars.pop("version", None)
    except FileNotFoundError:
      pass
    except KeyError:
      pass

  def _load_personal_default_values(self):
    try:
      with open(os.path.expanduser("~/.pypi-template"), encoding="utf-8") as fp:
        self._default_values.update(yaml.safe_load(fp))
    except Exception:
      pass

  def _collect_templates(self):
    for resource in self._list_resources():
      name = resource.replace("(dot)", ".")
      self._templates[name] = self._environment.get_template(resource)
      # extract template variables
      source = self._load_resource(resource)
      for var in meta.find_undeclared_variables(self._environment.parse(source)):
        self._debugging(f"🔎 found variable in {name} : {var}")
        if var not in self._template_vars and var not in self._system_vars:
          self._template_vars[var] = None

  def _collect_all_vars(self):
    for var in sorted(self._template_vars.keys()):
      self._collect_var(var)

  def _append(self, var, value):
    try:
      current = self._template_vars[var].copy()
    except KeyError:
      current = []
    if value not in current:
      self._debugging(f"appending {value} to {current}")
      self[var] = current + [value]

  def _collect_var(self, var, force=False):
    try:
      current = self._template_vars[var]
      if not force and current is not None and self._say_yes_to_all:
        return
      if var in self._var_lists:
        self.__collect_var_selections(var, current)
      else:
        self.__collect_var_value(var, current)
    except KeyError:
      print(f"🚨 unknown template variable: {var}")

  def __collect_var_value(self, var, current):
    question = f"{var.replace('_', ' ').capitalize()}: "
    if current is None:
      if var in self._default_values:
        current = self._default_values[var]
      else:
        current = ""
    self[var] = prompt(
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
        if selection not in selections:
          selections.append(selection)
    self[var] = selections
    
  def _changed_files(self):
    excluded = [ "base/index.md", "base/classifiers.txt" ]
    reported = []
    
    def _is_skipped_folder(folder):
      for path in self._template_vars["skip"]:
        if folder.startswith(path):
          if folder not in reported:
            self._being_verbose(f"⏭  skipping '{folder}' due to skipped '{path}'")
            reported.append(folder)
          return True
      return False
    
    for filename, template in self._templates.items():
      if filename in excluded:
        if filename not in reported:
          self._being_verbose(f"🛑 not rendering excluded {filename}")
          reported.append(filename)
        continue
      directory = os.path.dirname(filename)
      if "skip" in self._template_vars:
        if _is_skipped_folder(directory):
          continue
        if filename in self._template_vars["skip"]:
          if filename not in reported:
            self._being_verbose(f"⏭  skipping {filename}")
            reported.append(filename)
          continue
      yield filename, template

  def _render_files(self):
    self._being_verbose("🔨 applying templates")
    for filename, template in self._changed_files():
      # TODO generalize?
      filename = filename.replace(
        "(package_module_name)", self._template_vars["package_module_name"]
      )
      directory = os.path.dirname(filename)
      if directory != "" and not os.path.exists(directory):
        self._mkdir(directory)
      applied_vars = self._template_vars.copy()
      applied_vars.update(self._system_vars)
      applied_vars = {
        key : "" if value is None else value for key, value in applied_vars.items()
      }
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

  # filesystem helpers

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

  # output helpers
  
  def _out(self, data):
    if self._as_json:
      return json.dumps(data, indent=2, default=str)
    return data

  def _being_verbose(self, msg):
    if self._be_verbose or self._show_debug:
      print(msg)
      return True
    return False
  
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
  
  # resources helpers
  
  def _load_classifiers(self):
    return str(
      self._load_resource("base", "classifiers.txt"), "utf-8"
    ).split("\n")

  def _load_resource(self, *args):
    f = importlib_resources.files(__name__).joinpath("templates", *args)
    return f.read_bytes()

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

    for entry in importlib_resources.files(package).iterdir():
      resource = entry.name
      if resource.endswith(excluded_ext) or \
         resource in excluded or \
         f"{package}.{resource}" in excluded:
        pass
      elif importlib_resources.files(package).joinpath(resource).is_dir():
        subfiles = self._list_resources(f"{package}.{resource}")
        files += [ os.path.join(resource, f) for f in subfiles ]
      else:
        files.append(resource)
    return files
