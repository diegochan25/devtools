from abc import ABC, abstractmethod
from src.core.lib import Executable

class JavaScriptRuntime(Executable):
    pass

class JavaScriptPackageManager(Executable):
    pass

class JavaScriptModuleSystem(ABC):
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

class NPM(JavaScriptPackageManager):
    _name = 'npm'
    _cmd = 'npm'

class Yarn(JavaScriptPackageManager):
    _name = 'Yarn'
    _cmd = 'yarn'

class PNPM(JavaScriptPackageManager):
    _name = 'pnpm'
    _cmd = 'pnpm'