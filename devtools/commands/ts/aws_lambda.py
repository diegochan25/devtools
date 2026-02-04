from os import path, makedirs
import posixpath
from devtools.core.template import Template
from devtools.config.rule_set import JavaScriptRules
from devtools.core.decorators import abortable, requires
from devtools.core.command import Command
from devtools.core.io import die
from devtools.core.lang.json import CompilerOptions, PackageJson, TSConfigJson
from devtools.core.lib import case_map
from devtools.templates.ts.aws_lambda import ts_lambda

class TSLambda(Command):
    _name = 'lambda'
    _help = 'Create a TypeScript AWS Lambda function for Node 24.x runtime use.'

    @abortable
    @requires('path')
    def execute(self, **kwargs):
        abspath = path.abspath(path.normpath(kwargs.get('path')))
        basename = path.basename(abspath)
        rules = JavaScriptRules.generate()
        module = rules.module.name

        try: 
            makedirs(abspath)
        except FileExistsError:
            die(f"Directory at {abspath} already exists.")
        else:
            index_ts = ts_lambda()
            package_json = Template(
                filename = 'package.json',
                contents = PackageJson(
                name = case_map(basename).kebab,
                version = '0.1.0',
                type = 'commonjs' if module == 'commonjs' else 'module',
                private = True,
                main = posixpath.join('dist', 'index.js'),
                files=['dist'],
                scripts = {
                    'build': 'tsc'
                },
                engines={
                    'node': '>=18'
                }
            ).todict())
            tsconfig_json = Template(
                filename='tsconfig.json',
                contents=TSConfigJson(
                    include=['src/**/*.ts'],
                    compilerOptions=CompilerOptions(
                        target='esnext',
                        module='commonjs' if module == 'commonjs' else 'nodenext',
                        moduleResolution='node' if module == 'commonjs' else 'nodenext',
                        outDir='dist',
                        rootDir='src',
                        declaration=True,
                        declarationMap=False,
                        sourceMap=False,
                        removeComments=True,
                        strict=True,
                        esModuleInterop=True,
                    ),
                    exclude=['node_modules', 'dist']
                ).todict()
            )

            src = path.join(abspath, 'src')
            makedirs(src, exist_ok=True)
            index_ts.touch(at=src)
            package_json.touch(at=abspath)
            tsconfig_json.touch(at=abspath)
            
            if (pm := rules.package_manager).get_version() is not None:
                if pm.install('typescript', '@types/node', '@types/aws-lambda', at=abspath, dev=True):
                    die(f"Lambda function '{basename}' successfully created at {abspath}", fg='green', code=0)
                else:
                    die(f"Lambda function '{basename}' could not be created.")

    def construct(self, parent):
        parser = super().construct(parent)
        parser.add_argument('path', help='The path where the lambda function should be created. The last component of the path will be used for the function name')
        parser.set_defaults(fn=self.execute)
        return parser