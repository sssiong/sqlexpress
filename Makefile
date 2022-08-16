clean_dir:
	rm -fr build/
	rm -fr dist/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '.pytest_cache' -exec rm -fr {} +

commit_patch:
	bumpversion patch

commit_minor:
	bumpversion minor

commit_major:
	bumpversion major

test_script:
	pytest -vv

upload_pypi: clean_dir
	python setup.py sdist bdist_wheel
	twine upload dist/*
