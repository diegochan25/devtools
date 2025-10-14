from abc import ABC, abstractmethod
import re
import subprocess
from subprocess import CalledProcessError

from Output import red

class JSRuntime(ABC):
    _name: str
    _cmd: str

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def cmd(self) -> str:
        return self._cmd
    
    def __repr__(self):
        return f"<JavaScript runtime: {self._name}>"
    
    def get_version(self) -> tuple[int, int, int]:
        try:
            result = subprocess.run(f"{self._cmd} --version", shell=True, check=True, capture_output=True, text=True)
        except CalledProcessError:
            print(red(f"{self._name} was not found on this system."))
            exit(1)
        else:
            match = re.search(r"v?(\d+)\.(\d+)\.(\d+)", result.stdout)
            if not match:
                print(red(f"Failed to parse version of {self._name}. Output was:\n{result.stdout}"))
                exit(1)
            
            major, minor, patch = match.groups()
            return (int(major), int(minor), int(patch))

class Node(JSRuntime):
    def __init__(self):
        self._name = "Node"
        self._cmd = "node"

class Deno(JSRuntime):
    def __init__(self):
        self._name = "Deno"
        self._cmd = "deno"

class Bun(JSRuntime):
    def __init__(self):
        self._name = "Bun"
        self._cmd = "bun"

class JSPackageManager(ABC):
    _name: str
    _cmd: str

class JS():
    _runtime: JSRuntime
    _package_manager: JSPackageManager

    @property
    def runtime(self) -> JSRuntime:
        return self._runtime
    
    @runtime.setter
    def runtime(self, value: JSRuntime):
        self._runtime = value
    
    @property
    def package_manager(self) -> JSPackageManager:
        return self._package_manager
    
    @package_manager.setter
    def package_manager(self, value: JSPackageManager):
        self._package_manager = value


print(Node().get_version())