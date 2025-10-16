from typing import Any, Callable
from src.core.io import die

def abortable(fn: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except KeyboardInterrupt:
            die(f"Execution of method '{fn.__qualname__}' interrupted by user.")
    return wrapper

def requires(*keys: str) -> Callable[..., Any]:
    def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args, **kwargs):
            for key in keys:
                if key not in kwargs:
                    die(f"Missing required key '{key}' in argument list for method '{fn.__qualname__}'.")
            return fn(*args, **kwargs)
        return wrapper
    return decorator