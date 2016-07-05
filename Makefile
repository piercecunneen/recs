#!/bin/bash
PYLINT = pylint

install:
	pip install -r requirements.txt

lint:
	pylint src && pylint scripts && pylint test

test:
