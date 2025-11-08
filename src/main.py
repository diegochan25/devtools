from argparse import ArgumentParser
from src.commands.config.cmd import ConfigCmd
from src.commands.config.get import ConfigGet
from src.commands.config.scan import ConfigScan
from src.commands.config.set import ConfigSet
from src.commands.nest.cmd import NestCmd
from src.commands.nest.controller import NestController

def main():
    cli = ArgumentParser(prog='devtools')
    commands = cli.add_subparsers(dest='commands')

    config = ConfigCmd().construct(commands)
    nest = NestCmd().construct(commands)

    ConfigScan().construct(config)
    ConfigGet().construct(config)
    ConfigSet().construct(config)

    NestController().construct(nest)

    args = cli.parse_args()
    
    if hasattr(args, 'fn'):
        args.fn(**vars(args))

if __name__ == '__main__':
    main()