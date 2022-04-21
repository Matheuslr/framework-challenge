export PYTHONDONTWRITEBYTECODE=1

.PHONY=help

help:  ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

clean:  ## Remove cache files
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf

###
# Dependencies section
###
_base-pip:
	@pip install -U pip wheel

system-dependencies:
	@sudo apt-get update -y && sudo apt-get install -y libpq-dev

export-requirements: _base-pip
	@pip freeze > requirements.txt

dependencies: _base-pip  ## Install dependencies
	@pip install -r requirements.txt


###
# Lint section
###
_flake8:
	@flake8 --show-source framework_api/

_isort:
	@isort --check-only framework_api/

_black:
	@black --diff --check framework_api/

_isort-fix:
	@isort framework_api/

_black-fix:
	@black framework_api/

_dead-fixtures:
	@pytest framework_api/ --dead-fixtures

_mypy:
	@mypy framework_api/

lint: _flake8 _isort _black _dead-fixtures  ## Check code lint
format-code: _isort-fix _black-fix  ## Format code


###
# Run local section
###
copy-envs:  ## Copy `.env.example` to `.env`
	@cp -n .env.example .env

init: dev-dependencies pre-commit-install copy-envs ## Initialize project

run-local:  ## Run server
	@python manage.py runserver