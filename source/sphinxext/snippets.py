# Extension for embedding code examples in docs

import urllib2
import os.path
from docutils import nodes

from sphinx.errors import SphinxError
from sphinx.directives.code import CodeBlock
from sphinx.util.compat import Directive


class Language(object):
    """Config should contain the following keys:
    'key', 'name', 'highlight', 'line_comment',
    'gh_repository', 'gh_branch', 'gh_path'"""

    def __init__(self, config):
        for config_key in config:
            setattr(self, config_key, config[config_key])

        if not hasattr(self, 'highlight'):
            self.highlight = self.key

        self.has_remote_source = (hasattr(self, 'gh_repository') and
                                  hasattr(self, 'gh_branch') and
                                  hasattr(self, 'gh_path'))

    def get_raw_url(self):
        if not self.has_remote_source:
            return None
        return "https://raw.githubusercontent.com/{}/{}/{}" \
               .format(self.gh_repository,
                       self.gh_branch,
                       self.gh_path)

    def get_pretty_url(self, lineno=None):
        if not self.has_remote_source:
            return None
        url = "https://github.com/{}/blob/{}/{}" \
              .format(self.gh_repository,
                      self.gh_branch,
                      self.gh_path)
        if lineno:
            url += "#L" + repr(lineno)

        return url


class SnippetDisplay(Directive):
    """
    Directive to insert all snippets with a given title.
    """
    required_arguments = 1

    def run(self):
        env = self.state.document.settings.env

        key = self.arguments[0]
        node = SnippetDisplayNode()
        node['key'] = key

        env.snippet_display.append(node)

        return [node]


class SnippetDisplayNode(nodes.General, nodes.Element):
    @classmethod
    def register_to(cls, app):
        app.add_node(cls, html=(cls.html_visit, cls.html_depart))

    @staticmethod
    def html_visit(translator, node):
        translator.body.append('<div class="snippets-container" data-key="{}">'
                               .format(node['key']))

        translator.body.append('<ul class="headings">')
        for child in node.children:
            translator.body.append('<li><a class="heading" href="#" data-language="{}">{}</a></li>'
                                   .format(child['language'], child['language-name']))
        translator.body.append('</ul>')
        translator.body.append('<ul class="snippets">')

    @staticmethod
    def html_depart(translator, node):
        translator.body.append('</ul>')
        translator.body.append('</div>')


class SingleSnippetNode(nodes.General, nodes.Element):
    def __init__(self, key, language, content="", lineno=None):
        super(SingleSnippetNode, self).__init__()
        self['key'] = key
        self['language'] = language.key
        self['language-name'] = language.name

        if lineno:
            self['source-url'] = language.get_pretty_url(lineno)

        # Support strings, or a list of strings
        if isinstance(content, basestring):
            body = content
        else:
            body = u'\n'.join([line.rstrip() for line in content])

        literal = nodes.literal_block(body, body)
        literal['language'] = language.highlight    # For syntax hilighting.

        self.append(literal)    # Wrap the code block in our SingleSnippetNode

    @classmethod
    def register_to(cls, app):
        app.add_node(cls, html=(cls.html_visit, cls.html_depart))

    @staticmethod
    def html_visit(translator, node):
        translator.body.append('<li class="snippet" data-language="{}">'
                               .format(node['language']))

    @staticmethod
    def html_depart(translator, node):
        translator.body.append('</li>')


