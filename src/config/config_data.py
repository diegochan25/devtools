from abc import abstractmethod
from copy import deepcopy
from core.lib import tostring
from dataclasses import dataclass, asdict, is_dataclass
from typing import Literal


class LanguageConfig:
    def tostring(self) -> str:
        return tostring(self.todict)

    def todict(self) -> dict:
        def convert(value):
            if isinstance(value, LanguageConfig):
                return value.todict()
            elif is_dataclass(value):
                return {k: convert(v) for k, v in asdict(value).items()}
            elif isinstance(value, dict):
                return {k: convert(v) for k, v in value.items()}
            elif isinstance(value, (list, tuple)):
                return [convert(v) for v in value]
            else:
                return deepcopy(value)
        return {k: convert(v) for k, v in self.__dict__.items()}
    
    @classmethod
    def fromdict(cls, dictionary: dict) -> 'LanguageConfig':
        for attr in list(cls.__annotations__.keys()):
            if attr not in dictionary:
                raise ValueError(f"Missing required attribute '{attr}' in dictionary.")
        for attr in list(dictionary.keys()):
            if attr not in cls.__annotations__:
                raise ValueError(f"Unexpected key '{attr}' in dictionary.")
        return cls(**dictionary)

    
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
    eol: Literal['cr', 'lf', 'crlf', 'os']
    runtime: Literal['node', 'bun', 'deno']
    package_manager: Literal['npm', 'yarn', 'pnpm', 'bun']

    @staticmethod
    def default() -> 'JavaScriptConfig':
        return JavaScriptConfig(
            semicolon='use',
            quotes='double',
            bracket_spacing='space',
            block_spacing='tight',
            indent='space',
            tab_width=4,
            trailing_comma='none',
            arrow_fn_parentheses='use',
            event_var_name='event',
            eol='crlf',
            runtime='bun',
            package_manager='bun'
        )


@dataclass
class PythonConfig(LanguageConfig):
    str_quotes: Literal['double', 'single']
    f_str_quotes: Literal['double', 'single']
    indent: Literal['tab', 'space']
    tab_width: int
    docstring: Literal['rest', 'google', 'numpy']

    @staticmethod
    def default() -> 'PythonConfig':
        return PythonConfig(
            str_quotes='single',
            f_str_quotes='double',
            indent='space',
            tab_width=4,
            docstring_quotes='google',
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