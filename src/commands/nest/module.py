from os import getcwd, makedirs, path
from src.core.command import Command
from src.core.decorators import abortable, requires
from src.core.io import die
from src.core.lang.json import PackageJson
from src.core.lib import case_map
from src.templates.nest.nest_module import nest_module


class NestModule(Command):
    _name = 'module'
    _help = 'Create a NestJS module in the path specified, relative to the project\'s entry point.'

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

        module = nest_module(
            name = filename,
            use_controller = path.isfile(path.join(filepath, f"{case_map(filename).kebab}.controller.ts")),
            use_service = path.isfile(path.join(filepath, f"{case_map(filename).kebab}.service.ts")),
        )

        if module.touch(at=filepath):
            die(f"Module '{filename}' successfully created at {filepath}", fg='green', code = 0)
        else:
            die(f"There was a problem creating a module at {filepath}")

    def construct(self, parent):
        parser = super().construct(parent)
        parser.add_argument('path', help='Relative path to the module file to create.')
        parser.add_argument(
            '-f', '--flat', 
            action='store_true', 
            help='If set, generates the module file without creating a new directory.'
        )

        parser.set_defaults(fn=self.execute)
        return parser