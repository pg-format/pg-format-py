test:
	@pytest

lint:
	@flake8 pgformat --select=E9,F63,F7,F82 --show-source --statistics
	@flake8 pgformat --ignore=C901 --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	@flake8 tests --select=E9,F63,F7,F82 --show-source --statistics
	@flake8 tests --ignore=C901 --exit-zero --max-complexity=10 --max-line-length=127 --statistics

fix:
	@autopep8 --in-place `find pgformat -type f -name "*.py"`
	@autopep8 --in-place tests/*.py

build:
	@flit build

release:
	@echo "Run tbump new-version"

deps:
	pip install -r requirements.txt
	pip install tbump

init:
	@echo "Setting up environment and dependencies..."
	@git submodule update --init
	@python -m venv .venv
	@.venv/bin/pip install -r requirements.txt --quiet
	@.venv/bin/pip install tbump --quiet
	@echo "Please run: . .venv/bin/activate"

