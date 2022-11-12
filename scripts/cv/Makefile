# Makefile to build PDF and Markdown cv from YAML.
#
# Brandon Amos <http://bamos.github.io> and
# Ellis Michael <http://ellismichael.com>

WEBSITE_DIR=..
WEBSITE_PDF=$(WEBSITE_DIR)/blog/about/cv.pdf
WEBSITE_MD=$(WEBSITE_DIR)/pages/cv.md

TEMPLATES=$(shell find templates -type f)

BUILD_DIR=build
TEX=$(BUILD_DIR)/cv.tex
PDF=$(BUILD_DIR)/cv.pdf
MD=$(BUILD_DIR)/cv.md

ifneq ("$(wildcard cv.hidden.yaml)","")
	YAML_FILES = cv.yaml cv.hidden.yaml
else
	YAML_FILES = cv_onepage.yaml
endif

.PHONY: all public serve push clean

all: $(PDF) $(MD)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

public: $(BUILD_DIR) $(TEMPLATES) $(YAML_FILES) generate.py
	./generate.py cv.yaml

$(TEX) $(MD): $(TEMPLATES) $(YAML_FILES) generate.py
	./generate.py $(YAML_FILES)

$(PDF): $(TEX)
	latexmk -verbose -f -pdf -cd- -jobname=$(BUILD_DIR)/cv $(BUILD_DIR)/cv || /bin/true
	latexmk -verbose -f -c -cd $(BUILD_DIR)/cv || /bin/true

deploy: all
	cp $(PDF) $(WEBSITE_PDF)
	cp $(MD) $(WEBSITE_MD)

serve: deploy
	cd $(WEBSITE_DIR) && ./run.sh

clean:
	rm -rf $(BUILD_DIR)/cv*
