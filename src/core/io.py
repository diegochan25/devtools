from typing import Literal

def s(
        *args: str,
        fg: Literal['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'gray', 'white'] | None = None,
        bg: Literal['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'gray', 'white'] | None = None,
        end: str = '',
        sep: str = ' '
) -> str:
    foreground = {
        'red': '\x1b[31m',
        'green': '\x1b[32m',
        'yellow': '\x1b[33m',
        'blue': '\x1b[34m',
        'magenta': '\x1b[35m',
        'cyan': '\x1b[36m',
        'gray': '\x1b[90m',
        'white': '\x1b[97m'
    }

    background = {
        'red': '\x1b[41m',
        'green': '\x1b[42m',
        'yellow': '\x1b[43m',
        'blue': '\x1b[44m',
        'magenta': '\x1b[45m',
        'cyan': '\x1b[46m',
        'gray': '\x1b[100m',
        'white': '\x1b[107m'
    }

    stop = '\x1b[0m'

    styles = (foreground[fg] if fg is not None else '') + (background[bg] if bg is not None else '')

    return (styles if styles else '') + sep.join(args) + (stop if styles else '') + end

def log(*values: object, end: str = '\n', sep: str = ' ', fg: Literal['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'gray', 'white'] = 'red'):
    print(s(*[str(v) for v in values], fg=fg, end=end, sep=sep))

def die(*values: object, end: str = '\n', sep: str = ' ', code: int = 1, fg: Literal['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'gray', 'white']= 'red'):
    print(s(*[str(v) for v in values], fg=fg, end=end, sep=sep))
    exit(code)