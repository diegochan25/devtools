from argparse import ArgumentParser
from src.commands.config.cmd import ConfigCmd
from src.commands.config.get import ConfigGet
from src.commands.config.scan import ConfigScan
from src.commands.config.set import ConfigSet
from src.commands.js.cmd import JSCmd
from src.commands.js.aws_lambda import JSLambda
from src.commands.nest.cmd import NestCmd
from src.commands.nest.controller import NestController
from src.commands.nest.service import NestService

def main():
    cli = ArgumentParser(prog='devtools')
    commands = cli.add_subparsers(dest='commands')

    config = ConfigCmd().construct(commands)
    js = JSCmd().construct(commands)
    nest = NestCmd().construct(commands)

    ConfigScan().construct(config)
    ConfigGet().construct(config)
    ConfigSet().construct(config)

    JSLambda().construct(js)

    NestController().construct(nest)
    NestService().construct(nest)

    args = cli.parse_args()
    
    if hasattr(args, 'fn'):
        args.fn(**vars(args))

if __name__ == '__main__':
    main()