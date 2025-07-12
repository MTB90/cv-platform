SYSTEM_PYTHON=python3.12
VENV:=.venv

PIP:=$(VENV)/bin/pip
PYTHON:=$(VENV)/bin/python3
PYTEST:=$(VENV)/bin/pytest

$(VENV):
	$(SYSTEM_PYTHON) -m venv .venv

.PHONY: pip-install
pip-install: $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

.PHONY: pip-install-dev
pip-install-test: $(VENV)
	$(PIP) install -r requirements-test.txt

.PHONY: test-unit
test-unit:
	$(PYTEST) tests/unit

.PHONY: test-all
test-all: test-unit

.PHONY: build-image
build-image:
	docker build -t cv-platform-backend .
