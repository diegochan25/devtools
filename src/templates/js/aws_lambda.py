from src.config.cli_config import CLIConfig
from src.config.rule_set import JavaScriptRules
from src.core.template import Template

def js_lambda() -> Template:
    rules = JavaScriptRules.generate()
    return Template(
        filename = 'index.js',
        contents = [
            f"/** @param {{import({rules.q}aws-lambda{rules.q}).APIGatewayProxyEventV2}} {rules.event} */",
            f"const handler = async {rules.arr_fn_pl}{rules.event}{rules.arr_fn_pr} =>{rules.blk_s}{{",
            rules.t + '/* TODO implement */',
            rules.t + 'return {',
            rules.t * 2 + 'statusCode: 200,',
            f"{rules.t * 2}body: JSON.stringify({rules.q}Hello from Lambda!{rules.q}){rules.es5_c}",
            f"{rules.t}}}{rules.semi}",
            f"}}{rules.semi}",
            '',
            rules.module.export_stmt(default='handler')
        ]
    )