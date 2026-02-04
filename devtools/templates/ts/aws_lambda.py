from devtools.config.rule_set import JavaScriptRules
from devtools.core.template import Template

def ts_lambda() -> Template:
    rules = JavaScriptRules.generate()
    return Template(
        filename = 'index.ts',
        contents = [
            rules.module.import_stmt('aws-lambda', ['APIGatewayProxyEventV2'], type_only=True),
            '',
            f"const handler = async {rules.arr_fn_pl}{rules.event}: APIGatewayProxyEventV2{rules.arr_fn_pr} =>{rules.blk_s}{{",
            rules.t + '/* TODO implement */',
            rules.t + 'return {',
            rules.t * 2 + 'statusCode: 200,',
            f"{rules.t * 2}body: JSON.stringify({rules.q}Hello from Lambda!{rules.q}){rules.es5_c}",
            f"{rules.t}}}{rules.semi}",
            f"}}{rules.semi}",
            '',
            rules.module.export_stmt(exports=['handler'])
        ]
    )