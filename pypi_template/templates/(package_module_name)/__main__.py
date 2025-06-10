from {{ package_module_name }}.module import Template

tpl = Template()
print(tpl.hello().my_name_is("Stranger"))
