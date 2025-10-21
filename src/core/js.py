import json
from abc import ABC, abstractmethod
from copy import deepcopy
from dataclasses import asdict, dataclass
from json import JSONDecodeError
from os import path, getcwd
from typing import Any, Literal
from src.core.namecase import case_map

@dataclass 
class PackageJson: 
    name: str | None
    version: str | None
    description: str | None = None
    type: Literal['commonjs', 'module'] | None = None
    keywords: list[str] | None = None
    homepage: str | None = None
    bugs: str | dict[Literal['url', 'email'], str] | None = None
    license: str | None = None
    author: str | dict[Literal['name', 'email', 'url'], str] | None = None
    contributors: list[str | dict[Literal['name', 'email', 'url'], str]] | None = None
    funding: str | dict[Literal['type', 'url'], str] | list[str | dict[Literal['type', 'url'], str]] | None = None
    files: list[str] | None = None
    main: str | None = None
    module: str | None = None
    browser: str | None = None
    bin: str | dict[str, str] | None = None
    man: str | list[str] | None = None
    directories: dict[Literal['doc', 'lib', 'bin', 'man']] | None = None
    repository: str | dict[Literal['type', 'url', 'directory'], str] | None = None
    scripts: dict[str, str] | None = None
    config: dict[str, str] | None = None
    dependencies: dict[str, str] | None = None
    dev_dependencies: dict[str, str] | None = None
    peer_dependencies: dict[str, str] | None = None
    peer_dependencies_meta: dict[str, str] | None = None
    bundled_dependencies: list[str] | None = None
    optional_dependencies: dict[str, str] | None = None
    engines: dict[str, str] | None = None
    os: list[str] | None = None
    cpu: list[str] | None = None
    private: bool | None = None
    publish_config: dict[str, str] | None = None
    workspaces: list[str] | dict[Literal['packages', 'nohoist'], list[str]] | None = None

    def dict(self):
        dictionary = deepcopy(asdict(self))
        for key in list(dictionary.keys()):
            camel = case_map(key).camel
            value = dictionary.pop(key) 
            if value is not None:
                dictionary[camel] = value
        return dictionary
    
class ModuleSystem(ABC):
    
    @classmethod
    @abstractmethod
    def generate_import_statement(
        cls,
        imports: list[str | dict[str, str]] | None, 
        default_import: str | None,
        source: str,
    ) -> str:
        if not source:
            return None
        if not imports and not default_import:
            return None
        

class ES6(ModuleSystem):
    @classmethod
    def generate_import_statement(cls, imports=[], default_import={}, source='') -> str:
        from src.config.rule_map import RuleMap
        js = RuleMap.create().js
        super().generate_import_statement(imports, default_import, source)
        
        stmt = ['import']
        if default_import and imports:
                stmt.append(f"{default_import},")
        elif default_import and not imports:
                stmt.extend([default_import, 'from', f"\"{source}\";"])
        
        if imports:
            named_imports = []
            for named_import in imports:
                if isinstance(named_import, str):
                    named_imports.append(named_import)
                elif isinstance(named_import, dict):
                    name, alias = next(iter(named_import.items()))
                    named_imports.append(f"{name} as {alias}")
            
            stmt.extend(['{' + js.br_s + ', '.join(named_imports) + js.br_s + '}', 'from', f"\"{source}\";"])
        
        return ' '.join(stmt)


class CommonJS(ModuleSystem):
    @classmethod
    def generate_import_statement(cls, imports=[], default_import={}, source='') -> str:
        super().generate_import_statement(imports, default_import, source)
        from src.config.rule_map import RuleMap
        js = RuleMap.create().js

        stmt = []
        if default_import:
            default_import_stmt = ['const']
            default_import_stmt.append(default_import)

            default_import_stmt.extend(['=', f"require(\"{source}\");"])
            stmt.append(' '.join(default_import_stmt))

        if imports:
            named_import_stmt = ['const']
            named_imports = []
            for named_import in imports:
                if isinstance(named_import, str):
                  named_imports.append(named_import)
                elif isinstance(named_import, dict):
                    name, alias = next(iter(named_import.items()))
                    named_imports.append(f"{name}: {alias}")
            named_import_stmt.extend(['{' + js.br_s + ', '.join(named_imports) + js.br_s + '}', '=', f"require(\"{source}\");"])
            stmt.append(' '.join(named_import_stmt))

        return '\n'.join(stmt)
    
class JSPackageManager(ABC):
    name: str
    cmd: str
    
class JSRuntime(ABC):
    name: str
    cmd: str


class NodeJS(JSRuntime):
    name = 'Node.js'
    cmd = 'node'

class Deno(JSRuntime):
    name = 'Deno'
    cmd = 'deno'

class Bun(JSRuntime, JSPackageManager):
    name = 'Bun'
    cmd = 'bun'

class NPM(JSPackageManager):
    name = 'Node Package Manager (npm)'
    cmd = 'npm'

class Yarn(JSPackageManager):
    name = 'Yarn'
    cmd = 'yarn'

class PNPM(JSPackageManager):
    name = 'Performant Node Package Manager (pnpm)'
    cmd = 'pnpm'


class JS:
    @staticmethod
    def find_package_json(dir: str = getcwd()) -> str | None:
        cwd = path.abspath(dir)
        while not path.abspath(cwd) == path.abspath(path.dirname(cwd)):
            package_json_path = path.join(cwd, 'package.json')
            if path.isfile(package_json_path):
                return package_json_path
            else:
                cwd = path.dirname(cwd)
        return None
    @staticmethod
    def load_package_json(package_json_path: str) -> PackageJson | None:
        if path.isfile(package_json_path):
            with open(package_json_path, 'r', encoding='utf-8') as file:
                try:
                    package_json_dict: dict[str, Any] = json.load(file)
                except JSONDecodeError:
                    return None
                
                for key in list(package_json_dict.keys()):
                    snake = case_map(key).snake
                    package_json_dict[snake] = package_json_dict.pop(key)

                return PackageJson(**package_json_dict)
        else:
            return None
        
    def dump_package_json(package_json_path: str, package_json_dict: dict[str, Any]):
        try:
            PackageJson(**package_json_dict)
        except TypeError:
            return None
        if path.isfile(package_json_path):
            with open(package_json_path, 'r+', encoding='utf-8') as file:
                json.dump(package_json_dict, file, indent=4)
                return True
        else:
            return None