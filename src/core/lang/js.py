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
        imports: list[str | dict[str, str]] | None = None,
        default: str | None = None
    ) -> str:
        pass

    @classmethod
    @abstractmethod
    def export_stmt(cls) -> str:
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
    def export_stmt(cls) -> str:
        from src.config.rule_set import JavaScriptRules
        rules = JavaScriptRules.generate()
        
        return ''


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
    def export_stmt(cls) -> str:
        from src.config.rule_set import JavaScriptRules
        rules = JavaScriptRules.generate()
        
        return ''

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