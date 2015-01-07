# Extension for embedding code examples in docs

import urllib2
from docutils import nodes

from sphinx.errors import SphinxError
from sphinx.directives.code import CodeBlock
from sphinx.util.compat import Directive

def initialize(app):
    env = app.builder.env
    env.snippet_all = []
    env.snippet_display = []
    env.snippet_languages = {}

    if hasattr(env.config, 'snippet_language_list'):
        for lang_config in env.config.snippet_language_list:
            language_obj = Language(lang_config)
            key = language_obj.key
            env.snippet_languages[key] = language_obj
    else:
        ex = SphinxError("No configuration found for snippets languages! " +
                         "Please add snippet_language_list to conf.py")
        raise ex


class CodeSnippet(Directive):
    """
    A code snippet in a language. Arguments: title, language
    Not used for remote snippets, just those defined in ReST
    """

    has_content = True
    required_arguments = 2
    optional_arguments = 0
    final_argument_whitespace = False

    def run(self):
        env = self.state.document.settings.env

        key = self.arguments[0]
        lang_id = self.arguments[1]

        # Custom pretty names and hilight schemes from config file
        language = env.snippet_languages[lang_id]

        node = SingleSnippetNode(key, language, self.content)

        env.snippet_all.append(node)

        return []   # Display nothing where snippets are defined


class Language(object):
    """Config should contain the following keys:
    'key', 'name', 'highlight', 'line_comment',
    'gh_repository', 'gh_branch', 'gh_path'"""

    def __init__(self, config):
        for key in config:
            setattr(self, key, config[key])

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
    pass


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


def visit_single_snippet(self, node):
    self.body.append('<li class="snippet" data-language="{}">'.format(node['language']))


def depart_single_snippet(self, node):
    self.body.append('</li>')


def visit_snippet_display(self, node):
    self.body.append('<div class="snippets-container" data-key="{}">'
                     .format(node['key']))

    self.body.append('<ul class="headings">')
    for child in node.children:
        self.body.append('<li><a class="heading" href="#" data-language="{}">{}</a></li>'
                         .format(child['language'], child['language-name']))
    self.body.append('</ul>')
    self.body.append('<ul class="snippets">')


def depart_snippet_display(self, node):
    self.body.append('</ul>')
    self.body.append('</div>')


def resolve_snippets(app, doctree, docname):
    # Replace all SnippetDisplayNodes with a list of the relevant snippets.

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

def pull_snippet_content(app, env):
    if hasattr(env, 'snippet_pulled') and env.snippet_pulled:
        app.verbose('Found cached snippets in environment, skipping download')
        return

    for language in env.snippet_languages.itervalues():
        pull_single_language(app, env, language)

    env.snippet_pulled = True


def pull_single_language(app, env, language):
    raw_url = language.get_raw_url()
    if not raw_url:
        app.verbose("Snippets: No remote location configured for " + language.key)
        return

    app.verbose("Getting snippets from " + raw_url)
    try:
        response = urllib2.urlopen(raw_url)
    except urllib2.URLError as e:
        app.warn("Failed to get remote snippets for {}: status {} - {}"
                 .format(language.key, e.code, e.reason))
        return

    begin_string = "{} snippet-start".format(language.line_comment)
    end_string = "{} snippet-end".format(language.line_comment)
    ignore_string = "{} snippet-ignore".format(language.line_comment)

    parsed = None
    lineno = 0
    for raw_line in response:
        lineno += 1
        if end_string in raw_line and parsed:
            app.debug("Ending parsing for {}".format(parsed.key))
            env.snippet_all.append(parsed.to_node())
            parsed = None
        elif ignore_string not in raw_line and parsed:
            parsed.append(raw_line)
        elif begin_string in raw_line:
            key = raw_line.strip().split()[2]
            parsed = TextInterpreter(key, language, lineno)


class TextInterpreter:
    def __init__(self, key, language, lineno):
        self.key = key
        self.language = language
        self.lines = []
        self.lineno = lineno

    def append(self, line):
        self.lines.append(line)

    def to_node(self):
        return SingleSnippetNode(self.key, self.language,
                                 self.lines, self.lineno)


def setup(app):
    app.add_config_value('snippet_language_list', [], 'env')
    app.add_node(SnippetDisplayNode,
                 html=(visit_snippet_display, depart_snippet_display))
    app.add_node(SingleSnippetNode,
                 html=(visit_single_snippet, depart_single_snippet))

    app.add_directive('snippet-display', SnippetDisplay)
    app.add_directive('snippet', CodeSnippet)

    app.connect('builder-inited', initialize)
    app.connect('env-updated', pull_snippet_content)
    app.connect('doctree-resolved', resolve_snippets)
