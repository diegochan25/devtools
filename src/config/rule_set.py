from abc import abstractmethod
from dataclasses import dataclass
from os import linesep
from typing import Self
from src.config.cli_config import CLIConfig
from src.core.lang.js import ES6, NPM, PNPM, Bun, CommonJS, Deno, JavaScriptModuleSystem, JavaScriptPackageManager, JavaScriptRuntime, NodeJS, Yarn
from src.core.lang.py import GoogleDocstring, NumPyDocstring, PythonDocstring, ReSTDocstring
from src.core.lib import Serializable

class LanguageRules(Serializable):
    @classmethod
    @abstractmethod
    def generate(cls) -> Self:
        pass

@dataclass
class JavaScriptRules(LanguageRules):
    semi: str
    q: str
    br_s: str
    blk_s: str
    t: str
    es5_c: str
    es8_c: str
    arr_fn_pl: str
    arr_fn_pr: str
    event: str
    eol: str
    runtime: JavaScriptRuntime
    module: JavaScriptModuleSystem
    package_manager: JavaScriptPackageManager

    @classmethod
    def generate(cls):
        cfg = CLIConfig.read().javascript
        eol = '\r' if cfg.eol == 'cr' else '\n' if cfg.eol == 'lf' else '\r\n' if cfg.eol == 'crlf' else linesep
        return JavaScriptRules(
            semi = ';' if cfg.semicolon == 'use' else 'avoid',
            q = '"' if cfg.quotes == 'double' else "'",
            br_s = ' ' if cfg.bracket_spacing == 'space' else '',
            blk_s = ' ' if cfg.block_spacing == 'space' else eol if cfg.block_spacing == 'newline' else '',
            t = '\t' if cfg.indent == 'tab' else ' ' * cfg.tab_width,
            es5_c = ',' if not cfg.trailing_comma == 'none' else '',
            es8_c = ',' if cfg.trailing_comma == 'all' else '',
            arr_fn_pl = '(' if cfg.arrow_fn_parentheses == 'use' else '',
            arr_fn_pr = ')' if cfg.arrow_fn_parentheses == 'use' else '',
            event = cfg.event_var_name,
            eol = eol,
            runtime = NodeJS if cfg.runtime == 'node' else Deno if cfg.runtime == 'deno' else Bun,
            module = CommonJS if cfg.module == 'commonjs' else ES6,
            package_manager = NPM if cfg.module == 'npm' else Yarn if cfg.module == 'yarn' else PNPM if cfg.module == 'pnpm' else Bun
        )
    
class PythonRules(LanguageRules):
    q: str
    f_q: str
    t: str
    eol: str
    docstring: PythonDocstring

    @classmethod
    def generate(cls):
        cfg = CLIConfig.read().python
        eol = '\r' if cfg.eol == 'cr' else '\n' if cfg.eol == 'lf' else '\r\n' if cfg.eol == 'crlf' else linesep
        return PythonRules(
            q = '"' if cfg.quotes == 'double' else "'",
            f_q = '"' if cfg.f_str_quotes == 'double' else "'",
            t = '\t' if cfg.indent == 'tab' else ' ' * cfg.tab_width,
            eol = eol,
            docstring = ReSTDocstring if cfg.docstring == 'rest' else GoogleDocstring if cfg.docstring == 'google' else NumPyDocstring 
        )

@dataclass
class RuleSet(LanguageRules):
    js: JavaScriptRules
    py: PythonRules

    @classmethod
    def generate(cls):
        return RuleSet(
            js = JavaScriptRules.generate(),
            py = PythonRules.generate()
        )
    
print(
    JavaScriptRules.generate().module.import_stmt(
        source='fs',
        imports=['readFileSync', {'writeFileSync': 'write'}],
        default='fs'
    )
)
