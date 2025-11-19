from src.config.rule_set import JavaScriptRules
from src.core.decorators import requires
from src.core.lib import CaseMap
from src.core.template import Template

@requires('names')
def nest_service(**kwargs) -> Template:
    names: CaseMap = kwargs.get('names')
    rules = JavaScriptRules.generate()
    module = rules.module

    return Template(
        filename = f"{names.kebab}.service.ts",
        contents = [
            module.import_stmt(source='@nestjs/common', imports=['Injectable']),
            '',
            f"@Injectable()",
            module.inline_export(f"class {names.pascal}Service{rules.blk_s}{{"),
            rules.t,
            '}'
        ]
    )