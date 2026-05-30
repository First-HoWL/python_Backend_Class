import time
from datetime import datetime


# Завдання 1

def logger(func):
    def wrapper(*args, **kwargs):
        t = datetime.now().strftime("%H:%M")
        print(f"[{t}] Викликано функцію {func.__name__}")
        with open("log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{t}] Викликано функцію {func.__name__}\n")
        return func(*args, **kwargs)
    return wrapper

@logger
def helloworld():
    pass

@logger
def add(a, b):
    return a + b

helloworld()
result = add(2, 3)


# Завдання 2

def chunked(iterable, n):
    chunk = []
    for item in iterable:
        chunk.append(item)
        if len(chunk) == n:
            yield chunk
            chunk = []
    if chunk:
        yield chunk

for chunk in chunked([1, 2, 3, 4, 5], 2):
    print(chunk)
