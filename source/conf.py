# -*- coding: utf-8 -*-
#
# TempoIQ Manual documentation build configuration file
#

import sys
import os

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.append(os.path.abspath('sphinxext'))

# -- General configuration ------------------------------------------------

html_context = {
    # Github info for generating source links in documents
    'gh_repository': 'TempoIQ/docs',
    'gh_branch': 'master',
    'display_github': True
}

# For development builds, invoke sphinx-build with '-t dev'.
if not tags.has('dev'):
    tags.add('publish')
    html_context['publish'] = True

# If your documentation needs a minimal Sphinx version, state it here.
#needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.todo',
    'tempoiq_sphinx',
    'snippets'
]


# List of valid snippet languages.
snippet_language_list = [
    {
        'key': 'python',
        'name': 'Python',
        'local_file': 'includes/python_snippets.py',
        #'gh_repository': 'TempoIQ/tempoiq-python',
        #'gh_branch': 'master',
        #'gh_path': 'tests/test_snippets.py',
        'line_comment': '#'
    },
    {
        'key': 'node',
        'name': 'Node.js',
        'highlight': 'javascript',
        'gh_repository': 'TempoIQ/tempoiq-node-js',
        'gh_branch': 'master',
        'gh_path': 'test/test_snippets.js',
        'line_comment': '//'
    },
    {
        'key': 'ruby',
        'name': 'Ruby',
        'local_file': 'includes/ruby_snippets.rb',
        'line_comment': '#'
    },
    {
        'key': 'java',
        'name': 'Java',
        'gh_repository': 'TempoIQ/tempoiq-java',
        'gh_branch': 'master',
        'gh_path': 'src/integration-test/java/com/tempoiq/Snippets.java',
        'line_comment': '//'
    },
    {
        'key': 'csharp',
        'name': 'C#/.NET',
        'local_file': 'includes/csharp_snippets.cs',
        'line_comment': '//'
    },
    {
        'key': 'http',
        'name': 'HTTP',
        'highlight': 'bash',
        'line_comment': '#',
        'local_file': 'includes/http_snippets.txt'
    }
]


# Name of the default domain.
primary_domain = 'tempoiq'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'toc-main'

# A list of (type, target) tuples (by default empty) that should be ignored
# when generating warnings in “nitpicky mode”
nitpick_ignore = [
    ('tempoiq:class', 'String')
]

# General information about the project.
project = u'Documentation'
copyright = u'2015 TempoIQ Inc'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = '1.0'
# The full version, including alpha/beta/rc tags.
release = '1.0'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['includes/*']

# Include TODO directives in the output. Turn off for publishing in prod
if tags.has('dev'):
    todo_include_todos = True

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# Default language for syntax highlighting
highlight_language = 'javascript'


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'tempoiq_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
html_theme_path = ["themes"]

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = "TempoIQ documentation"

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'
