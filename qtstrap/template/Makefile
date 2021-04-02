# **************************************************************************** #
# General Make configuration

# This suppresses make's command echoing. This suppression produces a cleaner output. 
# If you need to see the full commands being issued by make, comment this out.
MAKEFLAGS += -s

# **************************************************************************** #

# load the project variables
ifneq (,$(wildcard src/app_info.py))
include src/app_info.py

# remove extra quotes
AppName := $(patsubst "%",%,$(AppName))
AppVersion := $(patsubst "%",%,$(AppVersion))
AppPublisher := $(patsubst "%",%,$(AppPublisher))
AppExeName := $(patsubst "%",%,$(AppExeName))
AppIconName := $(patsubst "%",%,$(AppIconName))
AppId := $(patsubst "%",%,$(AppId))

# export them for InnoSetup
export
endif

# **************************************************************************** #
# Development Targets

# run the application
run: venv
	$(VENV_PYTHON) src/main.py

# run the application in pdb
debug: venv
	$(VENV_PYTHON) -m pdb src/main.py

# **************************************************************************** #
# Build Targets

beep:
	echo $(AppName)
	echo $(AppVersion)

# build a one folder bundle 
bundle: venv
	$(VENV_PYINSTALLER) -y bundle.spec

# run the bundled executable
run_bundle:
ifeq ($(OS),Windows_NT)
	dist/$(AppName)/$(AppName).exe
else
	dist/$(AppName)/$(AppName)
endif

# **************************************************************************** #
# Release Targets

# wrap the bundle into a zip file
zip:
	$(PYTHON) -m zipfile -c dist/$(AppName)-$(AppVersion)-portable.zip dist/$(AppName)/

# build an installer with InnoSetup
installer:
	iscc "installer.iss"

# remove the various build outputs
clean:
	-@ $(RM) build
	-@ $(RM) dist

# **************************************************************************** #
# python venv settings
VENV_NAME := .venv

ifeq ($(OS),Windows_NT)
	VENV_DIR := $(VENV_NAME)
	VENV := $(VENV_DIR)\Scripts
	PYTHON := python
	VENV_PYTHON := $(VENV)\$(PYTHON)
	VENV_PYINSTALLER := $(VENV)\pyinstaller
	RM := rd /s /q 
else
	VENV_DIR := $(VENV_NAME)
	VENV := $(VENV_DIR)/bin
	PYTHON := python3
	VENV_PYTHON := $(VENV)/$(PYTHON)
	VENV_PYINSTALLER := $(VENV)/pyinstaller
	RM := rm -rf 
endif

# Add this as a requirement to any make target that relies on the venv
.PHONY: venv
venv: $(VENV_DIR)

# Create the venv if it doesn't exist
$(VENV_DIR):
	$(PYTHON) -m venv $(VENV_DIR)
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PYTHON) -m pip install -r requirements.txt

# If the first argument is "pip"...
ifeq (pip,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "pip"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif

# forward pip commands to the venv
pip: venv
	$(VENV_PYTHON) -m pip $(RUN_ARGS)

# update requirements.txt to match the state of the venv
freeze_reqs: venv
	$(VENV_PYTHON) -m pip freeze > requirements.txt

# try to update the venv - expirimental feature, don't rely on it
update_venv: venv
	$(VENV_PYTHON) -m pip install --upgrade -r requirements.txt

# deletes the venv
clean_venv:
	$(RM) $(VENV_DIR)

# deletes the venv and rebuilds it
reset_venv: clean_venv venv