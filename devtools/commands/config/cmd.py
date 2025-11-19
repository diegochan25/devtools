from devtools.core.command import Command

class ConfigCmd(Command):
    _name = 'config'
    _help = 'Commands related to the CLI\'s configuration options'

    def execute(self, **kwargs):
        return super().execute(**kwargs)
    
    def construct(self, parent):
        parser = super().construct(parent)
        return parser.add_subparsers()