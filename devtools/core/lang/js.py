from abc import ABC, abstractmethod
from json import JSONDecodeError
import json
from os import getcwd, linesep, path
import re
from subprocess import CalledProcessError
import subprocess
from typing import Literal
from devtools.core.io import die, s
from devtools.core.lib import Executable

class JSRuntime(Executable):
    # inherited from Executable
    # name: str
    # _cmd : str
    pass

class JSPackageManager(Executable):
    # inherited from Executable
    # name: str
    # _cmd : str
    _install_cmd: str

    @classmethod
    @abstractmethod
    def restore(cls, at: str=getcwd(), omit: list[Literal['dev', 'optional', 'peer']] | None = None) -> bool:
        if not path.isdir(at) or not path.isfile((pkg_json_path := path.join(at, 'package.json'))):
            die(f"No package.json could be found at {at}")
        
        with open(pkg_json_path, 'r', encoding='utf-8') as file:
            try:
                json.load(file)
            except JSONDecodeError:
                die(f"Malformed package.json at {at}")
        try:
            subprocess.run(
                f"{cls._cmd} install",
                cwd=at,
                shell=True,
                check=True,
                capture_output=True
            )
            return True
        except CalledProcessError:
            return False

    @classmethod
    @abstractmethod
    def install(cls, *packages: str, at: str = getcwd(), dev: bool = False) -> bool:
        packages = [p for p in packages if p]
        
        if not path.isdir(at) or not path.isfile((pkg_json_path := path.join(at, 'package.json'))):
            die(f"No package.json could be found at {at}")
        
        with open(pkg_json_path, 'r', encoding='utf-8') as file:
            try:
                json.load(file)
            except JSONDecodeError:
                die(f"Malformed package.json at {at}")

        try:
            subprocess.run(
                f"{cls._cmd} {cls._install_cmd} {'-D' if dev else ''} {' '.join(packages)}",
                cwd=at,
                shell=True,
                check=True,
                # capture_output=True,
                text=True
            )
            return True
        except CalledProcessError:
            return False

    @classmethod
    def run(cls, script: str, at: str = getcwd()) -> str:
        abspath = path.abspath(at)
        package_json_path = path.join(abspath, 'package.json')
        
        if not path.isfile(package_json_path) or not path.getsize(package_json_path):
            die(f"package.json could not be found at {abspath}")

        with open(package_json_path, 'r', encoding='utf-8') as file:
            try:
                package_json = json.load(file)
                if (scripts := package_json.get('scripts', None)) is None or not isinstance(scripts, dict) or scripts.get(script, None) is None:
                    die(f"Unable to find script '{script}' in package.json at {abspath}")
                try:
                    command = f"{cls._cmd} run {script}" 
                    result = subprocess.run(
                        command,
                        shell=True,
                        check=True,
                        capture_output=True,
                        text=True
                    )

                    return result.stdout
                
                except CalledProcessError as e:
                    die(s(f"Execution of script '{script}' failed.", fg='red'), s(e.stderr, fg='gray'), sep=linesep)
            except JSONDecodeError:
                die(f"Malformed package.json at {abspath}")

class JSModuleSystem(ABC):
    name: str

    @classmethod
    @abstractmethod
    def import_stmt(
        cls,
        source: str,
        imports: list[str | dict[str, str]] | None,
        default: str | None
    ) -> str:
        pass

    @classmethod
    @abstractmethod
    def is_import(
        cls,
        ln: str
    ) -> bool:
        pass

    @classmethod
    @abstractmethod
    def export_stmt(cls, exports: list[str | dict[str, str]] | None, default: str | None) -> str:
        pass

    @classmethod
    @abstractmethod
    def inline_export(cls, token: str, default: bool) -> str | None:
        pass

