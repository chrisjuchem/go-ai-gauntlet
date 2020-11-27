DEBUG = False
INFO = False

def info(*txt):
    if INFO:
        print(*txt)

def debug(*txt):
    if DEBUG:
        print(*txt)