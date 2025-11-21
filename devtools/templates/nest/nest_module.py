from devtools.config.rule_set import JavaScriptRules
from devtools.core.decorators import requires
from devtools.core.lang.nest import NestJSModule
from devtools.core.lib import CaseMap, case_map
from devtools.core.template import Template

@requires('names')
def nest_module(**kwargs) -> Template:
    names: CaseMap = kwargs.get('names')
    rules = JavaScriptRules.generate()
    module = rules.module
    use_controller = bool(kwargs.get('use_controller', False))
    use_service = bool(kwargs.get('use_service', False))

    return Template(
        filename = f"{names.kebab}.module.ts",
        contents = [
            str(NestJSModule(
                names.pascal,
                stmts = [
                    module.import_stmt(source='@nestjs/common', imports=['Module']),
                    module.import_stmt(source=f"./{names.kebab}.controller", imports=[f"{names.pascal}Controller"]) if use_controller else None,
                    module.import_stmt(source=f"./{names.kebab}.service", imports=[f"{names.pascal}Service"]) if use_service else None,
                ],
                imports = [],
                controllers = [f"{names.pascal}Controller"] if use_controller else [],
                providers = [f"{names.pascal}Service"] if use_service else []
            ))
        ]
    )