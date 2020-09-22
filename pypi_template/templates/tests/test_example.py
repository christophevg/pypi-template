from pypi_template.module import Template

def test_template():
  t = Template()
  assert t.hello().my_name_is("Christophe") == "hello Christophe"
