from cli.Output import red, white


def abortable(fn):
    def wrapper(*args, **kwargs):
        try:
            fn(*args, **kwargs)
        except KeyboardInterrupt:
            print(red(f"Execution of function '{fn.__name__}' aborted by user."))
            exit(1)
    return wrapper

def requires(*attrs: tuple[str]):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            missing_attrs = [attr for attr in attrs if attr not in kwargs]
            if missing_attrs:
                print(red(f"Method '{fn.__qualname__}' was called with missing required attributes: {', '.join(missing_attrs)}"))
                exit(1)
            return fn(*args, **kwargs)
        return wrapper
    return decorator