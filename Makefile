# have the makefile define the gates and just let the CI call it. Keeping the YAML dumb while keeping all the declarations in the makefile
.PHONY: lint fmt-check fmt type-check test bench all

lint:
	poetry run ruff check .

lint-fix:
	poetry run ruff check --fix .

fmt-check:
	poetry run ruff format --check .

fmt: 
	poetry run ruff format .

type-check:
	poetry run mypy

test: 
	poetry run pytest

bench:
	poetry run pytest benchmarks/ --no-cov

all: fmt-check lint type-check test
