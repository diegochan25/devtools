from os import path, makedirs
from devtools.core.template import Template
from devtools.config.rule_set import JavaScriptRules
from devtools.core.decorators import abortable, requires
from devtools.core.command import Command
from devtools.core.io import die
from devtools.core.lang.json import PackageJson
from devtools.core.lib import case_map
from devtools.templates.js.aws_lambda import js_lambda

class JSLambda(Command):
    _name = 'lambda'
    _help = 'Create an AWS-style Node 22.x Lambda Function package'

    @abortable
    @requires('path')
    def execute(self, **kwargs):
        abspath = path.abspath(path.normpath(kwargs.get('path')))
        basename = path.basename(abspath)
        rules = JavaScriptRules.generate()
        module = JavaScriptRules.generate().module.name

        try: 
            makedirs(abspath)
        except FileExistsError:
            die(f"Directory at {abspath} already exists.")
        else: 
            index_js = js_lambda()
            package_json = Template(
                filename = 'package.json',
                contents = PackageJson(
                name = case_map(basename).kebab,
                version = '0.1.0',
                type = 'commonjs' if module == 'commonjs' else 'module',
                private = True,
                keywords = ['AWS', 'Lambda', 'Node 22', 'CommonJS' if module == 'commonjs' else 'ES6', 'JavaScript'],
                main = index_js.filename
            ).todict())

            index_js.touch(at=abspath)
            package_json.touch(at=abspath)

            if (pm := rules.package_manager).get_version() is not None:
                if pm.install('@types/aws-lambda', at=abspath, dev=True):
                    die(f"Lambda function '{basename}' successfully created at {abspath}", fg='green', code=0)
                else:
                    die(f"Lambda function '{basename}' could not be created.")

    def construct(self, parent):
        parser = super().construct(parent)
        parser.add_argument('path', help='The path where the lambda function should be created. The last component of the path will be used for the function name')
        parser.set_defaults(fn=self.execute)
        return parser