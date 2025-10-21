from copy import deepcopy
from dataclasses import asdict, dataclass
from os import linesep
from src.config.cli_config import CLIConfig
from src.core.js import ES6, NPM, PNPM, Bun, CommonJS, Deno, JSPackageManager, JSRuntime, ModuleSystem, NodeJS, Yarn

@dataclass
class JavaScriptRuleMap:
    q: str
    semi: str
    t: str
    arr_paren_l: str
    arr_paren_r: str
    event: str
    comma: str
    eol: str
    module_system: ModuleSystem
    br_s: str
    block_s: str
    cls_f_case: str
    runtime: JSRuntime
    pm: JSPackageManager

    @staticmethod
    def create() -> "JavaScriptRuleMap":
        config = CLIConfig.current()

        if isinstance(config, CLIConfig):
            js_config = config.javascript
            js_rules = {}
            js_rules['q'] = "'" if js_config.quotes == 'single' else '"'
            js_rules['semi'] = ';' if js_config.semicolon == 'use' else ''
            js_rules['t'] = '\t' if js_config.indent == 'tab' else ' ' * js_config.tab_width
            js_rules['arr_paren_l'] = '(' if js_config.arrow_function_parentheses == 'use' else ''
            js_rules['arr_paren_r'] = ')' if js_config.arrow_function_parentheses == 'use' else ''
            js_rules['event'] = js_config.event_var_name
            js_rules['comma'] = ',' if js_config.trailing_comma == 'use' else ''
            eol = js_config.eol
            if eol == 'cr':
                js_rules['eol'] = '\r'
            elif eol == 'lf':
                js_rules['eol'] = '\n'
            elif eol == 'crlf':
                js_rules['eol'] = '\r\n'
            else:
                js_rules['eol'] = linesep
            js_rules['module_system'] = ES6 if js_config.module_system == 'es6' else CommonJS
            js_rules['br_s'] = ' ' if js_config.bracket_spacing == 'space' else ''
            js_rules['block_s'] = ' ' if js_config.block_spacing == 'space' else js_rules['eol'] if js_config.block_spacing == 'newline' else ''
            js_rules['cls_f_case'] = js_config.class_file_case
            js_rules['runtime'] = NodeJS if js_config.runtime == 'node' else Deno if js_config.runtime == 'deno' else Bun
            js_rules['pm'] = NPM if js_config.package_manager == 'npm' else Yarn if js_config.package_manager == 'yarn' else PNPM if js_config.package_manager == 'pnpm' else Bun

            return JavaScriptRuleMap(**js_rules)
        
@dataclass
class RuleMap:
    js: JavaScriptRuleMap

    @staticmethod
    def create():
        return RuleMap(
            js=JavaScriptRuleMap.create()
        )
    
    def dict(self):
        return deepcopy(asdict(self))