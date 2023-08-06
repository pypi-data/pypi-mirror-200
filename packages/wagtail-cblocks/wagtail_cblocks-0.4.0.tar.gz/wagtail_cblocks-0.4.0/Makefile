.PHONY: clean format help
.DEFAULT_GOAL := help

PYTHON := venv/bin/python

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo ""
	@grep '^[^.#]\+:\s\+.*#' Makefile | \
	  sed "s/\(.\+\):\s*\(.*\) #\s*\(.*\)/`printf "\033[93m"`  \1`printf "\033[0m"`	\3 [\2]/" | \
	  expand -35
	@echo ""
	@echo "Check the Makefile to know exactly what each target is doing."

clean: # Remove all builds and Python artifacts
	find wagtail_cblocks tests \
	  \( -name '*.py[co]' -o -name '__pycache__' \) -exec rm -rf {} +
	rm -rf build dist .eggs *.egg-info

test: # Run tests quickly with the current Python
	$(PYTHON) -m pytest --cov --cov-report=term:skip-covered

test-wip: # Run tests marked as wip with the current Python
	$(PYTHON) -m pytest -vv -m 'wip' --pdb

test-all: # Run tests on all Django and Wagtail versions
	nox

format: # Fix all the Python code syntax and imports order
	pre-commit run --all-files --hook-stage=manual

release: dist # Package and upload a release
	$(PYTHON) -m twine upload dist/*

dist: clean # Build source and wheel package
	$(PYTHON) -m build
	ls -l dist
