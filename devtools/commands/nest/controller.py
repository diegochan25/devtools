from os import makedirs, path
from devtools.config.rule_set import JavaScriptRules
from devtools.core.command import Command
from devtools.core.decorators import abortable, requires
from devtools.core.io import die, log
from devtools.core.lang.json import PackageJson
from devtools.core.lang.nest import NestJSModule
from devtools.core.lib import case_map
from devtools.templates.nest.nest_controller import nest_controller, nest_controller_spec_bun


class NestController(Command):
    _name = 'controller'
    _help = 'Create a NestJS controller in the path specified, relative to the project\'s entry point.'

    @abortable
    @requires('path')
    def execute(self, **kwargs):
        relpath: str = path.abspath(kwargs.get('path'))
        flat: bool = kwargs.get('flat', False)
        test: bool = kwargs.get('test', False)

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

        controller = nest_controller(
            names = names,
            use_service = path.isfile(path.join(filepath, f"{names.kebab}.service.ts")),
            use_path = True
        )

        classname = f"{names.pascal}Controller"
        
        if controller.touch(at=filepath):
            if (module_path := NestJSModule.exists(at=filepath)):
                with open(module_path, 'r', encoding='utf-8') as file:
                    module = NestJSModule.build(file.read())

                if classname not in module.controllers:
                    m_system = JavaScriptRules.generate().module
                    module.stmts.append(
                        m_system.import_stmt(
                            source=f"./{path.splitext(controller.filename)[0]}",
                            imports=[classname]
                        )
                    )
                    module.controllers.append(classname)

                with open(module_path, 'w', encoding='utf-8', newline='') as file:
                    file.write(str(module))
            else: 
                log(f"Consider creating a module to declare '{classname}' inside.", fg='yellow')

            if test:
                controller_spec = nest_controller_spec_bun(
                    names = names,
                    use_service = path.isfile(path.join(filepath, f"{names.kebab}.service.ts")),
                )
                controller_spec.touch(at=filepath)

            die(f"Controller '{classname}' successfully created at {filepath}", f"with test file {controller_spec.filename}" if test else '', fg='green', code = 0)
        else:
            die(f"There was a problem creating a controller at {filepath}")

    def construct(self, parent):
        parser = super().construct(parent)
        parser.add_argument('path', help='Relative path to the controller file to create.')
        parser.add_argument(
            '-f', '--flat', 
            action='store_true', 
            help='If set, generates the controller file without creating a new directory.'
        )
        parser.add_argument(
            '-t', '--test',
            action='store_true',
            help='If set, creates a .controller.spec.ts file alongside the .controller.ts file for unit testing.'
        )
        parser.set_defaults(fn=self.execute)
        return parser