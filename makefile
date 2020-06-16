.PHONY: all upload_pip upload_piptest lint flake8 tests setup

ifeq ($(OS),Windows_NT)
PYTHON = venv/Scripts/python.exe
PTEST = venv/Scripts/pytest.exe
else
PYTHON = ./venv/bin/python
PTEST = ./venv/bin/pytest
endif

SOURCE = tester_gae
TESTS = tests

PIP = $(PYTHON) -m pip install
COVERAGE = $(PYTHON) -m coverage
PYTEST = $(PTEST) --cov=$(SOURCE) --cov-report term:skip-covered

all: tests

tests: flake8 lint
	$(PYTEST) --durations=5 $(TESTS)
	$(COVERAGE) html --skip-covered

test:
	$(PYTEST) -s --cov-append $(TESTS)/test/$(T)
	$(COVERAGE) html --skip-covered

flake8:
	$(PYTHON) -m flake8 --max-line-length=110 $(SOURCE)

lint:
	$(PYTHON) -m pylint $(SOURCE)

dist:
	$(PYTHON) setup.py sdist bdist_wheel

upload_piptest: tests dist
	$(PYTHON) -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload_pip: tests dist
	$(PYTHON) -m twine upload dist/*

setup: setup_python setup_pip

setup_pip:
	$(PIP) --upgrade pip
	$(PIP) -r requirements.txt

setup_python:
	$(PYTHON_BIN) -m virtualenv ./venv
