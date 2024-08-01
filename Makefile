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
