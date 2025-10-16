from dataclasses import dataclass
import json
from json import JSONDecodeError
from os import path, getcwd
from typing import Any, Literal

@dataclass 
class PackageJson: 
    name: str | None
    version: str | None
    description: str | None = None
    keywords: list[str] | None = None
    homepage: str | None = None
    bugs: str | dict[Literal['url', 'email'], str] | None = None
    license: str | None = None
    author: str | dict[Literal['name', 'email', 'url'], str] | None = None
    contributors: list[str | dict[Literal['name', 'email', 'url'], str]] | None = None
    funding: str | dict[Literal['type', 'url'], str] | list[str | dict[Literal['type', 'url'], str]] | None = None
    files: list[str] | None = None
    main: str | None = None
    module: str | None = None
    browser: str | None = None
    bin: str | dict[str, str] | None = None
    man: str | list[str] | None = None
    directories: dict[Literal['doc', 'lib', 'bin', 'man']] | None = None
    repository: str | dict[Literal['type', 'url', 'directory'], str] | None = None
    scripts: dict[str, str] | None = None
    config: dict[str, str] | None = None
    dependencies: dict[str, str] | None = None
    dev_dependencies: dict[str, str] | None = None
    peer_dependencies: dict[str, str] | None = None
    peer_dependencies_meta: dict[str, str] | None = None
    bundled_dependencies: list[str] | None = None
    optional_dependencies: dict[str, str] | None = None
    engines: dict[str, str] | None = None
    os: list[str] | None = None
    cpu: list[str] | None = None
    private: bool | None = None
    publish_config: dict[str, str] | None = None
    workspaces: list[str] | dict[Literal['packages', 'nohoist'], list[str]] | None = None

    def dict(self):
        return self.__dict__

class JS:
    @staticmethod
    def find_package_json(dir: str = getcwd()) -> str | None:
        cwd = path.abspath(dir)
        while not path.abspath(cwd) == path.abspath(path.dirname(cwd)):
            package_json_path = path.join(cwd, 'package.json')
            if path.isfile(package_json_path):
                return package_json_path
            else:
                cwd = path.dirname(cwd)
        return None
    @staticmethod
    def load_package_json(package_json_path: str) -> PackageJson | None:
        if path.isfile(package_json_path):
            with open(package_json_path, 'r', encoding='utf-8') as file:
                try:
                    package_json_dict = json.load(file)
                except JSONDecodeError:
                    return None
                keymap = {
                    'devDependencies': 'dev_dependencies',
                    'peerDependencies': 'peer_dependencies',
                    'peerDependenciesMeta': 'peer_dependencies_meta',
                    'bundledDependencies': 'bundled_dependencies',
                    'optionalDependencies': 'optional_dependencies',
                }

                for camel, snake in keymap.items():
                    if camel in package_json_dict:
                        package_json_dict[snake] = keymap.pop(camel)

                return PackageJson(**package_json_dict)
        else:
            return None
        
    def dump_package_json(package_json_path: str, package_json_dict: dict[str, Any]):
        try:
            PackageJson(**package_json_dict)
        except TypeError:
            return None
        if path.isfile(package_json_path):
            with open(package_json_path, 'r+', encoding='utf-8') as file:
                json.dump(package_json_dict, file, indent=4)
        else:
            return None
