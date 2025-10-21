def green(*args, sep=' '):
    return f"{'\033[32m'}{sep.join(args)}{'\033[0m'}"
    
def red(*args, sep=' '):
    return f"{'\033[31m'}{sep.join(args)}{'\033[0m'}"
    
def yellow(*args, sep=' '):
    return f"{'\033[33m'}{sep.join(args)}{'\033[0m'}"
    
def blue(*args, sep=' '):
    return f"{'\033[34m'}{sep.join(args)}{'\033[0m'}"
    
def gray(*args, sep=' '):
    return f"{'\033[90m'}{sep.join(args)}{'\033[0m'}"

def white(*args, sep=' '):
    return f"\033[97m{sep.join(args)}\033[0m"

def ask(question: str) -> str:
    answer: str | None = None
    while answer is None:
        answer = str(input(f"{blue(question)}\n")).strip()
        if not answer:
            print(yellow("Please provide an answer"))
            answer = None
    return answer

def die(message: str, code: int = 1) -> None:
    print(red(message))
    exit(code)

def done(message: str, code: int = 0) -> None:
    print(green(message))
    exit(code)