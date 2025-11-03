import re
import subprocess
from abc import ABC, abstractmethod
from subprocess import CalledProcessError

class JSRuntime(ABC):
    _name: str
    _cmd: str

    @classmethod
    def get_version(cls) -> tuple[int, int, int] | None:
        try:
            stdout = subprocess.run(
                f"{cls._cmd} --version",
                shell=True,
                capture_output=True,
                text=True
            ).stdout

            if (match := re.search(r"\bv?(\d+\.\d+\.\d+)\b", stdout)) is not None:
                version_str = match.group(1)
                return tuple(map(int, version_str.split('.')))
            return None
        except CalledProcessError:
            return None

class JSModuleSystem(ABC):
    @classmethod
    @abstractmethod
    def import_stmt(cls) -> str:
        pass
    
    @classmethod
    @abstractmethod
    def export_stmt(cls) -> str:
        pass

class JSPackageManager(ABC):
    @classmethod
    @abstractmethod
    def get_version(cls) -> str:
        pass

    @abstractmethod
    def install(self, package_name: str) -> bool:
        pass
    
    @abstractmethod
    def uninstall(self, package_name: str) -> bool:
        pass
    
    @abstractmethod
    def init(self, package_name: str) -> bool:
        pass

class NodeJS(JSRuntime):
    _name = 'Node.js'
    _cmd = 'node'
    pass

class Deno(JSRuntime):
    _name = 'Deno'
    _cmd = 'deno'

class Bun(JSRuntime, JSPackageManager):
    _name = 'Bun'
    _cmd = 'bun'

class CommonJS(JSModuleSystem):
    @classmethod
    def import_stmt(cls) -> str:
        pass
    
    @classmethod
    def export_stmt(cls) -> str:
        pass

class ES6(JSModuleSystem):
    @classmethod
    def imports(cls) -> str:
        pass
    
    @classmethod
    def export_stmt(cls) -> str:
        pass

class NPM(JSPackageManager):
    pass

class PNPM(JSPackageManager):
    pass

class Yarn(JSPackageManager):
    pass