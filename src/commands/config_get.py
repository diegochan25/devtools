from argparse import _SubParsersAction
from src.config.cli_config import CLIConfig
from src.core.command import Command
from src.core.decorators import abortable, requires
from src.core.io import die
from src.core.lib import deep_attr, pretty

class ConfigGet(Command):
    _name = 'get'
    _help = 'Return the current value of a dot-separated configuration option.'

    @abortable
    @requires('key')
    def execute(self, **kwargs):
        key: str = kwargs.get('key')
        default: bool = kwargs.get('default')
        config = CLIConfig.current().dict()
        value = deep_attr(config, key.split('.'))

        if value is not None:
            print(f"{key}: {pretty(value)} {f"(default: {pretty(deep_attr(CLIConfig.default().dict(), key.split('.')))})" if default else ''}")

        else:
            die(f"{key} is not a valid attribute in the CLI config.")

    def construct(self, parent: _SubParsersAction) -> None:
        parser = super().construct(parent)
        parser.add_argument('key', help='The dot-separated key for the desired config option.')
        parser.add_argument('--default', '-d', action='store_true', help='If set, displays the default value of the option, in addition to the currently stored one.')
        parser.set_defaults(func=self.execute)