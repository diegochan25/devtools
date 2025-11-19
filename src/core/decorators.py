from os import linesep
from typing import ParamSpec, Type, Callable, Any, TypeVar
from src.core.io import die, s

R = TypeVar('R')
P = ParamSpec('P')

def throws(*exceptions: Type[BaseException]) -> Callable[P, R]:
    def decorator(fn: Callable[P, R]) -> Callable[P, R]:
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            try: 
                return fn(*args, **kwargs)
            except exceptions as e:
                die(
                    f"Exception of type {type(e).__name__} in {fn.__qualname__} caused the application to stop.", 
                    s(str(e), fg='gray'),
                    sep=linesep,
                )
                raise
        return wrapper
    return decorator

def requires(*values: str) -> Callable[P, R]:
    def decorator(fn: Callable[P, R]) -> Callable[P, R]:
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            for val in values:
                if val not in kwargs:
                    die(f"Missing required key '{val}' in kwargs for {fn.__qualname__}.")
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def abortable(fn: Callable[P, R]) -> Callable[P, R]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            return fn(*args, **kwargs)
        except KeyboardInterrupt:
            die(f"Execution of method {fn.__qualname__} interrupted by user using Ctrl + C.")
    return wrapper
