from devtools.core.command import Command

class TSCmd(Command):
    _name = 'ts'
    _help = 'TypeScript commands.'
    def execute(self, **kwargs):
        return super().execute(**kwargs)
    
    def construct(self, parent):
        return super().construct(parent).add_subparsers()