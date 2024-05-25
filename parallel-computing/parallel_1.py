"""
Multiprocessing example

workers concept
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

    numbers = [i * 2 for i in range(9999999)]
    total_data = [numbers for i in range(PROCESSES_COUNT)]

    start = datetime.now()
    res = []
    for data in total_data:
        res.append(process_data(data))
    end = datetime.now()
    print(f"Sequencial: {(end - start).total_seconds()}s")

    start = datetime.now()
    processes = []
    for data in total_data:
        p = mp.Process(target=process_data, args=(data,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()  # no need for ret because we would store it in a database
    end = datetime.now()
    print(f"Parallel: {(end - start).total_seconds()}s")


if __name__ == "__main__":
    main()
