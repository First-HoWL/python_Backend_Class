from datetime import datetime


def generator_logger(func):
    def wrapper(*args, **kwargs):
        for value in func(*args, **kwargs):
            time = datetime.now().strftime("%H:%M")
            message = f"[{time}][LOG] Yield: {value}"
            print(message)
            with open("gen_log.txt", "a", encoding="utf-8") as f:
                f.write(message + "\n")
            yield value
    return wrapper


@generator_logger
def numbers(count):
    for i in range(count):
        yield i


for num in numbers(3):
    print(f"Received: {num}")