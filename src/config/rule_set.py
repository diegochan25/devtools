from abc import ABC, abstractmethod
from dataclasses import dataclass
from os import linesep
from src.config.cli_config import CLIConfig
from src.core.lang.js import JavaScriptModuleSystem, JavaScriptPackageManager, JavaScriptRuntime, get_module_system, get_pm, get_runtime
from src.core.lib import Serializable
from typing import Self


class LanguageRules(ABC, Serializable):
    @staticmethod
    @abstractmethod
    def generate() -> Self:
        pass

@dataclass
class JavaScriptRules(LanguageRules):
    semi: str
    q: str
    br_s: str
    blck_s: str
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

    @staticmethod
    def generate() -> JavaScriptRules:
        js = CLIConfig.read().javascript
        return JavaScriptRules(
            semi = ';' if js.semicolon == 'use' else '',
            q = '"' if js.quotes == 'double' else "'",
            br_s = ' ' if js.bracket_spacing == 'space' else '',
            blck_s = ' ' if js.block_spacing == 'space' else linesep if js.block_spacing == 'newline' else '',
            t = '\t' if js.indent == 'tab' else ' ' * js.tab_width,
            es5_c= ',' if not js.trailing_comma == 'none' else '',
            es8_c = ',' if js.trailing_comma == 'all' else '',
            arr_fn_pl='(' if js.arrow_fn_parentheses == 'use' else '',
            arr_fn_pr = ')' if js.arrow_fn_parentheses == 'use' else '',
            event = js.event_var_name,
            eol = '\r' if js.eol == 'cr' else '\n' if js.eol == 'lf' else '\r\n' if js.eol == 'crlf' else linesep,
            runtime = get_runtime(js.runtime),
            module = get_module_system(js.module),
            package_manager = get_pm(js.package_manager)
        )

@dataclass
class PythonRules(LanguageRules):
    q: str
    f_q: str
    t: str
    docstring: PythonDocstring

    @staticmethod
    def generate() -> PythonRules:
        py = CLIConfig.read().python
        return PythonRules(
            q = '"' if py.quotes == 'double' else "'",
            f_q = '"' if py.f_str_quotes == 'double' else "'", 
            t = '\t' if py.indent == 'tab' else ' ' * py.tab_width,
            docstring = ReSTDocstring if py.docstring == 'rest' else GoogleDocstring if py.docstring == 'google' else NumPyDocstring
        )

@dataclass
class RuleSet(LanguageRules):
    js: JavaScriptRules
    py: PythonRules

    @staticmethod
    def generate() -> RuleSet:
        return RuleSet(
            js = JavaScriptRules.generate(),
            py = PythonRules.generate() 
        )
