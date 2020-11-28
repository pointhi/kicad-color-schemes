# Directory Configurations
THEME_DIR=themes

# Python Virtual Environment Configurations 
VENV_NAME=_venv
PYTHON_VERSION=3
PIP=$(VENV_NAME)/bin/pip$(PYTHON_VERSION)
PYTHON=$(VENV_NAME)/bin/python$(PYTHON_VERSION)

# Runs the theme selection script, which will prompt the user for a selection & then 
# execute that selection to update the theme. This will also save a backup of the
# original eeschema file in the event the user wants to revert to previous settings. 
.PHONY: theme
theme:
	python$(PYTHON_VERSION) scripts/theme_selection.py $(THEME_DIR)
	
# Creates the Python virtual environment and syncs it with resources/requirements.txt.
.PHONY: venv-update
venv-update:
	python$(PYTHON_VERSION) -m venv $(VENV_NAME)
	. $(VENV_NAME)/bin/activate
	$(PIP) install -r resources/requirements.txt