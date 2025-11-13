import json
from os import path
from src.core.io import die

class Template:
    _filename: str
    _contents: list[str] | dict

    @property
    def filename(self) -> str:
        return self._filename
    
    @filename.setter
    def filename(self, value: str) -> None:
        self._filename = value

    @property
    def contents(self) -> list[str] | dict:
        return self._contents
    
    @contents.setter
    def contents(self, value: list[str] | dict):
        self._contents = value

    @property
    def ext(self) -> str:
        return path.splitext(self._filename)[1].removesuffix('.')

    def render(self) -> str:
        if isinstance(self._contents, list):
            return '\n'.join(self._contents)
        elif isinstance(self._contents, dict):
            return json.dumps(self._contents, indent=4)
        return str(self._contents)
    
    def touch(self, at: str) -> bool:
        abspath = path.abspath(path.join(at, self.filename))

        if path.exists(abspath) and path.isfile(abspath) and path.getsize():
            die(f"File at {abspath} exists and is not empty.")
        
        with open(abspath, 'w', encoding='utf-8') as file:
            file.write(self.render())

    def __init__(self, filename: str, contents: list[str] | dict):
        self._filename = filename
        self._contents = contents