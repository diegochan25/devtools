from os import makedirs, path
from devtools.config.rule_set import JavaScriptRules
from devtools.core.command import Command
from devtools.core.decorators import abortable, requires
from devtools.core.io import die
from devtools.core.lang.git import Git
from devtools.core.lang.js import Bun, Deno, NodeJS
from devtools.core.lib import case_map
from devtools.templates.nest.gitignore import gitignore_nest
from devtools.templates.nest.nest_controller import nest_controller
from devtools.templates.nest.nest_main import nest_main
from devtools.templates.nest.nest_module import nest_module
from devtools.templates.nest.nest_service import nest_service
from devtools.templates.nest.package_json import package_json_bun, package_json_deno, package_json_node
from devtools.templates.nest.tsconfig import tsconfig_bun, tsconfig_deno, tsconfig_node

class NestProject(Command):
    _name = 'project'
    _help = 'Create a NestJS project in the path specified, relative to the current working directory.'

    @abortable
    @requires('path')
    def execute(self, **kwargs):
        abspath: str = path.abspath(kwargs.get('path'))
        init: bool = kwargs.get('init', False)
        rules = JavaScriptRules.generate()
        runtime = rules.runtime
        pm = rules.package_manager

        if runtime.get_version() is None:
            die(f"{runtime.name} not found on this system.")

        if pm.get_version() is None:
            die(f"{pm.name} not found on this system.")

        
        project_names = case_map(path.basename(abspath))
        makedirs(abspath, exist_ok=True)

        tsconfig = (
            tsconfig_node() if runtime is NodeJS else 
            tsconfig_deno() if runtime is Deno else 
            tsconfig_bun()
        )

        package_json = (
            package_json_node(names=project_names) if runtime is NodeJS else 
            package_json_deno(names=project_names) if runtime is Deno else 
            package_json_bun(names=project_names)
        )

        gitignore = gitignore_nest()

        tsconfig.touch(at=abspath)
        package_json.touch(at=abspath)
        gitignore.touch(at=abspath)

        pm.install(
            '@nestjs/core',
            '@nestjs/common',
            '@nestjs/platform-express',
            'reflect-metadata',
            'rxjs',
            at=abspath
        )

        pm.install(
            '@nestjs/cli' if not runtime.name == 'Bun' else None,
            'tsconfig-paths' if not runtime.name == 'Bun' else None,
            '@nestjs/testing',
            '@types/express',
            '@types/node' if not runtime.name == 'Deno' else None,
            '@types/bun' if runtime.name == 'Bun' else None,
            'typescript',
            at=abspath,
            dev=True
        )

        names = case_map('app')

        service = nest_service(names=names)
        controller = nest_controller(names=names, use_service=True)
        module = nest_module(names=names, use_controller=True, use_service=True)
        main = nest_main()

        src_path = path.join(abspath, 'src')

        makedirs(src_path)

        service.touch(at=src_path)
        controller.touch(at=src_path)
        module.touch(at=src_path)
        main.touch(at=src_path)

        if init:
            if Git.get_version() is None:
                die("Git was not found on this system")
            Git.init(at=abspath)
            

        die(f"Project '{path.basename(abspath)}' successfully created at {abspath}.", fg='green')

    def construct(self, parent):
        parser = super().construct(parent)
        parser.add_argument('path', help='Relative path to the controller file to create.')
        parser.add_argument(
            '-i', '--init',
            action='store_true',
            help='If set, will also initialize a git repository at the project\'s root directory'
        )
        
        parser.set_defaults(fn=self.execute)
        return parser