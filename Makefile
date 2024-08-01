test:
	pytest

lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --ignore=C901 --exit-zero --max-complexity=10 --max-line-length=127 --statistics

fix:
	autopep8 --in-place `find pgformat -type f -name "*.py"`
	autopep8 --in-place tests/*.py
