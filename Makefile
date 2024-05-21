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

# reinstall this package to the virtualenv
reload: venv
	$(VENV_PYTHON) -m pip install -e .

#
build: venv
	$(VENV_PYTHON) -m build

#
publish: venv
	$(VENV_PYTHON) -m twine upload dist/* -u __token__

#
tox: venv
	$(VENV_PYTHON) -m tox

#
tests: venv
	$(VENV_PYTHON) -m pytest -s

coverage: venv
	$(VENV_PYTHON) -m pytest --cov

docs: venv
	$(VENV_PYTHON) build_docs.py
.PHONY: docs

# remove build artifacts
clean:
	-$(RM) build
	-$(RM) dist
	-$(RM) qtstrap.egg-info

## **************************************************************************** #
# python venv settings
VENV_NAME := .venv
REQUIREMENTS := requirements.txt

VENV_DIR := $(VENV_NAME)

ifeq ($(OS),Windows_NT)
	VENV := $(VENV_DIR)/Scripts
	PYTHON := python
else
	VENV := $(VENV_DIR)/bin
	PYTHON := python3
endif

VENV_CANARY_DIR := $(VENV_DIR)/canary
VENV_CANARY_FILE := $(VENV_CANARY_DIR)/$(REQUIREMENTS)
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
	$(PYTHON) -m venv $(VENV_DIR)

# Update the venv if the canary is out of date
$(VENV_CANARY_FILE): $(REQUIREMENTS)
	uv pip install -r $(REQUIREMENTS)
	-$(RM) $(VENV_CANARY_DIR)
	-mkdir $(VENV_CANARY_DIR)
	-$(CP) $(REQUIREMENTS) $(VENV_CANARY_FILE)

# forcibly update the canary file
canary: $(VENV_CANARY_DIR)
	-$(RM) $(VENV_CANARY_DIR)
	-mkdir $(VENV_CANARY_DIR)
	$(CP) $(REQUIREMENTS) $(VENV_CANARY_FILE)

# update requirements.txt to match the state of the venv
freeze_reqs: venv
	$(VENV_PYTHON) -m pip freeze > $(REQUIREMENTS)

# try to update the venv - expirimental feature, don't rely on it
update_venv: venv
	uv pip install -r $(REQUIREMENTS)
	-$(RM) $(VENV_CANARY_DIR)
	-mkdir $(VENV_CANARY_DIR)
	-$(CP) $(REQUIREMENTS) $(VENV_CANARY_FILE)

# remove all packages from the venv
clean_venv:
	$(RM) $(VENV_CANARY_DIR)
	mkdir $(VENV_TMP_DIR)
	$(VENV_PYTHON) -m pip freeze > $(VENV_TMP_FREEZE)
	$(VENV_PYTHON) -m pip uninstall -y -r $(VENV_TMP_FREEZE)
	$(RM) $(VENV_TMP_DIR)

# clean the venv and rebuild it
reset_venv: clean_venv update_venv
