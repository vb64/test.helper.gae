.PHONY: all clean upload_pip upload_piptest lint flake8

PROJECT = tester_gae

all: tests

tests: flake8 lint

flake8:
	python -m flake8 --max-line-length=110 $(PROJECT)

lint:
	python -m pylint $(PROJECT)

upload_piptest: tests
	python setup.py sdist upload -r pypitest

upload_pip: tests
	python setup.py sdist upload -r pypi
