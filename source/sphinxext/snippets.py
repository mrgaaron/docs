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
        title = self.arguments[0]
        language = self.arguments[1]

        env = self.state.document.settings.env

        literal = nodes.literal_block(self.content, self.content)
        literal['language'] = language     # For syntax hilighting.
                        # TODO: don't require same language terms in directive

        text = "Snippet: title({}), language({})".format(title, language)
        heading = nodes.paragraph(text, text)
        register_nodes = [heading] + literal

        print("registering" + text)
        # Register in the environment for use in the resolve stage
        if not hasattr(env, 'snippets_all'):
            env.snippets_all = []

        env.snippets_all.append({
            'docname': env.docname,
            'title': title,
            'langugage': language,
            'heading': heading,
            'content': literal
        })

        return register_nodes


class SnippetDisplay(Directive):  # Param: title, prints all snippets related to that title
    """
    Directive to insert all snippets with a given title.
    """

    required_arguments = 1

    def run(self):
        title = self.arguments[0]

        node = SnippetDisplayNode()
        node['title'] = title

        return [node]


class SnippetDisplayNode(nodes.General, nodes.Element):
    pass


def purge_snippets(app, env, docname):
    if not hasattr(env, 'snippets_all'):
        return
    env.snippets_all = [snippet for snippet in env.snippets_all
                        if snippet['docname'] != docname]


# TODO: translate this from todo example to this extension
def resolve_snippets(app, doctree, fromdocname):
    # Replace all SnippetDisplayNodes with a list of the relevant snippets.

    env = app.builder.env

    for node in doctree.traverse(SnippetDisplayNode):
        content = []

        for snippet in env.snippets_all:
            # Only process snippets with the right title
            if snippet['title'] != node['title']:
                continue

            # Insert into the todolist
            content.append(snippet['heading'])
            content.append(snippet['content'])

        if len(content) > 0:
            node.replace_self(content)
        else:
            msg = "No snippets found for title({})".format(node['title'])
            node.replace_self([nodes.paragraph(msg, msg)])


def setup(app):
    app.add_node(SnippetDisplayNode)    # TODO: add visit/depart functions for Theme hooks

    app.add_directive('snippet-display', SnippetDisplay)
    app.add_directive('snippet', CodeSnippet)

    app.connect('env-purge-doc', purge_snippets)
    app.connect('doctree-resolved', resolve_snippets)
