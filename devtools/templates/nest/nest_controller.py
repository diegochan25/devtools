from devtools.config.rule_set import JavaScriptRules
from devtools.core.decorators import requires, throws
from devtools.core.lib import CaseMap
from devtools.core.template import Template

@requires('names')
@throws(AttributeError)
def nest_controller(**kwargs) -> Template:
    names: CaseMap = kwargs.get('names')
    rules = JavaScriptRules.generate()
    module = rules.module
    use_service = bool(kwargs.get('use_service', False))
    use_path = bool(kwargs.get('use_path', False))

    return Template(
        filename = f"{names.kebab}.controller.ts",
        contents = [
            module.import_stmt(source='@nestjs/common', imports=['Controller']),
            module.import_stmt(source=f"./{names.kebab}.service", imports=[f"{names.pascal}Service"]) if use_service else ''
            '',
            f"@Controller({f"{rules.q}{names.kebab}{rules.q}" if use_path else ''})",
            module.inline_export(f"class {names.pascal}Controller{rules.blk_s}{{"),
            f"{rules.t}constructor(private readonly {names.camel}Service: {names.pascal}Service){rules.blk_s}{{ }}" if use_service else '',
            '}'
        ]
    )