from typing import Any

from src.core.io import blue, gray, yellow

def deep_attr(dictionary: dict, keys: list[str]) -> Any:
    current = dictionary
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else: 
            return None
    return current

def deep_set(dictionary: dict, keys: list[str], value: Any) -> bool:
    current = dictionary
    for key in keys[:-1]:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return False

    last_key = keys[-1]
    if isinstance(current, dict) and last_key in current:
        current[last_key] = value
        return True
    return False

def pretty(data: Any, i: int = 0):
    lines = []
    tab = ' ' * (4 * i)
    if isinstance(data, dict):
        for key, value in data.items():
            lines.append(f"{tab}{key}:{'\n' if isinstance(value, (dict, list)) else ' '}")
            lines.append(pretty(value, i + 1))
    elif isinstance(data, list):
        for item in data:
            lines.append(f"{tab}-{'\n' if isinstance(item, (dict, list)) else ' '}")
            lines.append(pretty(item, i + 1))
    else:
        if isinstance(data, str):
            lines.append(blue(f"'{data}'"))
        elif data is None:
            lines.append(gray('None'))
        else:
            lines.append(yellow(str(data)))
        lines.append('\n')

    return ''.join(lines).strip('\n')