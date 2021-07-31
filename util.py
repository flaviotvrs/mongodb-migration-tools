from datetime import datetime

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_warning(message):
    print_message(message, bcolors.WARNING)

def print_fail(message):
    print_message(message, bcolors.FAIL)

def print_success(message):
    print_message(message, bcolors.OKGREEN)

def print_info(message):
    print("[" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "] " + message + bcolors.ENDC)

def print_message(message, color):
    print(color + "[" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "] " + message + bcolors.ENDC)

def str2bool(str):
    return str.strip().lower() in ("true", "yes", "1")
