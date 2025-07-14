SHELL := /bin/bash

SYSTEM_PYTHON=python3.12
VENV:=.venv

PIP:=$(VENV)/bin/pip
PYTHON:=$(VENV)/bin/python3
PYTEST:=$(VENV)/bin/pytest
FLAKE:=$(VENV)/bin/flake8
DOCKER:=docker

export PYTHONPATH=./app

$(VENV):
	$(SYSTEM_PYTHON) -m venv .venv

.PHONY: pip-install
pip-install: $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

.PHONY: pip-install-test
pip-install-test: $(VENV)
	$(PIP) install -r requirements-test.txt

.PHONY: test-unit
test-unit:
	$(PYTEST) tests/unit

.PHONY: test-all
test-all: test-unit

.PHONY: code-test
code-test:
	$(FLAKE) app

.PHONY: build-image
build-image:
	$(DOCKER) build -t cv-platform-backend .

.PHONY: up-services
up-dep-services:
	$(DOCKER) compose up

.PHONY: down-services
down-dep-services:
	$(DOCKER) compose down

.PHONY: serve
serve:
	source env.sh && $(PYTHON) app/api
