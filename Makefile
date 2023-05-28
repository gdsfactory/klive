help:
	@echo 'make docs:       	  Build the docs and place them in ./site'
	@echo 'make docs-serve:       mkdocs serve the docs'

docs:
	mkdocs build

docs-serve:
	mkdocs serve

.PHONY: docs docs-serve