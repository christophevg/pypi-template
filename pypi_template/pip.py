"""
Little submodule for managing dependencies. Mimics the pip interface. Commands with a + in front are available:
  Commands:
    +install             Install packages.
     lock                Generate a lock file.
     download            Download packages.
    +uninstall           Uninstall packages.
     freeze              Output installed packages in requirements format.
     inspect             Inspect the python environment.
    +list                List installed packages.
     show                Show information about installed packages.
     check               Verify installed packages have compatible dependencies.
     config              Manage local and global configuration.
     search              Search PyPI for packages.
     cache               Inspect and manage pip's wheel cache.
     index               Inspect information available from package indexes.
     wheel               Build wheels from your requirements.
     hash                Compute hashes of package archives.
     completion          A helper command used for command completion.
     debug               Show information useful for debugging.
     help                Show help for commands.
"""

import logging
logger = logging.getLogger(__name__)

class Pip:
  def __init__(self, pypi_template):
    self._pypi_template = pypi_template

  def list(self, scope=None):
    """
    Lists all current dependencies.
    """
    scope = self._scope(scope)
    if not scope:
      return
    return self._pypi_template._template_vars[scope]

  def install(self, dep, scope=None):
    """
    Installs new package dependency.
    """
    scope = self._scope(scope)
    if not scope:
      return
    deps = self._pypi_template[scope]
    if dep in deps:
      logger.warning(f"⚠️  {dep} is already installed")
      return
    logger.info(f"➕ installing new dependency : {dep}")
    deps.append(dep)
    self._pypi_template[scope] = deps
    self._apply_and_reinstall()

  def uninstall(self, dep, scope=None):
    """
    Uninstalls package dependency.
    """
    scope = self._scope(scope)
    if not scope:
      return
    deps = self._pypi_template[scope]
    if dep not in deps:
      logger.warning(f"⚠️  {dep} isn't installed")
      return
    logger.info(f"❌ uninstalling dependency : {dep}")
    deps.remove(dep)
    self._pypi_template[scope] = deps
    self._apply_and_reinstall()

  def _scope(self, scope):
    if scope == "test":
      return "test_requires"
    elif scope is None:
      return "requires"
    logger.error(f"🛑 unknown scope {scope}")
    return None

  def _apply_and_reinstall(self):
    self._pypi_template.apply()
    if self._pypi_template._going_to("👷‍♂️ reinstalling environments"):
      self._pypi_template._make("reinstall")
