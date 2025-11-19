from devtools.config.cli_config import CLIConfig
from devtools.core.command import Command
from devtools.core.decorators import abortable
from devtools.core.io import die, s
from devtools.core.lib import parse, tostring

class ConfigSet(Command):
    _name = 'set'
    _help = 'Change the current value of a dot-separated CLI configuration option.'

    @abortable
    def execute(self, **kwargs):
        name: str = kwargs.get('name')
        value: str = kwargs.get('value')
        default: bool = kwargs.get('default', False)

        if not (bool(value) ^ bool(default)):
            die('Either provide a config dictionary, or use the --default flag to reset to default.')

        keys = name.split('.')
        result = False
        v = None

        if default:
            v = CLIConfig.deep_read(keys, default=True)
            result = CLIConfig.deep_write(keys, default=True) 
        else: 
            v = parse(value)
            result = CLIConfig.deep_write(keys, v)
        
        if not result:
            die(f"There was an error reading the config option {name}")
        die(
            s(f"Config option {name} successfuly changed to:", fg='white'),
            tostring(v),
            s('(default)', fg='white') if default else '',
            fg=None
        )
    
    def construct(self, parent):
        parser = super().construct(parent)
        parser.add_argument('name', help='The dot-separated key of the config option to change.')
        parser.add_argument('value', nargs='?', help='The new value to use.')
        parser.add_argument('--default', '-d', action='store_true', help='If set, will show the default value of the desired config option.')
        parser.set_defaults(fn=self.execute)
        return parser