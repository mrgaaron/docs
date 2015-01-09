# Makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    = -n
SPHINXBUILD   = sphinx-build
PAPER         =
BUILDDIR      = build
GH_PAGES_SOURCES = source Makefile
GH_PAGES_PROD_REMOTE = upstream
GH_PAGES_DEV_REMOTE = origin

# User-friendly check for sphinx-build
ifeq ($(shell which $(SPHINXBUILD) >/dev/null 2>&1; echo $$?), 1)
$(error The '$(SPHINXBUILD)' command was not found. Make sure you have Sphinx installed, then set the SPHINXBUILD environment variable to point to the full path of the '$(SPHINXBUILD)' executable. Alternatively you can add the directory with the executable to your PATH. If you don't have Sphinx installed, grab it from http://sphinx-doc.org/)
endif

# Internal variables.
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) source
# the i18n builder cannot share the environment and doctrees with the others
I18NSPHINXOPTS  = $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) source

.PHONY: help clean html dirhtml singlehtml pickle json htmlhelp qthelp devhelp epub latex latexpdf text man changes linkcheck doctest gettext

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  html          to make standalone HTML files"
	@echo "  dev-html      to make a development build of HTML files"
	@echo "  publish-prod  to make and publish HTML files to the Production repo"
	@echo "  publish-dev   to make and publish HTML files to the Dev repo"
	@echo "  singlehtml    to make a single large HTML file"
	@echo "  json          to make JSON files"
	@echo "  xml           to make Docutils-native XML files"
	@echo "  changes       to make an overview of all changed/added/deprecated items"
	@echo "  linkcheck     to check all external links for integrity"
	@echo "  doctest       to run all doctests embedded in the documentation (if enabled)"

clean:
	rm -rf $(BUILDDIR)/*

html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

dev-html:
	$(SPHINXBUILD) -b html -t dev $(ALLSPHINXOPTS) $(BUILDDIR)/html
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

publish-prod:
	git checkout gh-pages
	rm -rf ./*
	git checkout master $(GH_PAGES_SOURCES)
	git reset HEAD
	$(SPHINXBUILD) -b html -t publish $(ALLSPHINXOPTS) $(BUILDDIR)/html
	mv -fv build/html/* ./
	rm -rf $(GH_PAGES_SOURCES) build
	git add -A
	git commit -m "Generated gh-pages for `git log master -1 --pretty=short --abbrev-commit`" && git push $(GH_PAGES_PROD_REMOTE) gh-pages ; git checkout master
	@echo
	@echo "Build finished. HTML pages have been published to prod."

publish-dev:
	git checkout gh-pages
	rm -rf ./*
	git checkout master $(GH_PAGES_SOURCES)
	git reset HEAD
	$(SPHINXBUILD) -b html -t publish $(ALLSPHINXOPTS) $(BUILDDIR)/html
	mv -fv build/html/* ./
	rm -rf $(GH_PAGES_SOURCES) build
	git add -A
	git commit -m "Generated gh-pages for `git log master -1 --pretty=short --abbrev-commit`" && git push $(GH_PAGES_DEV_REMOTE) gh-pages ; git checkout master
	@echo
	@echo "Build finished. HTML pages have been published."

singlehtml:
	$(SPHINXBUILD) -b singlehtml $(ALLSPHINXOPTS) $(BUILDDIR)/singlehtml
	@echo
	@echo "Build finished. The HTML page is in $(BUILDDIR)/singlehtml."

json:
	$(SPHINXBUILD) -b json $(ALLSPHINXOPTS) $(BUILDDIR)/json
	@echo
	@echo "Build finished; now you can process the JSON files."

xml:
	$(SPHINXBUILD) -b xml $(ALLSPHINXOPTS) $(BUILDDIR)/xml
	@echo
	@echo "Build finished. The XML files are in $(BUILDDIR)/xml."

changes:
	$(SPHINXBUILD) -b changes $(ALLSPHINXOPTS) $(BUILDDIR)/changes
	@echo
	@echo "The overview file is in $(BUILDDIR)/changes."

linkcheck:
	$(SPHINXBUILD) -b linkcheck $(ALLSPHINXOPTS) $(BUILDDIR)/linkcheck
	@echo
	@echo "Link check complete; look for any errors in the above output " \
	      "or in $(BUILDDIR)/linkcheck/output.txt."

doctest:
	$(SPHINXBUILD) -b doctest $(ALLSPHINXOPTS) $(BUILDDIR)/doctest
	@echo "Testing of doctests in the sources finished, look at the " \
	      "results in $(BUILDDIR)/doctest/output.txt."
