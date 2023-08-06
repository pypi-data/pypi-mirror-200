package_dir := src/tograml_pydantic_utils
tests_dir := tests
code_dir = $(package_dir) $(tests_dir)

.PHONY: clean
clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -rf `find . -name .pytest_cache`
	rm -f .coverage
	rm -rf {dist,.cache,covreport,.ruff_cache,.mypy_cache,.pytest_cache}

.PHONY: lint
lint:
	isort --check-only $(code_dir)
	black --check --diff $(code_dir)
	ruff $(code_dir)

.PHONY: reformat
reformat:
	black $(code_dir)
	isort $(code_dir)


.PHONY: tests
tests:
	PYTHONPATH=src pytest --cov=tograml_pydantic_utils --cov-report html tests/
