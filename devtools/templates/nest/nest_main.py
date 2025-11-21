from devtools.config.rule_set import JavaScriptRules
from devtools.core.template import Template

def nest_main() -> Template:
    rules = JavaScriptRules.generate()
    t = rules.t
    q = rules.q
    sc = rules.semi
    module = rules.module
    return Template(
        filename='main.ts',
        contents=[
            module.import_stmt(source='@nestjs/core', imports=['NestFactory']),
            module.import_stmt(source='@nestjs/common', imports=['ValidationPipe']),
            module.import_stmt(source='./app.module', imports=['AppModule']),
            '',
            f"(async (){rules.br_s}=>{rules.br_s}{{",
            t + 'const app = await NestFactory.create(AppModule)' + sc,
            t,
            t + 'app.enableCors()' + sc,
            f"{t}app.setGlobalPrefix({q}api{q}){sc}",
            t + 'app.useGlobalPipes(new ValidationPipe())' + sc,
            t,
            f"{t}const host = process.env.HOST ?? {q}127.0.0.1{q}{sc}",
            t + 'const port = parseInt(process.env.PORT) ?? 3000',
            t,
            f"{t}await app.listen(port, host, () => console.log({q}App is listening at http://%s:%d/{q}, host, port)){sc}",
            '})()' + sc
        ]
    )