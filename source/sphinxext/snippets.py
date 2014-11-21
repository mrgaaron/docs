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
        env = self.state.document.settings.env

        key = self.arguments[0]
        language = self.arguments[1]

        node = SingleSnippetNode()
        node['key'] = key
        node['language'] = language
        node['language-pretty'] = language.capitalize()
                        # TODO: don't require same language terms in directive

        code = u'\n'.join(self.content)
        literal = nodes.literal_block(code, code)
        literal['language'] = language     # For syntax hilighting.

        node.append(literal)    # Wrap the code block in our SingleSnippetNode

        # Register in the environment for use in the resolve stage
        if not hasattr(env, 'snippets_all'):
            env.snippets_all = []

        env.snippets_all.append({
            'docname': env.docname,
            'content': node
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

    for node in doctree.traverse(SnippetDisplayNode):
        content = []

        for snippet in env.snippets_all:
            # Only process snippets with the right title
            if snippet['content']['key'] != node['key']:
                continue

            node.append(snippet['content'])

        if len(node) == 0:
            msg = "No snippets found for key '{}'".format(node['key'])
            app.warn(msg, (docname, 0))


def setup(app):
    app.add_node(SnippetDisplayNode,
                 html=(visit_snippet_display, depart_snippet_display))
    app.add_node(SingleSnippetNode,
                 html=(visit_single_snippet, depart_single_snippet))

    app.add_directive('snippet-display', SnippetDisplay)
    app.add_directive('snippet', CodeSnippet)

    app.connect('env-purge-doc', purge_snippets)
    app.connect('doctree-resolved', resolve_snippets)
