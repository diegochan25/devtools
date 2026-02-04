from abc import abstractmethod
from dataclasses import dataclass
from os import linesep
from typing import Self
from devtools.config.cli_config import CLIConfig
from devtools.core.lang.js import ES6, NPM, PNPM, Bun, CommonJS, Deno, JSModuleSystem, JSPackageManager, JSRuntime, NodeJS, Yarn
from devtools.core.lang.py import GoogleDocstring, NumPyDocstring, PythonDocstring, ReSTDocstring
from devtools.core.lib import Serializable

class LanguageRules(Serializable):
    @classmethod
    @abstractmethod
    def generate(cls) -> Self:
        pass

@dataclass
class CppRules(LanguageRules):
    t: str
    
    @classmethod
    def generate(cls):
        cfg = CLIConfig.read().cpp
        return CppRules(
            t = '\t' if cfg.indent == 'tab' else ' ' * cfg.tab_width
        )

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
    runtime: JSRuntime
    module: JSModuleSystem
    package_manager: JSPackageManager

    @classmethod
    def generate(cls) -> 'JavaScriptRules':
        cfg = CLIConfig.read().javascript
        return JavaScriptRules(
            semi = ';' if cfg.semicolon == 'use' else 'avoid',
            q = '"' if cfg.quotes == 'double' else "'",
            br_s = ' ' if cfg.bracket_spacing == 'space' else '',
            blk_s = ' ' if cfg.block_spacing == 'space' else linesep if cfg.block_spacing == 'newline' else '',
            t = '\t' if cfg.indent == 'tab' else ' ' * cfg.tab_width,
            es5_c = ',' if not cfg.trailing_comma == 'none' else '',
            es8_c = ',' if cfg.trailing_comma == 'all' else '',
            arr_fn_pl = '(' if cfg.arrow_fn_parentheses == 'use' else '',
            arr_fn_pr = ')' if cfg.arrow_fn_parentheses == 'use' else '',
            event = cfg.event_var_name,
            eol = linesep,
            runtime = NodeJS if cfg.runtime == 'node' else Deno if cfg.runtime == 'deno' else Bun,
            module = CommonJS if cfg.module == 'commonjs' else ES6,
            package_manager = NPM if cfg.package_manager == 'npm' else Yarn if cfg.package_manager == 'yarn' else PNPM if cfg.package_manager == 'pnpm' else Bun
        )

@dataclass
class PythonRules(LanguageRules):
    q: str
    f_q: str
    t: str
    eol: str
    docstring: PythonDocstring

    @classmethod
    def generate(cls) -> 'PythonRules':
        cfg = CLIConfig.read().python
        return PythonRules(
            q = '"' if cfg.quotes == 'double' else "'",
            f_q = '"' if cfg.f_str_quotes == 'double' else "'",
            t = '\t' if cfg.indent == 'tab' else ' ' * cfg.tab_width,
            eol = linesep,
            docstring = ReSTDocstring if cfg.docstring == 'rest' else GoogleDocstring if cfg.docstring == 'google' else NumPyDocstring 
        )