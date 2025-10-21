from src.config.rule_map import RuleMap
from src.core.decorators import requires
from src.core.js import PackageJson
from src.core.namecase import case_map
from src.core.template import Template


@requires('name')
def nest_controller(**kwargs) -> Template:
    names = case_map(kwargs.get('name'))
    use_service = kwargs.get('use_service', False)
    use_route_name = kwargs.get('use_route_name', True)
    js = RuleMap.create().js

    contents = [js.module_system.generate_import_statement(imports=['Controller'], source='@nestjs/common')]

    if use_service:
        contents.append(js.module_system.generate_import_statement(imports=[f"{names.pascal}Service"], source=f"{names.kebab}.service"))

    contents.extend([
        '',
        f"@Controller({f"{js.q}{names.kebab}{js.q}" if use_route_name else ''})",
        f"export class {names.pascal}Controller{js.block_s}{{",
        f"{js.t}constructor({f"private readonly {names.camel}Service: {names.pascal}Service" if use_service else ''}){js.block_s}{{{js.block_s}}}",
        '}'
    ])

    return Template(f"{names.kebab}.controller.ts", contents)

@requires('name')
def package_json(**kwargs) -> Template:
    kebab_name = case_map(kwargs.get('name')).kebab

    return Template('package.json', PackageJson(
        name=kebab_name,
        version='0.1.0',
        description='NestJS application scaffolded with devtools',
        main='src/main.ts',
        private=True,
        keywords=['TypeScript', 'ES6', 'NestJS', 'Server', 'API', 'Application'],
        type='module',
        scripts= {
            'start': 'bun run src/main.ts',
            'dev': 'bun run src/main.ts --watch'
        }
    ).dict())

def main_ts() -> Template:
    js = RuleMap.create().jsjs = RuleMap.create().js
    return Template('main.ts', [
        'import { NestFactory } from "@nestjs/core";',
        'import { NestExpressApplication } from "@nestjs/platform-express";',
        'import { AppModule } from "./app.module";',
        '',
        '(async () => {',
        js.t + 'const app = await NestaFactory.create<NestExpressApplication>(AppModule);',
        js.t + 'app.setGlobalPrefix("api");',
        js.t,
        js.t + 'await app.listen(3000);',
        '})()'
    ])

def app_module() -> Template: 
    js = RuleMap.create().js
    return Template('app.module.ts', [
        'import { Module } from "@nestjs/core";',
        '',
        '@Module({',
        js.t + 'imports: [],',
        js.t + 'controllers: [],',
        js.t + 'providers: [],',
        js.t + 'exports: []',
        '})',
        'export class AppModule { }'
    ])