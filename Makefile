.PHONY: setup fetch validate analyze report test reproduce

setup:
	uv sync --frozen

fetch:
	uv run --frozen morphostasis fetch

validate:
	uv run --frozen morphostasis validate

analyze:
	uv run --frozen morphostasis analyze

report:
	uv run --frozen morphostasis report

test:
	uv run --frozen pytest -q

reproduce: setup fetch validate analyze report test
