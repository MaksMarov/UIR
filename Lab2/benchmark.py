import time

benchmark_results = {}

def benchmark(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        benchmark_results[func.__name__] = elapsed_time
        return result
    return wrapper