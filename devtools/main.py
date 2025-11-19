from argparse import ArgumentParser
from devtools.commands.config.cmd import ConfigCmd
from devtools.commands.config.get import ConfigGet
from devtools.commands.config.scan import ConfigScan
from devtools.commands.config.set import ConfigSet
from devtools.commands.js.cmd import JSCmd
from devtools.commands.js.aws_lambda import JSLambda
from devtools.commands.nest.cmd import NestCmd
from devtools.commands.nest.controller import NestController
from devtools.commands.nest.module import NestModule
from devtools.commands.nest.service import NestService

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

    NestModule().construct(nest)
    NestController().construct(nest)
    NestService().construct(nest)

    args = cli.parse_args()
    
    if hasattr(args, 'fn'):
        args.fn(**vars(args))

if __name__ == '__main__':
    main()