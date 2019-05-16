.PHONY: all upload_pip upload_piptest lint flake8 tests setup

ifeq ($(OS),Windows_NT)
PYTHON = venv\Scripts\python.exe
else
PYTHON = ./venv/bin/python
endif

SOURCE = tester_gae
TEST = tests
COVERAGE = $(PYTHON) -m coverage
TESTS = $(TEST)/run_tests.py

all: tests

tests: flake8 lint coverage html
	$(COVERAGE) report --skip-covered

test:
	$(PYTHON) $(TESTS) test.$(T)

flake8:
	$(PYTHON) -m flake8 --max-line-length=110 $(SOURCE)

lint:
	$(PYTHON) -m pylint $(SOURCE)

verbose:
	$(PYTHON) $(TESTS) verbose

coverage:
	$(COVERAGE) run $(TESTS)

html:
	$(COVERAGE) html --skip-covered

dist:
	$(PYTHON) setup.py sdist bdist_wheel

upload_piptest: tests dist
	$(PYTHON) -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload_pip: tests dist
	$(PYTHON) -m twine upload dist/*

setup: setup_python setup_pip

setup_pip:
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m pip install -r $(TEST)/requirements.txt

setup_python:
	$(PYTHON_BIN) -m virtualenv ./venv