class SnippetNodeBuilder:
    """Builds snippet nodes by parsing a code file in the given language"""

    @staticmethod
    def parse(code_file, language, app):
        begin_string = "{} snippet-begin".format(language.line_comment)
        end_string = "{} snippet-end".format(language.line_comment)
        ignore_string = "{} snippet-ignore".format(language.line_comment)

        lineno = 0
        builder = None

        for line in code_file:
            lineno += 1
            if end_string in line and builder:
                yield builder.to_node()
                builder = None
            elif ignore_string not in line and builder:
                builder.append(line)
            elif begin_string in line:
                tokens = line.strip().split()
                if (len(tokens) > 2):
                    key = tokens[2]
                    builder = SnippetNodeBuilder(key, language, lineno)
                else:
                    app.warn("Missing snippet name in {} - line {} - {}"
                             .format(language.key, lineno, line))

    def __init__(self, key, language, lineno):
        self.key = key
        self.language = language
        self.lineno = lineno
        self._lines = []

    def append(self, line):
        self._lines.append(line.expandtabs(8))

    def to_node(self):
        lines = []
        first = True
        spaces = 0

        for line in self._lines:
            if first and len(line.strip()) == 0:   # Omit leading blank lines
                continue
            elif first:
                # Snip off leading indentation based on the whitespace found
                # on the first line
                spaces = len(line) - len(line.lstrip())
                first = False
            lines.append(line[spaces:])

        return SingleSnippetNode(self.key, self.language,
                                 lines, self.lineno)


def setup(app):
    """Magic function that registers this extension in sphinx"""
    app.add_config_value('snippet_language_list', [], 'env')

    SingleSnippetNode.register_to(app)
    SnippetDisplayNode.register_to(app)

    app.add_directive('snippet-display', SnippetDisplay)

    app.connect('builder-inited', initialize)
    app.connect('env-updated', read_snippet_content)
    app.connect('doctree-resolved', resolve_snippets)


def initialize(app):
    """Called once the builder object has been initialized."""
    env = app.builder.env
    env.snippet_all = []
    env.snippet_display = []
    env.snippet_languages = {}
    env.snippet_pulled = False

    if hasattr(env.config, 'snippet_language_list'):
        for lang_config in env.config.snippet_language_list:
            language_obj = Language(lang_config)
            key = language_obj.key
            env.snippet_languages[key] = language_obj
    else:
        ex = SphinxError("No configuration found for snippets languages! " +
                         "Please add snippet_language_list to conf.py")
        raise ex

def read_snippet_content(app, env):
    """Called when Sphinx has finished building the environment"""
    for language in env.snippet_languages.itervalues():
        read_local_snippets(app, env, language)
        if not env.snippet_pulled:
            read_remote_snippets(app, env, language)

    env.snippet_pulled = True

def read_local_snippets(app, env, language):
    if not hasattr(language, 'local_file'):
        app.verbose("No local snippet file configured for " + language.key)
        return

    filename = os.path.join(env.srcdir, language.local_file)
    try:
        nodes = SnippetNodeBuilder.parse(open(filename), language, app)
        env.snippet_all.extend(nodes)
    except IOError as e:
        app.warn("Can't read local snippet file: " + filename)

def read_remote_snippets(app, env, language):
    raw_url = language.get_raw_url()
    if not raw_url:
        app.verbose("No remote snippet location configured for " + language.key)
        return

    app.verbose("Getting snippets from " + raw_url)
    try:
        response = urllib2.urlopen(raw_url)
    except urllib2.URLError as e:
        app.warn("Failed to get remote snippets for {}: status {} - {}"
                 .format(language.key, e.code, e.reason))
        return

    nodes = SnippetNodeBuilder.parse(response, language, app)
    env.snippet_all.extend(nodes)


def resolve_snippets(app, doctree, docname):
    """ Called once the doctree has been resolved.
    Replace all SnippetDisplayNodes with a list of the relevant snippets."""

    env = app.builder.env
    langs = env.snippet_languages.keys()

    for node in doctree.traverse(SnippetDisplayNode):
        missing_languages = list(langs)
        for snippet in env.snippet_all:
            # Only process snippets with the right title
            if snippet['key'] != node['key']:
                continue

            missing_languages.remove(snippet['language'])
            node.append(snippet)    # TODO: sort these deterministically?
                                    # That will happen for free if all snippets
                                    # are downloaded from remotes

        if len(missing_languages) > 0:
            msg = "Missing languages for snippet key '{}': {}" \
                        .format(node['key'], missing_languages)
            app.warn(msg, (docname, 0))

