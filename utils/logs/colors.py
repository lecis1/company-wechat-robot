HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
CYAN = '\033[96m'


def ok_wrapper(string):
    return f'{OKGREEN}{string}{ENDC}'


def fail_wrapper(string):
    return f'{FAIL}{string}{ENDC}'


def warning_wrapper(string):
    return f'{WARNING}{string}{ENDC}'


def debug_wrapper(string):
    return f'{CYAN}{string}{ENDC}'