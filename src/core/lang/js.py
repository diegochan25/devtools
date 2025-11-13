from abc import ABC, abstractmethod
from json import JSONDecodeError
import json
from os import getcwd, linesep, path
from subprocess import CalledProcessError
import subprocess
from typing import Literal
from src.core.io import die, s
from src.core.lib import Executable

class JavaScriptRuntime(Executable):
    pass

class JavaScriptPackageManager(Executable):
    _install_cmd: str

    @classmethod
    @abstractmethod
    def restore(cls, omit: list[Literal['dev', 'optional', 'peer']] | None) -> bool:
        pass

    @classmethod
    @abstractmethod
    def install(cls, *packages: str, dev: bool = False) -> bool:
        try:
            subprocess.run(
                f"{cls._cmd} {cls._install_cmd} {'-D' if dev else ''} {' '.join(packages)}"
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

class JavaScriptModuleSystem(ABC):
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
    def export_stmt(cls, exports: list[str | dict[str, str]] | None, default: str | None) -> str:
        pass

class CommonJS(JavaScriptModuleSystem):
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
        
        from src.config.rule_set import JavaScriptRules
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

        return rules.eol.join(lines)

    @classmethod
    def export_stmt(cls, exports: list[str] | None = None, default: str | None = None) -> str:
        if not (bool(exports) ^ bool(default)):
            return ''
        
        from src.config.rule_set import JavaScriptRules
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
            stmt.append(rules.eol.join(module_exports))

        return ' '.join(stmt)


class ES6(JavaScriptModuleSystem):
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
        from src.config.rule_set import JavaScriptRules
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
    def export_stmt(cls, exports: list[str] | None = None, default: str | None = None) -> str:
        if exports is None and default is None:
            return ''
        
        from src.config.rule_set import JavaScriptRules
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

        return rules.eol.join(lines)


class NodeJS(JavaScriptRuntime):
    _name = 'Node.js'
    _cmd = 'node'

class Deno(JavaScriptRuntime):
    _name = 'Deno'
    _cmd = 'deno'

class Bun(JavaScriptRuntime, JavaScriptPackageManager):
    _name = 'Bun'
    _cmd = 'bun'
    _install_cmd = 'add'

    @classmethod
    def restore(cls, omit: list[Literal['dev', 'optional', 'peer']] | None = None) -> bool:
        pass

    @classmethod
    def install(cls, packages: list[str]) -> dict[str, bool]:
        pass

    @classmethod
    def install_dev(cls, dev_packages: list[str]) -> dict[str, bool]:
        pass

class NPM(JavaScriptPackageManager):
    _name = 'npm'
    _cmd = 'npm'
    _install_cmd = 'install'

    @classmethod
    def restore(cls, omit: list[Literal['dev', 'optional', 'peer']] | None = None) -> bool:
        pass

    @classmethod
    def install(cls, packages: list[str]) -> dict[str, bool]:
        pass

    @classmethod
    def install_dev(cls, dev_packages: list[str]) -> dict[str, bool]:
        pass


class Yarn(JavaScriptPackageManager):
    _name = 'Yarn'
    _cmd = 'yarn'
    _install_cmd = 'add'

    @classmethod
    def restore(cls, omit: list[Literal['dev', 'optional', 'peer']] | None = None) -> bool:
        pass

    @classmethod
    def install(cls, packages: list[str]) -> dict[str, bool]:
        pass

    @classmethod
    def install_dev(cls, dev_packages: list[str]) -> dict[str, bool]:
        pass

class PNPM(JavaScriptPackageManager):
    _name = 'pnpm'
    _cmd = 'pnpm'
    _install_cmd = 'install'

    @classmethod
    def restore(cls, omit: list[Literal['dev', 'optional', 'peer']] | None = None) -> bool:
        pass

    @classmethod
    def install(cls, packages: list[str]) -> dict[str, bool]:
        pass

    @classmethod
    def install_dev(cls, dev_packages: list[str]) -> dict[str, bool]:
        pass