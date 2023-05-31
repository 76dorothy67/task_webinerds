_verbose = True


def log(text): _verbose and print(green(text))
def bold(text): return f"\033[1m{text}\033[0m"
def green(text): return f"\033[32m{text}\033[0m"
def blue(text): return f"\033[34m{text}\033[0m"
def yellow(text): return f"\033[33m{text}\033[0m"
def red(text): return f"\033[31m{text}\033[0m"
move_up = '\x1b[1A'


def verbosity(val: bool):
    global _verbose
    _verbose = val

def verbose(): return _verbose
