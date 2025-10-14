def red(*text: str, end='', sep=' ') -> str:
    return f"\033[31m{sep.join(text)}{end}\033[0m"

def green(*text: str, end='', sep=' ') -> str:
    return f"\033[32m{sep.join(text)}{end}\033[0m"

def yellow(*text: str, end='', sep=' ') -> str:
    return f"\033[33m{sep.join(text)}{end}\033[0m"

def blue(*text: str, end='', sep=' ') -> str:
    return f"\033[34m{sep.join(text)}{end}\033[0m"

def gray(*text: str, end='', sep=' ') -> str:
    return f"\033[90m{sep.join(text)}{end}\033[0m"

def white(*text: str, end='', sep=' ') -> str:
    return f"\033[37m{sep.join(text)}{end}\033[0m"