from src.config.cli_config import CLIConfig
from src.core.command import Command
from src.core.decorators import abortable
from src.core.io import die
from src.core.lib import tostring

class ConfigGet(Command):
    _name = 'get'
    _help = 'Return a view of a dot-separated CLI configuration option.'

    @abortable
    def execute(self, **kwargs):
        name: str = kwargs.get('name')
        default: bool = kwargs.get('default', False)
        keys = name.split('.')

        if not (result := CLIConfig.deep_read(keys, default=default)):
            die(f"There was an error reading the config option {name}")
        print(tostring({ name: result }))
    
    def construct(self, parent):
        parser = super().construct(parent)
        parser.add_argument('name', help='The dot-separated key of the config option to change.')
        parser.add_argument('--default', '-d', action='store_true', help='If set, will show the default value of the desired config option.')
        parser.set_defaults(fn=self.execute)
        return parser