from devtools.config.rule_set import JavaScriptRules
from devtools.core.decorators import requires
from devtools.core.lib import CaseMap
from devtools.core.template import Template

@requires('names')
def ts_layer(**kwargs) -> Template:
    names: CaseMap = kwargs.get('names')
    rules = JavaScriptRules.generate()
    return Template(
        filename = 'index.ts',
        contents = [
            f"/* Auto-generated index.ts file for layer {names.camel} */"
        ]
    )