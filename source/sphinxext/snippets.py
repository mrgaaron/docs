# Directive for embedding code examples

from docutils import nodes

from sphinx.directives.code import CodeBlock
from sphinx.util.compat import Directive, make_admonition


class CodeSnippet(Directive):    # Arguments: title, language
    """
    A code snippet in a language.
    """

    has_content = True
    required_arguments = 2
    optional_arguments = 0
    final_argument_whitespace = False

    def run(self):
        key = self.arguments[0]
        language = self.arguments[1]

        env = self.state.document.settings.env

        code = u'\n'.join(self.content)
        literal = nodes.literal_block(code, code)
        literal['key'] = key
        literal['language'] = language     # For syntax hilighting.
        literal['language-pretty'] = language.capitalize()
                        # TODO: don't require same language terms in directive

        # Register in the environment for use in the resolve stage
        if not hasattr(env, 'snippets_all'):
            env.snippets_all = []

        env.snippets_all.append({
            'docname': env.docname,
            'key': key,
            'langugage': language,
            'content': literal
        })

        return [literal]


class SnippetDisplay(Directive):  # Param: title, prints all snippets related to that title
    """
    Directive to insert all snippets with a given title.
    """

    required_arguments = 1

    def run(self):
        key = self.arguments[0]

        node = SnippetDisplayNode()
        node['key'] = key

        return [node]


class SnippetDisplayNode(nodes.General, nodes.Element):
    pass


def visit_snippet_display(self, node):
    self.body.append('<div class="snippets" data-key="{}">'
                     .format(node['key']))

    self.body.append('<div class="headings">')
    for child in node.children:
        self.body.append('<div data-language="{}">{}</div>'
                         .format(child['language'], child['language-pretty']))
    self.body.append('</div>')


def depart_snippet_display(self, node):
    self.body.append('</div>')


def purge_snippets(app, env, docname):
    if not hasattr(env, 'snippets_all'):
        return
    env.snippets_all = [snippet for snippet in env.snippets_all
                        if snippet['docname'] != docname]


def resolve_snippets(app, doctree, docname):
    # Replace all SnippetDisplayNodes with a list of the relevant snippets.

    env = app.builder.env

    for node in doctree.traverse(SnippetDisplayNode):
        content = []

        for snippet in env.snippets_all:
            # Only process snippets with the right title
            if snippet['key'] != node['key']:
                continue

            node.append(snippet['content'])

        if len(node) == 0:
            msg = "No snippets found for key '{}'".format(node['key'])
            app.warn(msg, (docname, 0))


def setup(app):
    app.add_node(SnippetDisplayNode,
                 html=(visit_snippet_display, depart_snippet_display))

    app.add_directive('snippet-display', SnippetDisplay)
    app.add_directive('snippet', CodeSnippet)

    app.connect('env-purge-doc', purge_snippets)
    app.connect('doctree-resolved', resolve_snippets)
