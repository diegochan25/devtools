from os import getcwd, path, scandir
from subprocess import CalledProcessError
import subprocess
from devtools.core.io import die
from devtools.core.lib import Executable

class Git(Executable):
    # inherited from Executable
    name = 'Git'
    _cmd = 'git'
    
    @classmethod
    def init(cls, at: str = getcwd()) -> bool:
        at = path.abspath(at)
        if not path.isdir(at):
            die(f"Path at {at} is not a directory.")
        try:
            subprocess.run(
                f"{cls._cmd} init .",
                cwd=at,
                shell=True,
                check=True,
                capture_output=True
            )
            return True
        except CalledProcessError:
            return False
