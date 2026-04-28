# TODO: https://github.com/svitlyi-itstep/PythonWebP35/tree/main  - teacher`s github repo

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

def fibonacci_up_to(n):
    a, b = 0, 1
    while a <= n:
        yield a
        a, b = b, a + b

def num_list(n):
    i = 0
    while i < len(n):
        yield (i, n[i])
        i += 1

# gen = fibonacci_up_to(10000)

# for num in gen:
#     print(num)

# roulette()

# list = [x for x in fibonacci_up_to(10000)]
#
# for i, x in num_list(list):
#     print(f"{i}. {x}")


def count():
    sum = 0
    count = 0
    while True:
        value = yield
        sum += value
        count += 1
        yield sum / count

# gen = count()
#
# for i in range(1, 10):
#     next(gen)
#     print(gen.send(i))
#
# next(gen)
# print(gen.send(100))


def check_list(listss):
    for item in listss:
        if isinstance(item, list):
            yield from check_list(item)
        else:
            yield item

some_list = [6, [21, 4, 1,[ 4, 6, 1], 3, 1], 3, [32, 9, 0], [1, [3, [3, 9]]], 0]


for i in check_list(some_list):
    print(i, end=", ")


