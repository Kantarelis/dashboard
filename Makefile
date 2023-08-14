.PHONY: check format test


check:
	isort --diff --check .			# isort configuration in `setup.cfg`
	black --diff --check --color .	# black configuration in `pyproject.toml`
	flake8 .						# flake8 configuration in `setup.cfg`
	mypy .							# mypy configuration in `setup.cfg`
	bandit -r -c pyproject.toml .	# mypy configuration in `pyproject.toml`

format:
	isort .
	black .

test:
	python -m pytest --cov .