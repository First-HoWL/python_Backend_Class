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

# @shecktime
# @make_prettier("*")
# @cycleFor(5)
# def helloworld(msg):
#     print(msg)

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

# some_list = [6, [21, 4, 1,[ 4, 6, 1], 3, 1], 3, [32, 9, 0], [1, [3, [3, 9]]], 0]


# for i in check_list(some_list):
#     print(i, end=", ")




def stopper(times):

    def decorator(func):
        allready = 0
        def wrapper(*args, **kwargs):
            nonlocal allready
            if (allready >= times):
                raise Exception("NO!")
            else:
                allready += 1
                func(*args, **kwargs)

        return wrapper
    return decorator

@stopper(2)
def helloworld(msg):
    print(msg)

# try:
#     helloworld("print")
#     helloworld("print")
#     helloworld("print")
#     helloworld("print")
#     helloworld("print")
#     helloworld("print")
# except Exception as e:
#     print(f"Exeption: {e}")
#

student = [
    {"name": "John", "age": "9", "grades": [9, 2, 12, 2, 11, 9]},
    {"name": "HoWL", "age": "16", "grades": [11, 12, 10, 12, 11, 9]},
    {"name": "Name", "age": "8", "grades": [2, 2, 6, 3, 7, 8]},
    {"name": "A Cool Name", "age": "13", "grades": [9, 6, 12, 8, 9, 9]},
    {"name": "Not Cool Name", "age": "13", "grades": [9, 6, 12, 8, 9, 9]},
    {"name": "Cool Name", "age": "13", "grades": [9, 6, 12, 8, 9, 9]}
]

# 1.  sorted_student = sorted(student, key = lambda x: int(x["age"]))

# 2.  sorted_student = sorted(student, key = lambda x: sum(x["grades"]) / len(x["grades"]), reverse = True)

# 3. sorted_student = sorted(student, key = lambda x: (-(sum(x["grades"]) / len(x["grades"])), x["name"]))




#
# updated_student = list(map(lambda x: x["avg"] = sum(x["grades"]) / len(x["grades"]), student))
#
# for student in updated_student:
#     print(student)

# sorted_student = sorted(student, key = lambda x: x["avg"] (-(sum(x["grades"]) / len(x["grades"])), x["name"]))
#
# for student in sorted_student:
#     print(student)

