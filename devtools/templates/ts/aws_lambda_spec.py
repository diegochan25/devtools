from devtools.config.rule_set import JavaScriptRules
from devtools.core.template import Template


def ts_lambda_spec(**kwargs) -> Template:
    name = kwargs.get("name", "")
    rules = JavaScriptRules.generate()
    return Template(
        filename="index.spec.ts",
        contents=[
            '/// <reference types="node" />',
            rules.module.import_stmt("node:test", ['describe', 'test', 'beforeEach', 'type TestContext']),
            f"describe({rules.q}{name} tests{rules.q}, () => {{",
            f"{rules.t}beforeEach((c) => {{",
            f"{rules.t*2}const ctx = c as TestContext;",
            rules.t * 2,
            f"{rules.t}}});",
            '',
            f"{rules.t}test({rules.q}All in order{rules.q}, async {rules.arr_fn_pl}t{rules.arr_fn_pr} => {{",
            rules.t * 2,
            f"{rules.t}}});",
            "});",
        ],
    )
