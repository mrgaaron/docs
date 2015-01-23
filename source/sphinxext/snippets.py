# Extension for embedding code examples in docs

import urllib2
import os.path
import re
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

    def has_remote_source(self):
        return (hasattr(self, 'gh_repository') and
                hasattr(self, 'gh_branch') and
                hasattr(self, 'gh_path'))

    def get_remote_url(self):
        if not self.has_remote_source():
            return None

        return "https://raw.githubusercontent.com/{}/{}/{}" \
               .format(self.gh_repository,
                       self.gh_branch,
                       self.gh_path)

    def get_pretty_remote_url(self, lineno=None):
        if not self.has_remote_source():
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
    def __init__(self, key, language, content="", lineno=None, remote=False):
        super(SingleSnippetNode, self).__init__()
        self['key'] = key
        self['language'] = language.key
        self['language-name'] = language.name

        if remote:
            self['source-url'] = language.get_pretty_remote_url(lineno)

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
        translator.body.append(
            '<li class="snippet" data-language="{}" data-source="{}">'
            .format(node.get('language'), node.get('source-url', '')))

    @staticmethod
    def html_depart(translator, node):
        translator.body.append('</li>')


class SnippetNodeBuilder:
    """Builds snippet nodes by parsing a code file in the given language"""

    @staticmethod
    def parse(code_file, language, app, remote=False):
        begin_rexp = re.compile(language.line_comment + r"\s*snippet-begin")
        end_rexp = re.compile(language.line_comment + r"\s*snippet-end")
        ignore_rexp = re.compile(language.line_comment + r"\s*snippet-ignore")

        lineno = 0
        builder = None

        for line in code_file:
            lineno += 1
            if builder and end_rexp.search(line):
                yield builder.to_node()
                builder = None
            elif builder and not ignore_rexp.search(line):
                builder.append(line)
            elif begin_rexp.search(line):
                tokens = line.strip().split()
                if (len(tokens) > 2):
                    key = tokens[2]
                    builder = SnippetNodeBuilder(key, language, lineno, remote)
                else:
                    app.warn("Missing snippet name in {} - line {} - {}"
                             .format(language.key, lineno, line))

    def __init__(self, key, language, lineno, remote=False):
        self.key = key
        self.language = language
        self.lineno = lineno
        self.remote = remote
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
                                 lines, self.lineno, remote=self.remote)


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
    env.snippet_languages = []
    env.snippet_pulled = False

    if hasattr(env.config, 'snippet_language_list'):
        for lang_config in env.config.snippet_language_list:
            language_obj = Language(lang_config)
            env.snippet_languages.append(language_obj)
    else:
        ex = SphinxError("No configuration found for snippets languages! " +
                         "Please add snippet_language_list to conf.py")
        raise ex

def read_snippet_content(app, env):
    """Called when Sphinx has finished building the environment"""
    for language in env.snippet_languages:
        read_local_snippets(app, env, language)
        if not env.snippet_pulled:
            read_remote_snippets(app, env, language)

    env.snippet_pulled = True

def read_local_snippets(app, env, language):
    if not hasattr(language, 'local_file'):
        app.debug("No local snippet file configured for " + language.key)
        return

    filename = os.path.join(env.srcdir, language.local_file)
    try:
        nodes = SnippetNodeBuilder.parse(open(filename), language, app, remote=False)
        env.snippet_all.extend(nodes)
    except IOError as e:
        app.warn("Can't read local snippet file: " + filename)

def read_remote_snippets(app, env, language):
    url = language.get_remote_url()
    if not url:
        app.debug("No remote snippet location configured for " + language.key)
        return

    try:
        response = urllib2.urlopen(url)
    except urllib2.URLError as e:
        app.warn("Failed to get remote snippets for {} ({}): {}"
                 .format(language.key, url, e.reason))
        return
    app.debug("Successfully downloaded remote snippets for {} ({}) "
              .format(language.key, url))

    nodes = SnippetNodeBuilder.parse(response, language, app, remote=True)
    env.snippet_all.extend(nodes)


def resolve_snippets(app, doctree, docname):
    """ Called once the doctree has been resolved.
    Replace all SnippetDisplayNodes with a list of the relevant snippets."""

    env = app.builder.env
    all_langs = [language.key for language in env.snippet_languages]

    for node in doctree.traverse(SnippetDisplayNode):
        missing_languages = list(all_langs)
        for snippet in env.snippet_all:
            # Only process snippets with the right title
            if snippet['key'] != node['key']:
                continue
            if snippet['language'] not in missing_languages:
                app.warn('Found multiple snippets with key "{}" and language "{}"'
                         .format(snippet['key'], snippet['language']))
                continue

            missing_languages.remove(snippet['language'])
            node.append(snippet)

        if len(missing_languages) > 0:
            msg = "Missing languages for snippet key '{}': {}" \
                        .format(node['key'], missing_languages)
            app.warn(msg, (docname, 0))

