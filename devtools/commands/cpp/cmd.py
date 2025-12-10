from devtools.core.command import Command

class CppCmd(Command):
    _name = 'cpp'
    _help = 'Commands related to the C++ programming language'

    def execute(self, **kwargs):
        return super().execute(**kwargs)
    
    def construct(self, parent):
        parser = super().construct(parent)
        return parser.add_subparsers()