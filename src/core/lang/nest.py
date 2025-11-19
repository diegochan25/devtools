from os import getcwd, path, scandir
import re
from src.config.rule_set import JavaScriptRules
from src.core.io import die
from src.core.lang.js import ES6, CommonJS
from src.core.lib import case_map 
from typing import Optional

class NestJSModule:
    __name: str
    __stmts: Optional[list[str]]
    __imports: Optional[list[str]]
    __controllers: Optional[list[str]]
    __providers: Optional[list[str]]
    __exports: Optional[list[str]]
    
    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, value: str) -> None:
        self.__name = value

    @property
    def stmts(self) -> Optional[list[str]]:
        return self.__stmts

    @property
    def classname(self) -> Optional[list[str]]:
        return f"{case_map(self.__name).pascal}Module"

    @property
    def imports(self) -> Optional[list[str]]:
        return self.__imports
    
    @property
    def controllers(self) -> Optional[list[str]]:
        return self.__controllers
    
    @property
    def providers(self) -> Optional[list[str]]:
        return self.__providers
    
    @property
    def exports(self) -> Optional[list[str]]:
        return self.__exports

    def __init__(
        self, 
        name: str, 
        stmts: Optional[list[str]] = None,
        imports: Optional[list[str]] = None,
        controllers: Optional[list[str]] = None,
        providers: Optional[list[str]] = None,
        exports: Optional[list[str]] = None
    ):
        self.__name = name
        self.__stmts = stmts
        self.__imports = imports
        self.__controllers = controllers
        self.__providers = providers
        self.__exports = exports

    def __str__(self) -> str:
        rules = JavaScriptRules.generate()
        tab = rules.t
        toarray = lambda ls: '[' + ', '.join(ls) + rules.es5_c + ']'

        arrays = [
            f"{tab}imports: {toarray(self.__imports)}" if self.__imports is not None else None,
            f"{tab}controllers: {toarray(self.__controllers)}" if self.__controllers is not None else None,
            f"{tab}providers: {toarray(self.__providers)}" if self.__providers is not None else None,
            f"{tab}exports: {toarray(self.__exports)}" if self.__exports is not None else None
        ]

        return rules.eol.join([
            *[stmt for stmt in list(dict.fromkeys(self.__stmts)) if stmt is not None],
            '',
            '@Module({',
            f",{rules.eol}".join([arr for arr in arrays if arr is not None]) + rules.es5_c,
            '})',
            rules.module.inline_export(f"class {self.classname}{rules.blk_s}{{ }}")
        ])

    @classmethod
    def build(cls, text: str):
        arrays = {
            'stmts': [
                JavaScriptRules.generate().module.import_stmt(source='@nestjs/common', imports=['Module'])
            ]
        }
        name = None
        for ln in text.splitlines():
            if CommonJS.is_import(ln) or ES6.is_import(ln):
                arrays.get('stmts').append(ln)
            elif (match := re.search(r"(\w+)\s*:\s+\[([^\]]*)\]", ln)):
                if not (attr := match.group(1).strip()):
                    continue
                if (raw := match.group(2).strip()):
                    if attr not in arrays:
                        arrays[attr] = []
                        arrays.get(attr).extend([c.strip() for c in raw.split(',') if c.strip()])
                else:
                    arrays[attr] = []
            elif 'class' in (words := ln.split()):
                name = [w for w in words if w.endswith('Module')][0].removesuffix('Module')
                if '.' in name:
                    name = name.split('.')[1]
        if name is None:
            die('NestJS module declaration requires name.')
        
        instance = cls(
            name,
            stmts = arrays.get('stmts') or None,
            imports = arrays.get('imports'),
            controllers = arrays.get('controllers'),
            providers = arrays.get('providers'),
            exports = arrays.get('exports')
        )

        print(instance)

        return instance
    
    @staticmethod
    def exists(at: str = getcwd()) -> str | False:
        for item in scandir(path.abspath(at)):
            if item.is_file() and item.name.endswith('.module.ts'):
                return item.path
        return False
