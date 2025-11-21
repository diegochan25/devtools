from os import makedirs, path
from devtools.config.rule_set import JavaScriptRules
from devtools.core.command import Command
from devtools.core.decorators import abortable, requires
from devtools.core.io import die, log
from devtools.core.lang.json import PackageJson
from devtools.core.lang.nest import NestJSModule
from devtools.core.lib import case_map
from devtools.templates.nest.nest_service import nest_service


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

        names = case_map(filename)

        service = nest_service(
            names = names
        )
        
        classname = f"{names.pascal}Service"
        
        if service.touch(at=filepath):
            if (module_path := NestJSModule.exists(at=filepath)):
                with open(module_path, 'r', encoding='utf-8') as file:
                    module = NestJSModule.build(file.read())

                if classname not in module.providers:
                    m_system = JavaScriptRules.generate().module
                    module.stmts.append(
                        m_system.import_stmt(
                            source=f"./{path.splitext(service.filename)[0]}",
                            imports=[classname]
                        )
                    )
                    module.providers.append(classname)

                with open(module_path, 'w', encoding='utf-8', newline='') as file:
                    file.write(str(module))
            else: 
                log(f"Consider creating a module to declare '{classname}' inside.", fg='yellow')

            die(f"Service '{classname}' successfully created at {filepath}", fg='green', code = 0)
        else:
            die(f"There was a problem creating a controller at {filepath}")

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