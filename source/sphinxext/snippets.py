# Directive for embedding code examples

from docutils import nodes

from sphinx.directives.code import CodeBlock
from sphinx.util.compat import Directive, make_admonition


class CodeSnippet(Directive):
    """
    A code snippet in a language. Arguments: title, language
    """

    has_content = True
    required_arguments = 2
    optional_arguments = 0
    final_argument_whitespace = False

    def run(self):
        env = self.state.document.settings.env

        key = self.arguments[0]
        lang = self.arguments[1]

        # Custom pretty names and hilight schemes from config file
        lang_config = env.config.snippet_langs.get(lang)
        if not lang_config:
            raise KeyError('Language "{}" not found in snippet_langs configuration'.format(lang))

        node = SingleSnippetNode()
        node['key'] = key
        node['language'] = lang
        node['language-pretty'] = lang_config['pretty']

        code = u'\n'.join(self.content)
        literal = nodes.literal_block(code, code)
        literal['language'] = lang_config['highlight']   # For syntax hilighting.

        node.append(literal)    # Wrap the code block in our SingleSnippetNode

        # Register in the environment for use in the resolve stage
        if not hasattr(env, 'snippets_all'):
            env.snippets_all = []

        env.snippets_all.append({
            'docname': env.docname,
            'content': node
        })

        return [literal]


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
    pass


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


# TODO: invalidate docs which include updated snippets
def purge_snippets(app, env, docname):
    if not hasattr(env, 'snippets_all'):
        return
    env.snippets_all = [snippet for snippet in env.snippets_all
                        if snippet['docname'] != docname]


def resolve_snippets(app, doctree, docname):
    # Replace all SnippetDisplayNodes with a list of the relevant snippets.

    env = app.builder.env
    langs = env.config.snippet_langs.keys()

    for node in doctree.traverse(SnippetDisplayNode):
        missing_languages = list(langs)
        for snippet in env.snippets_all:
            # Only process snippets with the right title
            if snippet['content']['key'] != node['key']:
                continue

            missing_languages.remove(snippet['content']['language'])
            node.append(snippet['content'])

        if len(missing_languages) > 0:
            msg = "Missing languages for snippet key '{}': {}" \
                        .format(node['key'], missing_languages)
            app.warn(msg, (docname, 0))

def check_snippets(app, env):
    langs = env.config.snippet_langs.keys()
    displayed = [node['key'] for node in env.snippets_display]
    for snippet in env.snippets_all:
        if snippet['content']['key'] not in displayed:
            msg = "Defined snippet never displayed: key={}, lang={}" \
                    .format(snippet['content']['key'],
                            snippet['content']['language'])
            app.warn(msg)

def setup(app):
    app.add_config_value('snippet_langs', [], 'env')
    app.add_node(SnippetDisplayNode,
                 html=(visit_snippet_display, depart_snippet_display))
    app.add_node(SingleSnippetNode,
                 html=(visit_single_snippet, depart_single_snippet))

    app.add_directive('snippet-display', SnippetDisplay)
    app.add_directive('snippet', CodeSnippet)

    app.connect('env-purge-doc', purge_snippets)
    app.connect('doctree-resolved', resolve_snippets)
    app.connect('env-updated', check_snippets)
