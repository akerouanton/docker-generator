.PHONY: install test-php

install:
	pip install -r requirements.txt

test:
	@./dockerize.py
