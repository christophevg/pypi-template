tag:
	git tag ${TAG} -m "${MSG}"
	git push --tags

venv:
	virtualenv $@

requirements: venv requirements.txt
	. venv/bin/activate; pip install -r requirements.txt > /dev/null

dist: requirements
	. venv/bin/activate; python setup.py sdist bdist_wheel

publish-test: dist
	. venv/bin/activate; twine upload --repository-url https://test.pypi.org/legacy/ dist/*

publish: dist
	. venv/bin/activate; twine upload --repository-url https://pypi.org/legacy/ dist/*

test:
	tox

.PHONY: dist
