import re
import subprocess
from abc import ABC
from copy import deepcopy
from dataclasses import asdict, dataclass, is_dataclass
from devtools.core.io import s
from subprocess import CalledProcessError
from typing import Any, Self, Union, get_args, get_origin

def tostring(data: Any, indent: int = 0) -> str:
    tab = ' ' * (4 * indent)
    lines = []

    if isinstance(data, dict):
        for name, value in data.items():
            lines.append(
                tab + s(f"{name}:", fg='white', end='\n' if isinstance(value, (dict, list, tuple, set)) else ' ') +
                (tostring(value, indent + 1) if isinstance(value, (dict, list, tuple, set)) else tostring(value))
            )
    elif isinstance(data, (list, tuple, set)):
        for item in data:
            lines.append(
                tab + s('-', fg='white', end='\n' if isinstance(item, (dict, list, tuple, set)) else ' ') +
                (tostring(item, indent + 1) if isinstance(item, (dict, list, tuple, set)) else tostring(item))
            )
    elif isinstance(data, str):
        return s(f"'{data}'", fg='green')
    elif data is None:
        return s('None', fg='gray')
    elif isinstance(data, (int, float, bool)):
        return s(str(data), fg='yellow')
    elif hasattr(data, '__name__'):
        return s(data.__name__, fg='magenta')
    else:
        return s(repr(data), fg='magenta')
    
    return '\n'.join(lines)

def parse(value: str) -> str | bool | int | float:
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            if (v := value.strip().lower()) in ('true', 'false'):
                return v == 'true'
            else:
                return str(value).strip().lower()
            
class Serializable(ABC):
    def tostring(self) -> str:
        return tostring(self.todict())

    def todict(self, drop_none: bool = True) -> dict:
        def not_null(d: dict) -> dict:
            result = {}
            for k, v in d.items():
                if v is None:
                    continue
                if isinstance(v, dict):
                    cleaned = not_null(v)
                    if cleaned:
                        result[k] = cleaned
                else:
                    result[k] = v
            return result

        def serialize(value):
            if isinstance(value, Serializable):
                return value.todict(drop_none=drop_none)
            elif is_dataclass(value):
                data = {k: serialize(v) for k, v in asdict(value).items()}
                return not_null(data) if drop_none else data
            elif isinstance(value, dict):
                data = {k: serialize(v) for k, v in value.items()}
                return not_null(data) if drop_none else data
            elif isinstance(value, (list, tuple)):
                return [serialize(v) for v in value]
            else:
                return deepcopy(value)

        base = {k: serialize(v) for k, v in self.__dict__.items()}

        return not_null(base) if drop_none else base

    @classmethod
    def fromdict(cls, dictionary: dict) -> Self:
        kwargs = {}
        annotations = cls.__annotations__

        optional = lambda annotation: type(None) in get_args(annotation) if get_origin(annotation) is Union else False

        for key, classname in annotations.items():
            if key not in dictionary:
                if optional(classname):
                    kwargs[key] = None
                else:
                    raise ValueError(f"Missing required attribute '{key}' in dict.")

            value = dictionary.get(key)

            if isinstance(value, dict):
                if hasattr(classname, 'fromdict'):
                    value = classname.fromdict(value)
                elif is_dataclass(classname):
                    value = classname(**value)
            elif isinstance(value, list):
                origin = get_origin(classname)
                args = get_args(classname)
                if origin in (list, tuple) and args:
                    subtype = args[0]
                    if hasattr(subtype, 'fromdict'):
                        value = [subtype.fromdict(i) if isinstance(i, dict) else i for i in value]
            kwargs[key] = value
        return cls(**kwargs)

@dataclass
class CaseMap(Serializable):
    camel: str
    kebab: str
    pascal: str
    spaced: str
    snake: str
    upper: str

def case_map(string: str) -> CaseMap:
    words = []
    start = 0
    prev = None

    for i in range(len(string)):
        curr = string[i]
        prev = None
        next = None
        if i != 0:
            prev = string[i - 1]
        if i < len(string) - 1:
            next = string[i + 1]
        if prev is not None:
            if curr.isupper() and prev and prev.islower():
                words.append(string[start:i])
                start = i
            if curr.isdigit() and prev.isalpha():
                words.append(string[start:i])
                start = i
            if curr.isalpha() and prev.isdigit():
                words.append(string[start:i])
                start = i
            if next is not None:
                if curr.isupper() and next.islower():
                    words.append(string[start:i])
                    start = i
    words.append(string[start:])

    words = [s.lower() for w in words for substr in w.split('_') for s in substr.split('-') if s]

    return CaseMap(
        camel=''.join([words[0]] + [w.capitalize() for w in words[1:]]),
        kebab='-'.join(words),
        pascal=''.join(w.capitalize() for w in words),
        spaced=' '.join(words),
        snake='_'.join(words),
        upper='_'.join(words).upper()
    )


class Executable(ABC):
    _name: str
    _cmd: str

    @classmethod
    def get_version(cls) -> tuple[int, int, int] | None:
        try:
            output = subprocess.run(
                f"{cls._cmd} --version",
                shell=True,
                check=True,
                capture_output=True,
                text=True
            ).stdout.strip()

            m = re.search(r"\bv?(\d+)(?:\.(\d+))?(?:\.(\d+))?", output)
            if not m:
                return None
            
            groups = m.groups()
            major = int(groups[0]) if groups[0] else 0
            minor = int(groups[1]) if groups[1] else 0
            patch = int(groups[2]) if groups[2] else 0
            return (major, minor, patch)

        except (CalledProcessError, FileNotFoundError):
            return None