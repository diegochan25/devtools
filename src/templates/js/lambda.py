from src.config.rule_set import JavaScriptRules
from src.core.decorators import requires
from src.core.template import Template

def js_lambda(**kwargs) -> Template:
    js = JavaScriptRules.generate()
    return Template(
        filename='index.js',
        contents= [
            f"export const handler = async {js.arr_fn_pl}{js.event}{js.es8_c}{js.arr_fn_pr} =>{js.blck_s}{{",
            f"{js.t}const response = {{",
            f"{js.t * 2}statusCode: 200,",
            f"{js.t * 2}body: JSON.stringify({js.q}Hello from Lambda!{js.q}){js.es5_c}",
            f"{js.t}}}{js.semi}",
            f"{js.t}return response{js.semi}",
            f"}}{js.semi}"
        ]
    )
