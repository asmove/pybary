.PHONY: help clean test coverage docs servedocs install
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

rel_current_path = sys.argv[1]
abs_current_path = os.path.abspath(rel_current_path)
uri = "file://" + pathname2url(abs_current_path)

webbrowser.open(uri)
endef

export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

regex_pattern = r'^([a-zA-Z_-]+):.*?## (.*)$$'

for line in sys.stdin:
	match = re.match(regex_pattern, line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef

export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"
COVERAGE_IGNORE_PATHS = "pybary/examples"

PACKAGE_NAME = "pybary"
PACKAGE_VERSION := "$$(poetry version -s)"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test clean-cache ## remove all build, test, coverage, Python artifacts and cache

clean-build: ## remove build artifacts
	rm -fr build/ dist/ .eggs/
	find . -name '*.egg-info' -o -name '*.egg' -exec rm -fr {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -o -name '*.pyo' -o -name '*~' -exec rm -rf {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/ .coverage coverage.* htmlcov/ .pytest_cache

clean-cache: ## remove test and coverage artifacts
	find . -name '*cache*' -exec rm -rf {} +

test: ## run tests quickly with the default Python
	pytest

atest: install ## run tests on every Python version with tox
	tox -q

test-watch: ## run tests on watchdog mode
	ptw

lint: clean ## perform inplace lint fixes
	pip3 install --upgrade ruff
	ruff --fix .
	pre-commit run --all-files

coverage: clean ## check code coverage quickly with the default Python
	pytest --cov=pybary/
	coverage run --source "$(PACKAGE_VERSION)" -m pytest
	coverage report -m --omit="$(COVERAGE_IGNORE_PATHS)"
	coverage html
	$(BROWSER) htmlcov/index.html

install: clean ## install the package to the active Python's site-packages
	poetry shell
	poetry install

echo-version: ## Echo package version
	printf "$(PACKAGE_VERSION)" 

bump-version: ## bump version to user-provided {patch|minor|major} semantic
	poetry version $(v)
	git add pyproject.toml
	git commit -m "release/ tag v$(PACKAGE_VERSION)"
	git tag "v$(PACKAGE_VERSION)"
	git push
	git push --tags
	poetry version

publish: clean ## build source and publish package
	poetry publish --build
