from jinja2 import nodes
from jinja2.ext import Extension
from jinja2.utils import next

class AbifyExtension(Extension):
    """Adds support for a abify block in Jinja."""
    tags = set(['abify'])

    def parse(self, parser):
        node = nodes.Scope(lineno=next(parser.stream).lineno)
        assignments = []
        while parser.stream.current.type != 'block_end':
            lineno = parser.stream.current.lineno
            if assignments:
                parser.stream.expect('comma')
            target = parser.parse_assign_target()
            parser.stream.expect('assign')
            expr = parser.parse_expression()
            assignments.append(nodes.Assign(target, expr, lineno=lineno))
        node.body = assignments + \
            list(parser.parse_statements(('name:endabify',),
                                         drop_needle=True))
        return node
