CLASSIFIERS=pypi_template/templates/base/classifiers.txt
CLASSIFIERS_URL=https://pypi.org/pypi?:action=list_classifiers

update-classifiers: $(CLASSIFIERS)
$(CLASSIFIERS):
	curl $(CLASSIFIERS_URL) > $@
	
.PHONY: $(CLASSIFIERS)

RUN_ARGS = verbose debug apply

publish-and-update: publish env
	pip install -U pypi-template
	