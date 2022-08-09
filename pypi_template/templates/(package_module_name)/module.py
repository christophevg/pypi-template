"""
A very stupid example module, mainly for showing documentation generation.
"""

class Template():
  """
  A very stupid example class, mainly for showing documentation generation.
  """
  def __init__(self):
    """
    Initializes a flag to track wether the other party said hello first.
    """
    self.said_hello = False

  def hello(self):
    """
    Tracks that the other party said hello.
    """
    self.said_hello = True
    return self

  def my_name_is(self, name="Christophe"):
    """This function says hello.
    Accepts an optional name and formats a salutation given that name.
    Args:
      name: A optional string as name of some nice person to say hello to.
    Returns:
      A personalized salutation in the form of a string.
    """
    if self.said_hello:
      return f"hello {name}"
    return None
