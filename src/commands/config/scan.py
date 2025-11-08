from src.config.cli_config import CLIConfig
from src.core.command import Command
from src.core.decorators import abortable


class ConfigScan(Command):
    _name = 'scan'
    _help = 'Return a view of the CLI config\'s current settings.'

    @abortable
    def execute(self, **kwargs):
        default: bool = kwargs.get('default', False)
        print(CLIConfig.read(default=default).tostring())
    
    def construct(self, parent):
        parser = super().construct(parent)
        parser.add_argument('--default', '-d', action='store_true', help='If set, returns a view of the default configuration settings.')
        parser.set_defaults(fn=self.execute)
        return parser