tag:
	git tag ${TAG} -m "${MSG}"
	git push --tags

publish-test:
	python setup.py sdist upload -r pypitest

publish:
	python setup.py sdist upload -r pypi
