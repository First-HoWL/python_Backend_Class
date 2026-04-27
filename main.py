# https://github.com/svitlyi-itstep/PythonWebP35/tree/main  - teacher`s github repo

import time
import random
def make_prettier(symbol = "="):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(symbol*20)
            func(*args, **kwargs)
            print(symbol*20)

        return wrapper
    return decorator
def shecktime(func):
    timestart = time.perf_counter()
    def wrapp(*args, **kwargs):
        func(*args, **kwargs)
        print(f"{round(time.perf_counter() - timestart, 7):.8f} seconds")
    return wrapp

def cycleFor(times, delay = 3):
    def decorator(func):
        def wrapp(*args, **kwargs):
            for i in range(times):
                try:
                    print(f"Attempt {i}...")
                    func(*args, **kwargs)
                    print("WIN!!!!")
                    break
                except:
                    time.sleep(delay)

        return wrapp
    return decorator

@shecktime
@make_prettier("*")
@cycleFor(5)
def helloworld(msg):
    print(msg)

@shecktime
@cycleFor(5, 2)
def roulette(probability = 0.5):
    if random.random() < probability:
        raise Exception()

#helloworld("print")

roulette()