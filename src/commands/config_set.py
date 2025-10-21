from argparse import _SubParsersAction
from src.config.cli_config import CLIConfig
from src.core.command import Command
from src.core.decorators import abortable
from src.core.io import die, done
from src.core.lib import deep_attr, deep_set, pretty

class ConfigSet(Command):
    _name = 'set'
    _help = 'Set the new value for a dot-separated configuration option'

    @abortable
    def execute(self, **kwargs):
        key: str = kwargs.get('key')
        value = kwargs.get('value')
        default: bool = kwargs.get('default', False)
        config_dict = CLIConfig.current().dict()
        keys = key.split('.')

        if not (bool(value) ^ bool(default)):
            die('Either provide a value to set the option to, or use the \'--default\' flag to reset its value.')

        if default:
            value = deep_attr(CLIConfig.default().dict(), keys)

        if deep_attr(config_dict, keys) is not None:
            result = deep_set(config_dict, keys, value)
            if result:
                #TODO write to the config.json
                done(f"{key} successfully set to {pretty(value)}")
            else:
                die('An unknown error occurred during the execution of the \'config set\' command.')
        else:
            die(f"{key} is not a valid attribute in the CLI config.")


        pass

    def construct(self, parent: _SubParsersAction) -> None:
        parser = super().construct(parent)
        parser.add_argument('key', help='The dot-separated key for the desired config option.')
        parser.add_argument('value', nargs='?', default=None, help='The new value to set the option to.')
        parser.add_argument('--default', '-d', action='store_true', help='If set, resets the provided config option to its default value.')
        parser.set_defaults(func=self.execute)