import json
from dataclasses import dataclass
from os import makedirs, path
from src.core.io import die
from typing import Any

@dataclass 
class Template:
    filename: str
    contents: list[str] | dict[str | int, Any]
    
    def write(self, at: str):
        abs_path = path.abspath(path.join(at, self.filename))
        if path.exists(abs_path):
            with open(abs_path, 'r', encoding='utf-8') as f:
                if f.read():
                    die(f"File at {abs_path} exists and is not empty. Aborting to avoid overriding.")
                    
        makedirs(path.dirname(abs_path), exist_ok=True)
        with open(abs_path, 'w+', encoding='utf-8') as file:
            if isinstance(self.contents, list):
                file.write('\n'.join(self.contents))
            elif isinstance(self.contents, dict):
                file.write(json.dumps(self.contents, indent=4))