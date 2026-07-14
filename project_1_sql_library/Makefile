.PHONY: install install-dev run lint typecheck test clean

VENV := .venv

PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip


install:
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt


install-dev: install
	$(PIP) install -r requirements-dev.txt


run:
	$(PYTHON) main.py


lint:
	$(PYTHON) -m flake8 .


typecheck:
	$(PYTHON) -m mypy .


test:
	$(PYTHON) -m pytest


clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete