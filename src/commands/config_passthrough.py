import argparse
from src.core.command import Command


class ConfigPassthrough(Command):
    _name = 'config'
    _help = 'Utilities related to the CLI\'s configuration'

    def execute(self): 
        return super().execute()

    def construct(self, parent: argparse._SubParsersAction) -> argparse._SubParsersAction:
        parser = super().construct(parent=parent)
        return parser.add_subparsers(dest='subcommands')