from devtools.config.rule_set import JavaScriptRules
from devtools.core.decorators import requires, throws
from devtools.core.lib import CaseMap
from devtools.core.template import Template

@requires('names')
@throws(AttributeError)
def nest_controller(**kwargs) -> Template:
    names: CaseMap = kwargs.get('names')
    rules = JavaScriptRules.generate()
    use_service = bool(kwargs.get('use_service', False))
    use_path = bool(kwargs.get('use_path', False))

    module = rules.module
    q = rules.q
    t = rules.t

    return Template(
        filename = f"{names.kebab}.controller.ts",
        contents = [
            module.import_stmt(source='@nestjs/common', imports=['Controller']),
            module.import_stmt(source=f"./{names.kebab}.service", imports=[f"{names.pascal}Service"]) if use_service else None,
            '',
            f"@Controller({f"{q}{names.kebab}{q}" if use_path else ''})",
            module.inline_export(f"class {names.pascal}Controller{rules.blk_s}{{"),
            f"{t}constructor(private readonly {names.camel}Service: {names.pascal}Service){rules.blk_s}{{ }}" if use_service else None,
            '}'
        ]
    )

@requires('names')
def nest_controller_spec_bun(**kwargs) -> Template:
    names: CaseMap = kwargs.get('names')
    use_service: bool = kwargs.get('use_service', False)
    rules = JavaScriptRules.generate()

    module = rules.module
    t = rules.t
    q = rules.q
    sc = rules.semi
    
    return Template(
        filename = f"{names.kebab}.controller.spec.ts",
        contents=[
            module.import_stmt(source='bun:test', imports=['describe', 'beforeEach', 'test']),
            module.import_stmt(source='@nestjs/testing', imports=['Test', 'TestingModule']),
            module.import_stmt(source=f"./{names.kebab}.controller", imports=[f"{names.pascal}Controller"]),
            module.import_stmt(source=f"./{names.kebab}.service", imports=[f"{names.pascal}Service"]) if use_service else None,
            '',
            f"describe({q}{names.pascal}Controller{q}, (){rules.blk_s}=>{rules.blk_s}{{",
            f"{t}let {names.camel}Controller: {names.pascal}Controller{sc}",
            '',
            f"{t}beforeEach(async (){rules.blk_s}=>{rules.blk_s}{{",
            f"{t*2}const {names.camel}: TestingModule = await Test.createTestingModule({{",
            f"{t*3}controllers: [{names.pascal}Controller]{',' if use_service else rules.es5_c}",
            f"{t*3}providers: [{names.pascal}Service]{rules.es5_c}" if use_service else None,
            f"{t*2}}}).compile(){sc}",
            '',
            f"{t*2}{names.camel}Controller = {names.camel}.get<{names.pascal}Controller>({names.pascal}Controller){sc}",
            t + '})' + sc,
            '',
            f"{t}test({q}Should be defined{q}, (){rules.blk_s}=>{rules.blk_s}{{",
            f"{t*2}expect({names.pascal}Controller).toBeDefined(){sc}",
            t + '})' + sc,
            '})' + sc
        ]
    )