class CommonJS(JSModuleSystem):
    name = 'commonjs'

    @classmethod
    def import_stmt(
        cls,
        source: str,
        imports: list[str | dict[str, str]] | None = None,
        default: str | None = None
    ) -> str:
        if imports is None and default is None:
            return ''
        
        from devtools.config.rule_set import JavaScriptRules
        rules = JavaScriptRules.generate()
        lines = []

        if imports and len(imports):
            spread_imports = []
            for imp in imports:
                if isinstance(imp, dict) and len(imp) == 1:
                    name, alias = next(iter(imp.items()))
                    spread_imports.append(f"{name}: {alias}")
                elif isinstance(imp, str) and imp:
                    spread_imports.append(imp)
            stmt = rules.br_s.join(['{', ', '.join(spread_imports), '}'])
            lines.append(' '.join(['const', stmt, '=', f"require({rules.q}{source}{rules.q}){rules.semi}"]))
        if default:
           lines.append(f"const {default} = require({rules.q}{source}{rules.q}){rules.semi}")

        return linesep.join(lines)
    
    @classmethod
    def is_import(cls, ln: str) -> bool:
        words = [str(w).strip() for w in ln.split(' ') if w]
        return any([True for w in words if w.startswith('require')])

    @classmethod
    def export_stmt(cls, exports: list[str] | None = None, default: str | None = None) -> str:
        if not (bool(exports) ^ bool(default)):
            return ''
        
        from devtools.config.rule_set import JavaScriptRules
        rules = JavaScriptRules.generate()

        stmt = ['module.exports', '=']

        if default:
            stmt.append(default + rules.semi)
        
        elif exports and len(exports):
            module_exports = ['{']
            for i, export in enumerate(exports):
                if isinstance(export, dict) and len(export) == 1:
                    name, alias = next(iter(export.items()))
                    module_exports.append(f"{alias}: {name}{',' if i < len(exports) - 1 else rules.es5_c}")
                elif isinstance(export, str):
                    module_exports.append(f"{rules.t}{export}{',' if i < len(exports) - 1 else rules.es5_c}")
            module_exports.append('}' + rules.semi)
            stmt.append(linesep.join(module_exports))

        return ' '.join(stmt)
    
    @classmethod
    def inline_export(cls, token: str, default: bool = False):
        isvar = lambda ln: bool(ln.split()[0] in ('var', 'let', 'const'))
        isclass = lambda ln: bool('class' in ln)
        isfunc = lambda ln: (
            re.search(r"\bfunction\s*\*?\b", ln)
            or re.search(r"\([^)]*\)\s*=>", ln)
            or re.search(r"[A-Za-z_$][A-Za-z0-9_$]*\s*=>", ln)
        )
        matchindex = lambda pattern, array: [i for i, s in enumerate(array) if re.compile(pattern).search(s)][0]

        words = token.split()
        # remove typescript type
        if isvar(token):
            if words[1].endswith(':'):
                words = [words[0], words[1].removesuffix(':'), *words[words.index('='):]]
            elif words[2] == ':':
                words = [words[:1], *words[words.index('='):]]

        token = ' '.join(words)
        name = None
        export = ''

        if isvar(token):
            name = words[1]
            export = ' '.join(token.split('=')[1])
        elif isfunc(token):
            index = matchindex(r"^function\s*\*?$", words) + 1
            fnname = words[index]
            name = fnname[:fnname.index('(')] if '(' in fnname else fnname
        elif isclass(token):
            name = words.pop(words.index('class') + 1)
            export = ' '.join(words)

        if default:
            return f"module.exports = {export}"
        elif name is not None:
            return f"exports.{name} = {export}"
        return None

class ES6(JSModuleSystem):
    name = 'es6'

    @classmethod
    def import_stmt(
        cls,
        source: str,
        imports: list[str | dict[str, str]] | None = None,
        default: str | None = None
    ) -> str:
        if imports is None and default is None:
            return ''
        from devtools.config.rule_set import JavaScriptRules
        rules = JavaScriptRules.generate()
        stmt = ['import']
        
        modules = []
        if default: 
                modules.append(default)
    
        if imports and len(imports):
            named_imports = []
            for imp in imports:
                if isinstance(imp, dict) and len(imp) == 1:
                    name, alias = next(iter(imp.items()))
                    named_imports.append(f"{name} as {alias}")
                elif isinstance(imp, str) and imp:
                    named_imports.append(imp)
            modules.append(f"{{{rules.br_s}{', '.join(named_imports)}{rules.br_s}}}")
        
        stmt.append(', '.join(modules))
        stmt.append('from')
        stmt.append(f"{rules.q}{source}{rules.q}{rules.semi}")

        return ' '.join(stmt)
    
    @classmethod
    def is_import(cls, ln):
        words = ln.split()
        return 'import' in words
 
    @classmethod
    def export_stmt(cls, exports: list[str] | None = None, default: str | None = None) -> str:
        if exports is None and default is None:
            return ''
        
        from devtools.config.rule_set import JavaScriptRules
        rules = JavaScriptRules.generate()

        lines = []

        if exports is not None and len(exports):
            named_exports = []
            for i, export in enumerate(exports):
                if isinstance(export, dict) and len(export) == 1:
                    name, alias = next(iter(export.items()))
                    named_exports.append(f"{name} as {alias}{',' if i < len(exports) - 1 else rules.es5_c}")
                elif isinstance(export, str):
                    named_exports.append(f"{export}{',' if i < len(exports) - 1 else rules.es5_c}")
            lines.append(f"export {{{rules.br_s}{' '.join(named_exports)}{rules.br_s}}}{rules.semi}")

        if default is not None:
            lines.append(f"export default {default}{rules.semi}")

        return linesep.join(lines)
    
    @classmethod
    def inline_export(cls, token: str, default: bool = False):
        isvar = lambda ln: bool(ln.split()[0] in ('var', 'let', 'const'))
        if default:
            if isvar(token):
                return f"export default {token.split('=')[1]}"
            else:
                return f"export default {token}"
        else:
            return f"export {token}"

class NodeJS(JSRuntime):
    name = 'Node.js'
    _cmd = 'node'

class Deno(JSRuntime):
    name = 'Deno'
    _cmd = 'deno'

class Bun(JSRuntime, JSPackageManager):
    name = 'Bun'
    _cmd = 'bun'
    _install_cmd = 'add'

class NPM(JSPackageManager):
    name = 'npm'
    _cmd = 'npm'
    _install_cmd = 'install'

class Yarn(JSPackageManager):
    name = 'Yarn'
    _cmd = 'yarn'
    _install_cmd = 'add'

class PNPM(JSPackageManager):
    name = 'pnpm'
    _cmd = 'pnpm'
    _install_cmd = 'install'