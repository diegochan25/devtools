from src.config.rule_set import JavaScriptRules
from src.core.decorators import requires
from src.core.lib import case_map
from src.core.template import Template

@requires('name')
def nest_controller(**kwargs) -> Template:
    names = case_map(kwargs.get('name'))
    rules = JavaScriptRules.generate()
    module = rules.module

    return Template(
        filename = f"{names.kebab}.service.ts",
        contents = [
            module.import_stmt(source='@nestjs/common', imports=['Injectable']),
            '',
            f"@Injectable()",
            module.inline_export(f"class {names.pascal}Service {{"),
            '',
            '}'
        ]
    )