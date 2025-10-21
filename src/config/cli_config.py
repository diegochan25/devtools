import json
from copy import deepcopy
from dataclasses import asdict, dataclass
from json import JSONDecodeError
from os import path
from typing import Any, Literal

from src.core.io import die

@dataclass
class JavaScriptConfig:
    quotes: Literal['single', 'double']
    semicolon: Literal['use', 'avoid']
    indent: Literal['space', 'tab']
    tab_width: int
    arrow_function_parentheses: Literal['use', 'avoid']
    event_var_name: str
    trailing_comma: Literal['use', 'avoid']
    eol: Literal['cr', 'lf', 'crlf', 'os']
    module_system: Literal['es6', 'commonjs']
    bracket_spacing: Literal['space', 'tight']
    block_spacing: Literal['space', 'tight', 'newline']
    class_file_case: Literal['pascal', 'kebab', 'snake']
    runtime: Literal['node', 'deno', 'bun']
    package_manager: Literal['npm', 'yarn', 'pnpm', 'bun']

    @staticmethod
    def default() -> "JavaScriptConfig":
        return JavaScriptConfig(
            quotes='double',
            semicolon='use',
            indent='space',
            tab_width=4,
            arrow_function_parentheses='use',
            event_var_name='event',
            trailing_comma='avoid',
            eol='crlf',
            module_system='es6',
            bracket_spacing='space',
            block_spacing='space',
            class_file_case='pascal',
            runtime='bun',
            package_manager='bun',
        )

@dataclass
class CLIConfig: 
    javascript: JavaScriptConfig
    
    @staticmethod
    def current() -> "CLIConfig":
        with open(path.join(path.dirname(__file__), 'config.json'), 'w+', encoding='utf-8') as file:
            if file.read(1):
                try:
                    config = json.load(file)
                except JSONDecodeError:
                    config = CLIConfig.default().dict()
                    json.dump(config, file, indent=4)
            else: 
                config = CLIConfig.default().dict()
                json.dump(config, file, indent=4)

        return CLIConfig(
            javascript=JavaScriptConfig(**config['javascript'])
        )

    @staticmethod
    def default() -> "CLIConfig":
        return CLIConfig(
            javascript = JavaScriptConfig.default()
        )
    
    def dict(self) -> dict[str, Any]:
        return deepcopy(asdict(self))
    
    def write(self):
        try:
            with open(path.join(path.dirname(__file__), 'config.json'), 'w', encoding='utf-8') as file:
                json.dump(self.dict(), file, indent=4)
        except: 
            die('Malformed object sturcture.')
