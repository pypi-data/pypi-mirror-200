from datetime import timedelta
import time


def get_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = timedelta(seconds=end_time - start_time)
        ms = int(elapsed_time.total_seconds() * 1000)
        print("Function {} took {} ms to execute.".format(func.__name__, ms))
        return result

    return wrapper
