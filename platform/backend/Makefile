SHELL := /bin/bash

SYSTEM_PYTHON=python3.12
VENV:=.venv

PIP:=$(VENV)/bin/pip
PYTHON:=$(VENV)/bin/python3
PYTEST:=$(VENV)/bin/pytest
FLAKE:=$(VENV)/bin/flake8
BLACK:=$(VENV)/bin/black

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
	$(BLACK) --check app --line-length 100 --exclude app/migrations

.PHONY: code-format
code-format:
	$(BLACK) app --line-length 100 --exclude app/migrations

.PHONY: unit-test
unit-test:
	$(PYTEST) app --cov=./ --cov-report=html

.PHONY: build-image
build-image:
	$(DOCKER) build -t cv-platform-backend .

.PHONY: up-services
up-dep-services: build-image
	$(DOCKER) compose up &

.PHONY: down-services
down-dep-services:
	$(DOCKER) compose down

.PHONY: serve
serve:
	source env.sh && $(PYTHON) app/api

.PHONY: migration
migration:
	(cd app; alembic upgrade head)
