from src.core.command import Command

class JSCmd(Command):
    _name = 'js'
    _help = 'JavaScript and Node.js commands.'
    def execute(self, **kwargs):
        return super().execute(**kwargs)
    
    def construct(self, parent):
        return super().construct(parent).add_subparsers()