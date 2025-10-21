import argparse
from src.core.command import Command


class NestPassthrough(Command):
    _name = 'nest'
    _help = 'Utilities related to the NestJS JavaScript backend framework'

    def execute(self): 
        return super().execute()

    def construct(self, parent: argparse._SubParsersAction) -> argparse._SubParsersAction:
        parser = super().construct(parent=parent)
        return parser.add_subparsers(dest='subcommands')