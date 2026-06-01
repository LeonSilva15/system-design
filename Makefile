.PHONY: install docs-serve docs-build

UV ?= uv

install:
	$(UV) sync --group docs

docs-serve:
	$(UV) run --group docs mkdocs serve

docs-build:
	$(UV) run --group docs mkdocs build --strict
