from argparse import _SubParsersAction
from src.config.cli_config import CLIConfig
from src.core.command import Command
from src.core.lib import pretty


class ConfigScan(Command):
    _name = 'scan'
    _help = 'Get a readable view of the CLI\'s current configuration.'
    def execute(self, **_):
        print(pretty(CLIConfig.current().dict()))
        
    def construct(self, parent: _SubParsersAction) -> None:
        parser = super().construct(parent)
        parser.set_defaults(func=self.execute)