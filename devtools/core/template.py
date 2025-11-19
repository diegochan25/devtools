import json
from os import linesep, path
from typing import Literal
from devtools.core.io import die

class Template:
    __filename: str
    __contents: list[str] | dict

    @property
    def filename(self) -> str:
        return self.__filename

    @property
    def contents(self) -> list[str] | dict:
        return self.__contents
    
    @property
    def ext(self) -> str:
        return path.splitext(self.__filename)[1].removesuffix('.')

    def render(self) -> str:
        if isinstance(self.__contents, list):
            return linesep.join(self.__contents)
        elif isinstance(self.__contents, dict):
            return json.dumps(self.__contents, indent=4)
        return str(self.__contents)
    
    def touch(self, at: str) -> Literal[True]:
        abspath = path.abspath(path.join(at, self.filename))

        if path.exists(abspath) and path.isfile(abspath) and path.getsize(abspath):
            die(f"File at {abspath} exists and is not empty.")
        else:
            try:
                with open(abspath, 'w', encoding='utf-8') as file:

                    file.write(self.render())
                    return True
            except: 
                die(f"There was an error writing to the file at {abspath}")

    def __init__(self, filename: str, contents: list[str] | dict):
        self.__filename = filename
        self.__contents = contents if isinstance(contents, dict) else [ln for ln in contents if ln is not None] if isinstance(contents, list) else []