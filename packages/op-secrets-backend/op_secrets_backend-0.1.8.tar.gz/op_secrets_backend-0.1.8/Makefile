PACKAGE_NAME = src/`python setup.py --name`
COVERAGE_THRESHOLD = 80
# ubuntu dependencies -> pyenv -> pyenv-python vXYZ -> python-virtualenv
install-python-environment:
	./requirements/setup_python_environment.sh $(python_version)
# install development requirements
dev-install:install
	pip install -r requirements/requirements_dev.txt --upgrade
# install package requirements

install: # install package requirements
	python setup.py install

lint:
ifeq (, $(shell which black))
	flake8 $(PACKAGE_NAME) test package_functions.py
else
	black -vS $(PACKAGE_NAME) test package_functions.py
	flake8 $(PACKAGE_NAME) test package_functions.py
endif

test-run:
# invoking interpreter directly adds the current dir to sys.path
	# python -m pytest -rsA test/examples.py
	# python -m pytest -srA
	coverage run -m --source $(PACKAGE_NAME) \
	pytest -p no:cacheprovider --durations=5 --disable-warnings -srfExXpP $(flag);


check-coverage:
	coverage report -m --fail-under=${COVERAGE_THRESHOLD}
docs:
	rm -f docs/$(PACKAGE_NAME).rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ $(PACKAGE_NAME)
	$(MAKE) $(MAKE_OPTIONS) -C docs clean
	$(MAKE) $(MAKE_OPTIONS) -C docs html
	$(BROWSER) docs/_build/html/index.html

build-package:
# builds source and wheel package
	python3 -m build

bumpversion: test lint
	bumpversion $(type)


