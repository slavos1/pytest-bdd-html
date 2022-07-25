VENV ?= .venv
PY_LINE_SIZE ?= 100
PY_FILES = $(wildcard *.py pytest_bdd_html/**.py tests/**.py)
# XXX "--profile black" is crucial for smooth working with black
# source: https://jugmac00.github.io/til/how-to-properly-configure-isort-and-black/
ISORT_ARGS ?= --profile black --star-first --honor-noqa --atomic --combine-as --combine-star --balanced -l ${PY_LINE_SIZE}
PYLINT_SCORE = 9.5
SHELL = bash

all: test

dev cov:
	${VENV}/bin/tox -e $@ --skip-pkg-install -- ${EXTRA}

test: dev

isort:
	${VENV}/bin/isort ${ISORT_ARGS} --color ${PY_FILES}

# --line-length=100
black fmt: isort
	${VENV}/bin/black -l ${PY_LINE_SIZE} ${PY_FILES}

help: EXTRA := -p bdd-html --help
help: test

# needs pip install build
build::
	rm -rf dist/
	${VENV}/bin/python -m build --sdist --wheel

check::
	${VENV}/bin/twine check dist/*

upload-test:: build check
	${VENV}/bin/twine upload -r testpypi dist/*

upload-prod:: build check
	${VENV}/bin/twine upload -r pypi dist/*

lint:
	nice -19 stdbuf -o0 ${VENV}/bin/pylint \
		--generated-members=objects \
		--fail-under=${PYLINT_SCORE} \
		--score=y \
		--disable too-few-public-methods \
		--output >(tee pylint.log) ${EXTRA} \
		pytest_bdd_html/ tests/

# pip install mypy git+https://github.com/lxml/lxml-stubs.git
mypy:
	${VENV}/bin/mypy --install-types --non-interactive pytest_bdd_html/ tests/ 2>&1 | tee mypy.log

# bumpver update --patch --tag rc --dry
bump-patch:
	bumpver update --patch --tag alpha --dry

doc: README.html

README.html: README.rst
	pandoc -w asciidoc -o >( sed '2s/^/:toc: left\n:source-highlighter: pygments\n/; s/^=//; s/,sourceCode,/,/' > $<.adoc ) $<
	asciidoctor -o $@ $<.adoc
	rm -f $<.adoc
