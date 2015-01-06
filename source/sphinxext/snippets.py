# Directive for embedding code examples

import urllib2
from docutils import nodes

from sphinx.directives.code import CodeBlock
from sphinx.util.compat import Directive, make_admonition


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
        language = Language.lookup(lang_id, env.config.snippet_langs)

        node = SingleSnippetNode(key, language, self.content)

        # Register in the environment for use in the resolve stage
        if not hasattr(env, 'snippets_all'):
            env.snippets_all = []

        env.snippets_all.append(node)

        return []   # Display nothing where snippets are defined


class Language(dict):
    def __init__(self, key, config):
        super(Language, self).__init__()
        self.update(config)
        self['key'] = key

    def get_raw_url(self):
        return "https://raw.githubusercontent.com/{}/{}/{}" \
                    .format(self.get('gh_repository'),
                            self.get('gh_branch'),
                            self.get('gh_path'))

    @staticmethod
    def lookup(key, table):
        """Static method to generate a Language object from a map
        of key=>config"""
        config = table.get(key)

        if not config:
            raise KeyError('Unknown language: "{}"'.format(key))

        return Language(key, config)


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

        if not hasattr(env, 'snippets_display'):
            env.snippets_display = []
        env.snippets_display.append(node)

        return [node]


class SnippetDisplayNode(nodes.General, nodes.Element):
    pass


class SingleSnippetNode(nodes.General, nodes.Element):
    def __init__(self, key, language, content=""):
        super(SingleSnippetNode, self).__init__()
        self['key'] = key
        self['language'] = language['key']
        self['language-pretty'] = language['pretty']

        # Support strings, or a list of strings
        if isinstance(content, basestring):
            body = content
        else:
            body = u'\n'.join([line.rstrip() for line in content])

        literal = nodes.literal_block(body, body)
        literal['language'] = language['highlight']   # For syntax hilighting.

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
                         .format(child['language'], child['language-pretty']))
    self.body.append('</ul>')
    self.body.append('<ul class="snippets">')


def depart_snippet_display(self, node):
    self.body.append('</ul>')
    self.body.append('</div>')


def resolve_snippets(app, doctree, docname):
    # Replace all SnippetDisplayNodes with a list of the relevant snippets.

    env = app.builder.env
    langs = env.config.snippet_langs.keys()

    for node in doctree.traverse(SnippetDisplayNode):
        missing_languages = list(langs)
        for snippet in env.snippets_all:
            # Only process snippets with the right title
            if snippet['key'] != node['key']:
                continue

            missing_languages.remove(snippet['language'])
            node.append(snippet)

        if len(missing_languages) > 0:
            msg = "Missing languages for snippet key '{}': {}" \
                        .format(node['key'], missing_languages)
            app.warn(msg, (docname, 0))

def pull_snippet_content(app, env):
    if hasattr(env, 'snippets_pulled') and env.snippets_pulled:
        app.verbose('Found cached snippets in environment, skipping download')
        return

    if not hasattr(env, 'snippets_all'):
        env.snippets_all = []

    for language_id in env.config.snippet_langs:
        language = Language.lookup(language_id, env.config.snippet_langs)
        pull_single_language(app, env, language)

    env.snippets_pulled = True

    #displayed = [node['key'] for node in env.snippets_display]
    #for snippet in env.snippets_all:
    #    if snippet['content']['key'] not in displayed:
    #        msg = "Defined snippet never displayed: key={}, lang={}" \
    #                .format(snippet['content']['key'],
    #                        snippet['content']['language'])
    #        app.warn(msg)

def pull_single_language(app, env, language):
    raw_url = language.get_raw_url()
    app.verbose("Getting snippets from " + raw_url)
    try:
        response = urllib2.urlopen(raw_url)
    except urllib2.URLError as e:
        app.warn("Failed to get remote snippets for {}: status {} - {}"
                 .format(language['key'], e.code, e.reason))
        return

    begin_string = "{} snippet-start".format(language['comment'])
    end_string = "{} snippet-end".format(language['comment'])
    ignore_string = "{} snippet-ignore".format(language['comment'])

    parsed = None
    # TODO: add line number in SingleSnippetNode
    for raw_line in response:
        if end_string in raw_line and parsed:
            app.debug("Ending parsing for {}".format(parsed.key))
            env.snippets_all.append(parsed.to_node())
            parsed = None
        elif ignore_string not in raw_line and parsed:
            parsed.append(raw_line)
        elif begin_string in raw_line:
            key = raw_line.strip().split()[2]
            app.verbose("Found begin_string for key [{}] in:".format(key))
            app.verbose(raw_line)
            parsed = TextInterpreter(key, language)


class TextInterpreter:
    def __init__(self, key, language):
        self.key = key
        self.language = language
        self.lines = []

    def append(self, line):
        self.lines.append(line)

    def to_node(self):
        return SingleSnippetNode(self.key, self.language, self.lines)


def setup(app):
    app.add_config_value('snippet_langs', [], 'env')
    app.add_node(SnippetDisplayNode,
                 html=(visit_snippet_display, depart_snippet_display))
    app.add_node(SingleSnippetNode,
                 html=(visit_single_snippet, depart_single_snippet))

    app.add_directive('snippet-display', SnippetDisplay)
    app.add_directive('snippet', CodeSnippet)

    app.connect('env-updated', pull_snippet_content)
    app.connect('doctree-resolved', resolve_snippets)
