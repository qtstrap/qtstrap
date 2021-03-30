# Makefile

The provided Makefile has several targets that assist with general project development. Using the Makefile means that you do not have to activate the venv unless you need to interact with it directly. The Makefile uses specially constructed targets to automatically build the venv and execute using the venv's python installation.

General targets:

- `make run` run your project
- `make debug` run your project in debug mode
- `make bundle` builds a single-folder bundle using PyInstaller
- `make run_bundle` run the single-folder bundle's executable
- `make zip` compress the bundle into a zip file
- `make installer` wrap the bundle into a Windows installer using Inno Setup
- `make clean` delete the project's build artifacts
  
The Makefile also seamlessly manages your python virtual environment using the following targets:

- `make venv` create the venv, if it doesn't exist
- `make pip` passes it's args to the venv's pip
- `make clean_venv`
- `make reset_venv`