from pypi_template.module import Template

def test_template():
  t = Template()
  assert t.say_hello() == "hello Christophe"
