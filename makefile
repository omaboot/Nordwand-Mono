.PHONY: install build build-otf build-ttf web-cut install-mac

FONT_VERSION ?= $(shell git describe --tags --abbrev=0 2>/dev/null || echo 1.0.0)

install:
	uv sync

build:
	uv run python -m generate_font --font-version $(FONT_VERSION) --web-font
	uv run python -m scripts.banner
	uv run python -m scripts.specimen_pdf
	uv run python -m scripts.samples
	uv run python -m scripts.alternatives_markdown

build-font:
	uv run python -m generate_font --font-version $(FONT_VERSION) --web-font

build-ttf:
	uv run python -m generate_font --font-version $(FONT_VERSION) --ttf

# A small Regular and Bold for the web (Latin-1, punctuation, arrows), in fonts/web-cut/
web-cut: build-ttf
	uv run python -m scripts.web_cut

build-otf:
	uv run python -m generate_font --font-version $(FONT_VERSION) --otf

install-mac:
	cp -r fonts/otf/NordwandMono-*.otf ~/Library/Fonts

visualize:
	open -n -a /Library/Frameworks/Python.framework/Versions/3.12/Resources/Python.app \
    --env "__PYVENV_LAUNCHER__=$PWD/.venv/bin/python" \
    --args -m visualize lowercase_a
