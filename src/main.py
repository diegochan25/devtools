import argparse
from src.commands.config_get import ConfigGet
from src.commands.config_passthrough import ConfigPassthrough
from src.commands.config_scan import ConfigScan
from src.commands.nest_controller import NestController
from src.commands.nest_passthrough import NestPassthrough

def main():
    root = argparse.ArgumentParser(prog='devtools', description='Developer tools for language and framework-related file creation utilities.')
    root_parsers = root.add_subparsers(dest='command')

    config = ConfigPassthrough().construct(root_parsers)
    ConfigScan().construct(config)
    ConfigGet().construct(config)

    nest = NestPassthrough().construct(root_parsers)
    NestController().construct(nest)

    args = root.parse_args()
    args.func(**vars(args))  

if __name__ == '__main__':
    main()

