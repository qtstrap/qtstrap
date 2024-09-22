# **************************************************************************** #
# General Make configuration

# This suppresses make's command echoing. This suppression produces a cleaner output. 
# If you need to see the full commands being issued by make, comment this out.
MAKEFLAGS += -s

# **************************************************************************** #

# load the pypi credentials
ifneq (,$(wildcard .env))
include .env
# export them for twine
export
endif

# **************************************************************************** #
# Targets

# run the application
run: venv
	$(VENV_PYTHON) src/main.py

#
build:
	uv build

#
publish:
	twine upload dist/* -u __token__

#
tox:
	$(VENV_PYTHON) -m tox

#
tests:
	$(VENV_PYTHON) -m pytest -s

coverage:
	$(VENV_PYTHON) -m pytest --cov

.PHONY: docs
docs:
	$(VENV_PYTHON) build_docs.py

# remove build artifacts
clean:
	-$(RM) build
	-$(RM) dist
	-$(RM) qtstrap.egg-info

## **************************************************************************** #
# python venv settings
VENV_NAME := .venv
CANARY_FILE := pyproject.toml

VENV_DIR := $(VENV_NAME)

ifeq ($(OS),Windows_NT)
	VENV := $(VENV_DIR)/Scripts
	PYTHON := python
else
	VENV := $(VENV_DIR)/bin
	PYTHON := python3
endif

VENV_CANARY_DIR := $(VENV_DIR)/canary
VENV_CANARY_FILE := $(VENV_CANARY_DIR)/$(CANARY_FILE)
VENV_TMP_DIR := $(VENV_DIR)/tmp
VENV_TMP_FREEZE := $(VENV_TMP_DIR)/freeze.txt
VENV_PYTHON := $(VENV)/$(PYTHON)
VENV_PYINSTALLER := $(VENV)/pyinstaller
RM := rm -rf 
CP := cp

# Add this as a requirement to any make target that relies on the venv
.PHONY: venv
# venv: $(VENV_DIR) $(VENV_CANARY_FILE)
venv: $(VENV_DIR)

# Create the venv if it doesn't exist
$(VENV_DIR):
	uv venv
	uv sync

# Update the venv if the canary is out of date
$(VENV_CANARY_FILE): $(CANARY_FILE)
	uv sync
	-$(RM) $(VENV_CANARY_DIR)
	-mkdir $(VENV_CANARY_DIR)
	-$(CP) $(CANARY_FILE) $(VENV_CANARY_FILE)

# forcibly update the canary file
canary: $(VENV_CANARY_DIR)
	-$(RM) $(VENV_CANARY_DIR)
	-mkdir $(VENV_CANARY_DIR)
	$(CP) $(CANARY_FILE) $(VENV_CANARY_FILE)
