import json
from os import path
from typing import Any, Optional
from src.config.config_data import ConfigData
from src.core.decorators import throws

class CLIConfig: 
    __config_path: str = path.join(path.dirname(__file__), 'config.json')

    @classmethod
    def touch(cls):
        if not path.exists(cls.__config_path) or not path.isfile(cls.__config_path) or not path.getsize(cls.__config_path):
            with open(cls.__config_path, 'w', encoding='utf-8') as file:
                json.dump(ConfigData.default().todict(), file, indent=4)
                return

    @classmethod
    # @throws(ValueError)
    def read(cls, default: bool = False) -> ConfigData:
        if default:
            return ConfigData.default()
        cls.touch()
        with open(cls.__config_path, 'r', encoding='utf-8') as file:
            config_dict = json.load(file)
            return ConfigData.fromdict(config_dict)
        
    @classmethod
    @throws(ValueError)        
    def write(cls, config: Optional[dict] = None, default: bool = False) -> bool:
        if not (bool(config) ^ bool(default)):
            raise ValueError('Either provide a config dictionary, or use the --default flag to reset to default.')
        
        config = config if config is not None else CLIConfig.read(default=True).todict()

        ConfigData.fromdict(config)

        cls.touch()
        with open(cls.__config_path, 'w', encoding='utf-8') as file:
            json.dump(ConfigData.default().todict() if default else config, file, indent=4)
            return True

    @classmethod
    def deep_read(cls, keys: list[str], default: bool = False) -> Any:
        cls.touch()
        config = ConfigData.default() if default else cls.read()
        config_dict = config.todict()

        current: Any = config_dict
        for key in keys:
            if not isinstance(current, dict):
                return None
            current = current.get(key)
            if current is None:
                return None
        return current
    
    @classmethod
    def deep_write(cls, keys: list[str], value: Any = None, default: bool = False) -> bool:
        cls.touch()

        if not keys or not (bool(value) ^ bool(default)):
            return False

        target = cls.read().todict()
        new_value = None

        if default:
            source = ConfigData.default().todict()
            current = source
            for key in keys:
                if not isinstance(current, dict):
                    return False
                current = current.get(key)
                if current is None:
                    return False
            new_value = current
        else:
            new_value = value

        if new_value is None:
            return False

        current = target
        for key in keys[:-1]:
            if not isinstance(current, dict):
                return False
            if key not in current:
                return False
            current = current.get(key)

        if not isinstance(current, dict):
            return False
        current[keys[-1]] = new_value

        return cls.write(target)