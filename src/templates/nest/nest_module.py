from src.config.rule_set import JavaScriptRules
from src.core.decorators import requires
from src.core.lib import case_map
from src.core.template import Template

@requires('name')
def nest_controller(**kwargs) -> Template:
    names = case_map(kwargs.get('name'))
    rules = JavaScriptRules.generate()
    module = rules.module
    use_controller = bool(kwargs.get('use_controller', False))
    use_service = bool(kwargs.get('use_service', False))

    return Template(
        filename = f"{names.kebab}.module.ts",
        contents = [
            module.import_stmt(source='@nestjs/common', imports=['Module']),
            module.import_stmt(source=f"./{names.kebab}.controller", imports=[f"{names.pascal}Controller"]) if use_controller else '',
            module.import_stmt(source=f"./{names.kebab}.service", imports=[f"{names.pascal}Service"]) if use_service else '',
            '',
            '@Module({',
            rules.t + 'imports: [],',
            rules.t + f"controllers: [{f"{names.pascal}Controller" if use_controller else ''}],",
            rules.t + f"providers: [{f"{names.pascal}Service" if use_service else ''}],",
            rules.t + 'exports: []' + rules.es5_c,
            '})',
            module.inline_export(f"class {names.pascal}Module {{ }}"),
        ]
    )