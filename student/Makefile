#
# This file makes your submission when you type 'make'


# Set MODE for running on local or on hadoop

MODE="-rlocal"

PYFILES = $(wildcard *.py)
TXTFILES = $(wildcard *.txt)
PDFFILES = $(wildcard *.pdf)

zip: validator.py $(PYFILES) $(TXTFILES) $(PDFFILES)
	python validator.py --zip
