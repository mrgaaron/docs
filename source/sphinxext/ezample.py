# Directive for embedding code examples

from docutils import nodes

from sphinx.directives.code import CodeBlock
from sphinx.util.compat import Directive, make_admonition


class EzampleSnippet(CodeBlock):    # Needs params: title, language
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

        if not hasattr(env, 'ezample_all'):
            env.ezample_all = []
        env.ezample_all.append({
            'docname': env.docname,
            'title': title,
            'langugage': language,
            'content': self.content
        })
        self.arguments = [title]
        CodeBlock.run(self)


class EzampleBlock(Directive):  # Param: title, prints all snippets related to that title
    pass


class ezample_block(nodes.General, nodes.Element):
    pass


def purge_ezamples(app, env, docname):
    if not hasattr(env, 'ezample_all'):
        return
    env.ezample_all = [ezample for ezample in env.ezample_all
                       if ezample['docname'] != docname]


def setup(app):
    app.add_config_value('ezample_source_dir', 'source/include/code', False)

    app.add_node(ezample_block)    # TODO: add visit/depart functions for Theme hooks

    app.add_directive('ezample', EzampleBlock)
    app.add_directive('ezample-snippet', EzampleSnippet)

    app.connect('env-purge-doc', purge_ezamples)
