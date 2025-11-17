from os import makedirs, path
from src.core.command import Command
from src.core.decorators import abortable, requires
from src.core.io import die
from src.core.lang.json import PackageJson
from src.templates.nest import nest_service


class NestService(Command):
    _name = 'service'
    _help = 'Create a NestJS service in the path specified, relative to the project\'s entry point.'

    @abortable
    @requires('path')
    def execute(self, **kwargs):
        relpath = path.abspath(kwargs.get('path'))
        flat = kwargs.get('flat', False)

        if (pkg_json_path := PackageJson.find(at=relpath)) is None:
            die('Could not find a package.json file in current or parent directories.')
        
        if (package_json := PackageJson.load(filepath=pkg_json_path)) is None:
            die(f"Unable to parse contents of file at {pkg_json_path} to JSON.")
        
        if (entry_point := package_json.main or package_json.module) is None:
            die(f"package.json at {pkg_json_path} does not specify an entry point.")

        filepath = path.join(path.dirname(pkg_json_path), path.dirname(entry_point), relpath)
        filename = path.basename(filepath)

        if flat:
            filepath = path.dirname(filepath)

        makedirs(filepath, exist_ok = True)

        service = nest_service(
            name = filename
        )
        
        if service.touch(at=filepath):
            die(f"Service {filename} successfully created at {filepath}", fg='green', code = 0)
        else:
            die(f"There was a problem creating a service at {filepath}")

    def construct(self, parent):
        parser = super().construct(parent)
        parser.add_argument('path', help='Relative path to the service file to create.')
        parser.add_argument(
            '-f', '--flat', 
            action='store_true', 
            help='If set, generates the service file without creating a new directory.'
        )

        parser.set_defaults(fn=self.execute)
        return parser