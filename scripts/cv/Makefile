# Makefile to build PDF and Markdown cv from YAML.
#
# Brandon Amos <http://bamos.github.io> and
# Ellis Michael <http://ellismichael.com>

WEBSITE_DIR=..
WEBSITE_PDF=$(WEBSITE_DIR)/blog/about/cv.pdf
WEBSITE_MD=$(WEBSITE_DIR)/pages/cv.md

TEMPLATES=$(shell find templates -type f)

INPUT_FILENAME?=cv_frontend.yaml

BUILD_DIR=build
TEX=$(BUILD_DIR)/cv.tex
PDF=$(BUILD_DIR)/cv.pdf
MD=$(BUILD_DIR)/cv.md

ifneq ("$(wildcard cv.hidden.yaml)","")
	YAML_FILES = $(INPUT_FILENAME) cv.hidden.yaml
else
	YAML_FILES = $(INPUT_FILENAME)
endif

.PHONY: all build build/cv.tex build/cv.md build/cv.pdf clean

all: $(PDF) $(MD)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(TEX) $(MD): $(TEMPLATES) $(YAML_FILES) generate.py
	./generate.py $(YAML_FILES)

$(PDF_ART): $(TEX)
	latexmk -verbose -f -pdf -cd- -jobname=$(BUILD_DIR)/cv $(BUILD_DIR)/cv || /bin/true
	latexmk -verbose -f -c -cd $(BUILD_DIR)/cv || /bin/true

$(PDF): $(TEX)
	latexmk -verbose -f -pdf -cd- -jobname=$(BUILD_DIR)/cv $(BUILD_DIR)/cv || /bin/true
	latexmk -verbose -f -c -cd $(BUILD_DIR)/cv || /bin/true

clean:
	rm -rf $(BUILD_DIR)/cv*
