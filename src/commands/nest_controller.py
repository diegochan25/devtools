import argparse
from os import path
from src.core.command import Command
from src.core.decorators import abortable, requires
from src.core.io import die, done
from src.core.js import JS
from src.core.namecase import case_map
from src.templates.nest import nest_controller

class NestController(Command):
    _name = 'controller'
    _help = 'Create a NestJS controller in the path specified, relative to the project\'s entry point.'

    @abortable
    @requires('path')
    def execute(self, **kwargs):
        super().execute()
        rel_path = path.normpath(kwargs.get('path'))
        flat = kwargs.get('flat', False)

        package_json_path = JS.find_package_json()
        if package_json_path is None:
            die('Could not find a package.json file in current or parent directories.')

        package_json = JS.load_package_json(package_json_path)
        if package_json is None:
            die(f"Unable to parse contents of file at {package_json_path} to JSON.")
        
        entry_point = package_json.main or package_json.module
        if not entry_point:
            die('Entry point not specified in package.json')
        
        file_path = path.join(path.dirname(package_json_path), path.dirname(entry_point), rel_path)
        file_name = path.basename(rel_path)
        names = case_map(file_name)

        if flat:
            file_path = path.dirname(file_path)

        controller = nest_controller(
            name=names.kebab, 
            use_service=path.isfile(path.join(file_path, f"{names.kebab}.service.ts"))
        )

        controller.write(at=file_path)
        done(f"Controller successfully created at {file_path}!")
            

    def construct(self, parent: argparse._SubParsersAction) -> None:
        parser = super().construct(parent)
        parser.add_argument('path', help='Relative path to the controller file to create.')
        parser.add_argument(
            '--flat', '-f', 
            action='store_true', 
            help='If set, generates the controller file without creating a new directory.'
        )
        parser.set_defaults(func=self.execute)