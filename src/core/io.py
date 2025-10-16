green = lambda *args, sep=' ': f"{'\033[32m'}{sep.join(args)}{'\033[0m'}"
red = lambda *args, sep=' ': f"{'\033[31m'}{sep.join(args)}{'\033[0m'}"
yellow = lambda *args, sep=' ': f"{'\033[33m'}{sep.join(args)}{'\033[0m'}"
blue = lambda *args, sep=' ': f"{'\033[34m'}{sep.join(args)}{'\033[0m'}"
gray = lambda *args, sep=' ': f"{'\033[90m'}{sep.join(args)}{'\033[0m'}"

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