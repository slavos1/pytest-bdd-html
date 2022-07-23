VENV ?= .venv
PY_LINE_SIZE ?= 100
PY_FILES = $(wildcard *.py pytest_bdd_html/**.py tests/**.py)
# XXX "--profile black" is crucial for smooth working with black
# source: https://jugmac00.github.io/til/how-to-properly-configure-isort-and-black/
ISORT_ARGS ?= --profile black --star-first --honor-noqa --atomic --combine-as --combine-star --balanced -l ${PY_LINE_SIZE}

all: test

test:
	${VENV}/bin/tox -e dev --skip-pkg-install -- ${EXTRA}

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

# bumpver update --patch --tag rc --dry
# bumpver update --patch --tag final --dry

upload-test:: build check
	${VENV}/bin/twine upload -r testpypi dist/*
