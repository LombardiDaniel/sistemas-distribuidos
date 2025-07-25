"""
Multiprocessing example

classic
"""

import math
import multiprocessing as mp
from datetime import datetime

PROCESSES_COUNT = 8


def process_data(numbers: list[float]) -> float:
    """Processes the given data"""
    results = []
    for number in numbers:
        results.append(math.sqrt(number**5))

    res = 0
    for result in results:
        res += result

    return res


def main():
    """main"""

    numbers = [float(i) * 2 for i in range(9999999)]

    chunk_size = int(len(numbers) / PROCESSES_COUNT)

    start = datetime.now()
    process_data(numbers)
    end = datetime.now()
    print(f"Sequencial: {(end - start).total_seconds()}s")

    start = datetime.now()
    processes = []
    for i in range(0, len(numbers), chunk_size):
        p = mp.Process(target=process_data, args=(numbers[i : i + chunk_size],))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()  # no need for ret because we would store it in a database
    end = datetime.now()
    print(f"Parallel: {(end - start).total_seconds()}s")


if __name__ == "__main__":
    main()
