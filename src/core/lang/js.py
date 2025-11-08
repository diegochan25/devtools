from abc import ABC, abstractmethod

from src.core.lib import Executable

class JavaScriptModuleSystem(ABC):
    @classmethod
    @abstractmethod
    def import_stmt(cls) -> str:
        pass
    
    @classmethod
    @abstractmethod
    def export_stmt(cls) -> str:
        pass

class JavaScriptRuntime(Executable):
    pass

class JavaScriptPackageManager(Executable):
    pass