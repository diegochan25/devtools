from abc import abstractmethod
from src.core.lib import Serializable
from dataclasses import dataclass
from typing import Literal

class LanguageConfig(Serializable):    
    @staticmethod
    @abstractmethod
    def default() -> 'LanguageConfig':
        pass

@dataclass
class JavaScriptConfig(LanguageConfig):
    semicolon: Literal['use', 'avoid']
    quotes: Literal['double', 'single']
    bracket_spacing: Literal['space', 'tight']
    block_spacing: Literal['space', 'tight', 'newline']
    indent: Literal['tab', 'space']
    tab_width: int
    trailing_comma: Literal['all', 'es5', 'none']
    arrow_fn_parentheses: Literal['use', 'avoid']
    event_var_name: str
    eol: Literal['lf', 'crlf', 'os']
    runtime: Literal['node', 'bun', 'deno']
    module: Literal['commonjs', 'es6']
    package_manager: Literal['npm', 'yarn', 'pnpm', 'bun']

    @staticmethod
    def default() -> 'JavaScriptConfig':
        return JavaScriptConfig(
            semicolon='use',
            quotes='double',
            bracket_spacing='space',
            block_spacing='space',
            indent='space',
            tab_width=4,
            trailing_comma='none',
            arrow_fn_parentheses='use',
            event_var_name='event',
            eol='lf',
            runtime='bun',
            module='es6',
            package_manager='bun'
        )


@dataclass
class PythonConfig(LanguageConfig):
    quotes: Literal['double', 'single']
    f_str_quotes: Literal['double', 'single']
    indent: Literal['tab', 'space']
    tab_width: int
    eol: Literal['lf', 'crlf', 'os']
    docstring: Literal['rest', 'google', 'numpy']

    @staticmethod
    def default() -> 'PythonConfig':
        return PythonConfig(
            quotes='single',
            f_str_quotes='double',
            indent='space',
            tab_width=4,
            eol='lf',
            docstring='google',
        )

@dataclass 
class ConfigData(LanguageConfig):
    javascript: JavaScriptConfig 
    python: PythonConfig 
    
    @staticmethod
    def default() -> 'ConfigData':
        return ConfigData(
            javascript = JavaScriptConfig.default(), 
            python = PythonConfig.default() 
        )
    