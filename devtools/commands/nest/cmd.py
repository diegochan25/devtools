from devtools.core.command import Command

class NestCmd(Command):
    _name = 'nest'
    _help = 'Commands related to NestJS, the TypeScript server-side application framework.'

    def execute(self, **kwargs):
        return super().execute(**kwargs)
    
    def construct(self, parent):
        parser = super().construct(parent)
        return parser.add_subparsers()