# global variables
DOCKER_IMAGE=python:3
IMAGE_NAME=ukrvassabi/svc-img-processing

VERSION=$(shell python setup.py --version)

# allow 'build' and 'test' arguments
.PHONY: build test

# default argument
default: help

version:
	@echo "Version: ${VERSION}"

help:
	@IFS=$$'\n' ; \
	help_lines=(`fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//'`); \
	for help_line in $${help_lines[@]}; do \
		IFS=$$'#' ; \
		help_split=($$help_line) ; \
		help_command=`echo $${help_split[0]} | sed -e 's/^ *//' -e 's/ *$$//'` ; \
		help_info=`echo $${help_split[2]} | sed -e 's/^ *//' -e 's/ *$$//'` ; \
		printf "%-30s %s\n" $$help_command $$help_info ; \
	done

test: ## run unit tests
	pytest --cov-config .coveragerc --cov=svc --cov-report term-missing svc/tests

env: ## create virtual environment
	python3 -m virtualenv venv
	source venv/bin/activate && pip install -r dev-requirements.txt

run: ## run development server
	python svc/api/app.py

run-gunicorn: ## run server with gunicorn
	gunicorn -c deployment/gunicorn.conf --log-config deployment/logging.conf svc.api.app:create_app

docker-run: ## run docker-compose
	docker-compose up -d

docker-build: ## create docker image
	docker build --force-rm -t $(IMAGE_NAME) .
