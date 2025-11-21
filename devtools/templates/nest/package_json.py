from devtools.config.rule_set import JavaScriptRules
from devtools.core.decorators import requires
from devtools.core.lang.json import PackageJson
from devtools.core.lib import CaseMap
from devtools.core.template import Template

@requires('names')
def package_json_node(**kwargs) -> Template:
    names: CaseMap = kwargs.get('names')
    m_name = JavaScriptRules.generate().module.name
    return Template(
        filename='package.json',
        contents = PackageJson(
            name = names.kebab,
            version = '0.1.0',
            private = True,
            type = 'commonjs' if m_name == 'commonjs' else 'module' if m_name == 'es6' else None,
            main = 'src/main.ts',
            scripts = {
                'build': 'nest build',
                'start': 'nest start',
                'start:dev': 'nest start --watch',
                'test': 'node --test \\"**/*.test.{js,ts}\\" \\"**/*.spec.{js,ts}\\"'
            }
        ).todict()
    )

@requires('names')
def package_json_deno(**kwargs) -> Template:
    names: CaseMap = kwargs.get('names')
    m_name = JavaScriptRules.generate().module.name
    return Template(
        filename='package.json',
        contents = PackageJson(
            name = names.kebab,
            version = '0.1.0',
            private = True,
            type = 'commonjs' if m_name == 'commonjs' else 'module' if m_name == 'es6' else None,
            main = 'src/main.ts',
            scripts = {
                'start': 'deno run --allow-net --allow-read --allow-env src/main.ts',
                'start:dev': 'deno run --watch --allow-net --allow-read --allow-env src/main.ts',
            }
        ).todict()
    )

@requires('names')
def package_json_bun(**kwargs) -> Template:
    names: CaseMap = kwargs.get('names')
    m_name = JavaScriptRules.generate().module.name
    return Template(
        filename='package.json',
        contents = PackageJson(
            name = names.kebab,
            version = '0.1.0',
            private=True,
            type = 'commonjs' if m_name == 'commonjs' else 'module' if m_name == 'es6' else None,
            module = 'src/main.ts',
            scripts = {
                'start': 'bun src/main.ts',
                'start:dev': 'bun --watch src/main.ts',
                'test': 'bun test'
            }
        ).todict()
    )