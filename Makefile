PY := python3

.PHONY: links-validate
links-validate:
	$(PY) tools/link_lint.py

.PHONY: yaml-validate
yaml-validate:
	$(PY) tools/yaml_guard.py

.PHONY: new-month
new-month:
	$(PY) tools/gen_note.py month --year $(YEAR) --mon $(MON)

.PHONY: new-year
new-year:
	$(PY) tools/gen_note.py year --year $(YEAR)

