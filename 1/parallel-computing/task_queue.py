"""
https://www.cs.usfca.edu/~galles/visualization/QueueArray.html

Queue workers example

E quando não queremos esperar a execução terminar? Vamos apenas executando
(exemplo: telemetria, coleta e processamento de dados contínua)
"""

import math
import multiprocessing as mp
import time
from datetime import datetime

WORKERS_COUNT = 4

QUEUE = mp.Queue()


def process_data(numbers: list[float]) -> float:
    """Processes the given data"""
    results = []
    for number in numbers:
        results.append(math.sqrt(number**5))

    res = 0
    for result in results:
        res += result

    return res


def work(worker_id: int, queue: mp.Queue):
    """Executes a task"""
    print(f"WORKER_{worker_id}: init")
    while True:
        task = queue.get()  # Hangs until a task is rcvd
        print(f"WORKER_{worker_id}: task rcvd: {task['id']}")

        start = datetime.now()
        res = process_data(task["numbers"])
        time.sleep(5)
        end = datetime.now()

        print(
            f"WORKER_{worker_id}: task {task['id']}:{res} done in {(end - start).total_seconds()}s"
        )


def main():
    """main"""

    for worker_id in range(WORKERS_COUNT):
        p = mp.Process(
            target=work,
            args=(worker_id, QUEUE),
        )
        p.start()

    numbers = [i for i in range(9999999)]

    task_id = 0
    print("Clique [ENTER] para enviar uma tarefa, [CTRL+C] para sair.")
    while input() == "":
        task_id += 1
        task = {
            "id": task_id,
            "numbers": numbers,
        }
        QUEUE.put(task)
        print("main: task sent!")


if __name__ == "__main__":
    main()
