BROWSER_PYSCRIPT := '''
import os, webbrowser, sys
from urllib.request import pathname2url
rel_current_path = sys.argv[1]
abs_current_path = os.path.abspath(rel_current_path)
uri = "file://" + pathname2url(abs_current_path)
webbrowser.open(uri)
'''

PRINT_HELP_PYSCRIPT := '''
import re, sys
regex_pattern = r'^([a-zA-Z_-]+):.*?## (.*)$$'
for line in sys.stdin:
    match = re.match(regex_pattern, line)
    if match:
        target, help = match.groups()
        print("%-20s %s" % (target, help))
'''

BROWSER := "python -c \"$$BROWSER_PYSCRIPT\""
COVERAGE_IGNORE_PATHS := "pybary/examples"
PACKAGE_NAME := "pybary"
PACKAGE_VERSION := `poetry version -s`

help:
    @echo "Available commands:"
    @just --list

clean: clean-build clean-pyc clean-test clean-cache ## remove all build, test, coverage, Python artifacts and cache

clean-build:
    rm -fr build/ dist/ .eggs/
    find . -name '*.egg-info' -o -name '*.egg' -exec rm -fr {} +

clean-pyc:
    find . -name '*.pyc' -o -name '*.pyo' -o -name '*~' -exec rm -rf {} +

clean-test:
    rm -fr .tox/ .coverage coverage.* htmlcov/ .pytest_cache

clean-cache:
    find . -name '*cache*' -exec rm -rf {} +

test:
    pytest

atest:
    tox -q

watch:
    ptw

lint:
    just clean
    pip3 install --upgrade ruff
    ruff check --fix
    pre-commit run --all-files

coverage:
    just clean
    pytest --cov=pybary --cov-report=term-missing
    coverage run --source "$PACKAGE_VERSION" -m pytest
    coverage report -m --omit="$COVERAGE_IGNORE_PATHS"
    coverage html
    $BROWSER htmlcov/index.html

install:
    just clean
    poetry shell
    poetry install

echo-version:
    @echo "$PACKAGE_VERSION"

check-bump:
    @if [ "$v" != "patch" ] && [ "$v" != "minor" ] && [ "$v" != "major" ]; then \
        echo "Invalid input for 'v': $v. Please use 'patch', 'minor', or 'major'."; \
        exit 1; \
    fi
bump:
    just check-bump v=$v
    poetry version $v
    git add pyproject.toml
    git commit -m "release/ tag v$(poetry version -s)"
    git tag "v$(poetry version -s)"
    git push
    git push --tags
    poetry version

publish:
    just clean
    poetry publish --build
