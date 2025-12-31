# -*- coding: utf-8 -*-

# Project Automation Makefile
#
# This Makefile serves as a command-line system to perform common development
# operations for this project. It automatically resolves the correct Python
# interpreter and executes the appropriate scripts for each operation.
#
# Usage:
#   make <command>              # Run a specific command
#   make help                   # Show all available commands
#
# Python Environment:
# - Uses ~/.pyenv/shims/python for bootstrap and setup commands
# - Uses .venv/bin/python for project-specific operations
# - Automatically manages virtual environment and dependencies
#
# Command Categories:
# - ⭐ Essential commands for daily development
# - 🏗 Build and compilation operations
# - 🚀 Deployment operations
# - 💥 Cleanup and removal operations
# - 🛠 Configuration and setup operations
# - 🗑 Maintenance operations
#
# ==============================================================================
.PHONY: help \
		venv-create \
		venv-remove \
		poetry-lock \
		poetry-export \
		install-root \
		install \
		install-dev \
		install-test \
		install-doc \
		install-automation \
		install-all \
		test-only \
		test \
		cov-only \
		cov \
		view-cov \
		int-only \
		int \
		gen-m \
		nb-to-md \
		build-doc \
		view-doc \
		build \
		publish \
		release \
		setup-codecov \
		setup-rtd \
		edit-github


help: ## ⭐ Show all available commands with descriptions
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-40s\033[0m %s\n", $$1, $$2}'


# Environment Setup Commands
venv-create: ## ⭐ Create project virtual environment (.venv)
	~/.pyenv/shims/python ./bin/g1_t2_s1_venv_create.py


venv-remove: ## 💥 Remove project virtual environment completely
	~/.pyenv/shims/python ./bin/g1_t2_s2_venv_remove.py


poetry-lock: ## ⭐ Resolve dependencies using poetry (updates poetry.lock)
	~/.pyenv/shims/python ./bin/g2_t1_s1_poetry_lock.py


poetry-export: ## ⭐ Export locked dependencies to requirements.txt for deployment
	~/.pyenv/shims/python ./bin/g2_t1_s6_poetry_export.py


install-root: ## Install only this package in development mode (no deps)
	~/.pyenv/shims/python ./bin/g2_t2_s1_install_only_root.py


install: ## ⭐ Install main runtime dependencies (use after venv-create)
	~/.pyenv/shims/python ./bin/g2_t2_s2_install.py


install-dev: ## Install development tools (linting, formatting, etc.)
	~/.pyenv/shims/python ./bin/g2_t2_s3_install_dev.py


install-test: ## Install testing framework and test utilities
	~/.pyenv/shims/python ./bin/g2_t2_s4_install_test.py


install-doc: ## Install Sphinx and documentation building tools
	~/.pyenv/shims/python ./bin/g2_t2_s5_install_doc.py


install-automation: ## Install tools for CI/CD and automation scripts
	~/.pyenv/shims/python ./bin/g2_t2_s6_install_automation.py


install-all: ## Install all dependencies (dev, test, doc, automation)
	~/.pyenv/shims/python ./bin/g2_t2_s7_install_all.py


# Testing Commands
test-only: ## Run unit tests only (assumes test deps already installed)
	~/.pyenv/shims/python ./bin/g3_t1_s1_run_unit_test.py


test: install install-test test-only ## ⭐ Run unit tests with dependency check


cov-only: ## Run coverage analysis only (assumes test deps installed)
	~/.pyenv/shims/python ./bin/g3_t2_s1_run_cov_test.py


cov: install install-test cov-only ## ⭐ Run tests with coverage analysis


view-cov: ## ⭐ Open coverage report in browser (run after cov)
	~/.pyenv/shims/python ./bin/g3_t2_s2_view_cov_result.py


int-only:## Run integration tests only (assumes deps installed)
	~/.pyenv/shims/python ./bin/g3_t3_s1_run_int_test.py


int: install install-test int-only ## ⭐ Run integration tests with dependency check


# Code Generation Commands
gen-m: ## 🛠 Generate m.py module for lazy-loading API types
	.venv/bin/python scripts/gen_m.py


# Documentation Commands
nb-to-md: ## 🛠 Convert Jupyter notebooks to Markdown format
	~/.pyenv/shims/python ./bin/g4_t1_s1_nb_to_md.py


build-doc: install install-doc ## ⭐ Build Sphinx documentation (output: docs/build/html)
	~/.pyenv/shims/python ./bin/g4_t2_s1_build_doc.py


view-doc: ## ⭐ Open built documentation in browser
	~/.pyenv/shims/python ./bin/g4_t2_s2_view_doc.py


# Package Build and Release Commands
build: ## 🏗 Build Python wheel and source distribution packages
	~/.pyenv/shims/python ./bin/g5_t1_s1_build_package.py


publish: build ## ⭐ Build and publish package to AWS CodeArtifact
	~/.pyenv/shims/python ./bin/g5_t2_s1_publish_package.py


release: ## ⭐ Create GitHub release with current version tag
	~/.pyenv/shims/python ./bin/g5_t2_s3_create_release.py


setup-codecov: ## ⭐ Configure Codecov token for CI coverage reporting
	~/.pyenv/shims/python ./bin/g6_t1_s1_setup_codecov.py


setup-rtd: ## ⭐ Create ReadTheDocs.org Project
	~/.pyenv/shims/python ./bin/g6_t1_s2_setup_readthedocs.py


edit-github: ## ⭐ Update GitHub repository description and settings
	~/.pyenv/shims/python ./bin/g6_t1_s3_edit_github_repo.py
