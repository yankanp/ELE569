import time
from memory_profiler import memory_usage

def factorial_iterative(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def main():
    number = 10000  # You can adjust this number
    start_time = time.time()
    result = factorial_iterative(number)
    end_time = time.time()

    print(f"The factorial of {number} is calculated.")
    print(f"Execution Time: {end_time - start_time} seconds")

if __name__ == "__main__":
    mem_usage = memory_usage(proc=main, interval=1, timeout=1)
    print(f"Peak Memory Usage: {max(mem_usage)} MiB")
