#!/bin/bash
PYLINT = pylint

install:
	pip install -r requirements.txt

lint:
	pylint src && pylint scripts && pylint tests && pylint main.py

test:
	coverage run ./tests/main.py && coverage report --omit=./tests/*

coverage:
	coverage run tests/main.py