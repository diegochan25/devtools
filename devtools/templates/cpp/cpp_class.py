from devtools.config.rule_set import CppRules
from devtools.core.decorators import requires
from devtools.core.lib import CaseMap
from devtools.core.template import Template

@requires('names')
def cpp_class_h(**kwargs) -> Template:
    rules = CppRules.generate()
    names: CaseMap = kwargs.get('names')
    namespace = str(kwargs.get('namespace'))
    enum = bool(kwargs.get('enum'))
    
    t = rules.t
    ct = t if namespace is not None else ''

    return Template(
        filename=f"{names.pascal}.h",
        contents=[
            '#pragma once',
            '#include <string>',
            '',
            'using std::string;',
            '',
            f"namespace {namespace} {{" if namespace is not None else None,
            f"{ct}{'enum ' if enum else ''}class {names.pascal} {{",
            f"{t + ct}",
            f"{ct}}};",
            '}' if namespace is not None else None
        ]
    )

@requires('names')
def cpp_class_impl(**kwargs) -> Template:
    rules = CppRules.generate()
    names: CaseMap = kwargs.get('names')
    namespace = str(kwargs.get('namespace'))
    
    ct = rules.t if namespace is not None else ''

    return Template(
        filename=f"{names.pascal}.cpp",
        contents=[
            f"#include \"{names.pascal}.h\"",
            '',
            f"namespace {namespace} {{" if namespace is not None else None,
            ct,
            '}' if namespace is not None else None
        ]
    )