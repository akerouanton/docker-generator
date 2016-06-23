.PHONY: install test-php

NOSETESTS ?= nosetests

install:
	pip install -r requirements.txt

tests:
	PYTHONPATH=./lib $(NOSETESTS) -d -w test/unit -v --with-coverage --cover-package=dockerize
	PYTHONPATH=./lib $(NOSETESTS) -d -w test/functional -v
