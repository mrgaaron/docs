# Sphinx domain for TempoIQ API

from sphinx import addnodes
from sphinx.domains import Domain, ObjType
from sphinx.domains.python import _pseudo_parse_arglist
from sphinx.directives import ObjectDescription
from sphinx.locale import l_, _
from sphinx.roles import XRefRole
from sphinx.util.docfields import Field, GroupedField, TypedField
from sphinx.util.nodes import make_refnode

## TODO: create Objects:
# - Selector
# - PipelineFunction

class TempoIQObject(ObjectDescription):

    # If True, this object is callable and a desc_parameterlist is added
    has_arguments = False

    doc_field_types = [
        TypedField('arguments', label=l_('Arguments'),
                   names=('argument', 'arg', 'parameter', 'param'),
                   typerolename='class', typenames=('type', 'paramtype'),
                   can_collapse=True),
        Field('endpoint', label=l_('HTTP Endpoint'), has_arg=False,
              names=('endpoint', )),
        GroupedField('errors', label=l_('Errors'), rolename='err',
                     names=('throws', 'errors'),
                     can_collapse=True),
        Field('returnvalue', label=l_('Returns'), has_arg=False,
              names=('returns', 'return')),
        Field('returntype', label=l_('Return type'), has_arg=False,
              names=('rtype', ))

    ]

    def handle_signature(self, sig, signode):
        sig = sig.strip()
        if '(' in sig and sig[-1:] == ')':
            # name(arglist)
            prefix, arglist = sig.split('(', 1)
            prefix = prefix.strip()
            arglist = arglist[:-1].strip()
        else:
            prefix = sig
            arglist = None
        if '.' in prefix:
            nameprefix, name = prefix.rsplit('.', 1)
        else:
            nameprefix = None
            name = prefix

        objectname = self.env.temp_data.get('tempoiq:object')
        if nameprefix:
            if objectname:
                # someone documenting the method of an attribute of the current
                # object? shouldn't happen but who knows...
                nameprefix = objectname + '.' + nameprefix
            fullname = nameprefix + '.' + name
        elif objectname:
            fullname = objectname + '.' + name
        else:
            objectname = ''
            fullname = name

        signode['object'] = objectname
        signode['fullname'] = fullname

        if nameprefix:
            signode += addnodes.desc_addname(nameprefix + '.', nameprefix + '.')
        signode += addnodes.desc_name(name, name)
        if self.has_arguments:
            if not arglist:
                signode += addnodes.desc_parameterlist()
            else:
                _pseudo_parse_arglist(signode, arglist)

        return fullname, nameprefix

    def add_target_and_index(self, name_obj, sig, signode):
        objectname = self.options.get(
            'object', self.env.temp_data.get('tempoiq:object'))
        fullname = name_obj[0]

        if fullname not in self.state.document.ids:
            signode['names'].append(fullname)
            signode['ids'].append(fullname.replace('$', '_S_'))
            signode['first'] = not self.names
            self.state.document.note_explicit_target(signode)

            objects = self.env.domaindata['tempoiq']['objects']
            if fullname in objects:
                self.state_machine.reporter.warning(
                    'duplicate object description of %s, ' % fullname +
                    'other instance in ' +
                    self.env.doc2path(objects[fullname][0]),
                    line=self.lineno)
            objects[fullname] = self.env.docname, self.objtype

        indextext = self.get_index_text(objectname, name_obj)
        if indextext:
            self.indexnode['entries'].append(('single', indextext,
                                             fullname.replace('$', '_S_'),
                                             ''))

    def get_index_text(self, objectname, name_obj):
        name, obj = name_obj
        if self.objtype == 'method':
            return _('%s (%s method)') % (name, obj)
        elif self.objtype == 'class':
            return _('%s (class)') % name
        return ''


class TempoIQMethod(TempoIQObject):
    has_arguments = True

    doc_field_types = [
        TypedField('arguments', label=l_('Arguments'),
                   names=('argument', 'arg', 'parameter', 'param'),
                   typerolename='class', typenames=('type', 'paramtype'),
                   can_collapse=True),
        Field('endpoint', label=l_('HTTP Endpoint'), has_arg=False,
              names=('endpoint', )),
        GroupedField('errors', label=l_('Errors'), rolename='err',
                     names=('throws', 'errors'),
                     can_collapse=True),
        Field('returns', label=l_('Returns'), has_arg=False,
              names=('returns', 'return')),
        Field('cursored', label=l_("Cursored"), names=('cursored', 'cursor'),
              has_arg=False)
    ]


class TIQXRefRole(XRefRole):
    def process_link(self, env, refnode, has_explicit_title, title, target):
        # basically what sphinx.domains.python.PyXRefRole does
        refnode['tempoiq:object'] = env.temp_data.get('tempoiq:object')
        if not has_explicit_title:
            title = title.lstrip('.')      # only has a meaning for the target
            target = target.lstrip('~')    # only has a meaning for the title
            # if the first character is a tilde, don't display the module/class
            # parts of the contents
            if title[0:1] == '~':
                title = title[1:]
                dot = title.rfind('.')
                if dot != -1:
                    title = title[dot + 1:]
        # if the first character is a dot, search more specific namespaces
        # first, else search builtins first
        if target[0:1] == '.':
            target = target[1:]
            refnode['refspecific'] = True
        return title, target


class TempoIQDomain(Domain):
    name = 'tempoiq'
    label = 'TempoIQ'

    object_types = {
        'method': ObjType(l_('method'), 'method'),
        'class': ObjType(l_('class'), 'class'),
    }

    directives = {
        'method': TempoIQMethod,
        'class': TempoIQObject
    }

    roles = {
        'method': TIQXRefRole(fix_parens=True),
        'class': TIQXRefRole()
    }

    initial_data = {
        'objects': {},  # fullname -> docname, objtype
    }

    def clear_doc(self, docname):
        for fullname, (fn, _) in list(self.data['objects'].items()):
            if fn == docname:
                del self.data['objects'][fullname]

    def find_obj(self, env, obj, name, typ, searchorder=0):
        if name[-2:] == '()':
            name = name[:-2]
        objects = self.data['objects']
        newname = None
        if searchorder == 1:
            if obj and obj + '.' + name in objects:
                newname = obj + '.' + name
            else:
                newname = name
        else:
            if name in objects:
                newname = name
            elif obj and obj + '.' + name in objects:
                newname = obj + '.' + name
        return newname, objects.get(newname)

    def resolve_xref(self, env, fromdocname, builder, typ, target, node,
                     contnode):
        objectname = node.get('tempoiq:object')
        searchorder = node.hasattr('refspecific') and 1 or 0
        name, obj = self.find_obj(env, objectname, target, typ, searchorder)
        if not obj:
            return None
        return make_refnode(builder, fromdocname, obj[0],
                            name.replace('$', '_S_'), contnode, name)

    def get_objects(self):
        for refname, (docname, typ) in list(self.data['objects'].items()):
            yield refname, refname, typ, docname, \
                refname.replace('$', '_S_'), 1


def setup(app):
    app.add_domain(TempoIQDomain)
