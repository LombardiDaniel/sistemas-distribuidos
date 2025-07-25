"""
https://www.cs.usfca.edu/~galles/visualization/QueueArray.html

Work Queue example

E quando não queremos esperar a execução terminar? Vamos apenas executando
(exemplo: telemetria, coleta e processamento de dados contínua)
"""

import multiprocessing as mp
import random
import time
from datetime import datetime

WORKERS_COUNT = 4

QUEUE = mp.Queue()


def process_data(numbers: list[float]) -> float:
    return sum(numbers) / len(numbers)


def work(worker_id: int, queue: mp.Queue):
    print(f"WORKER_{worker_id}: init")
    while True:
        task = queue.get()  # Hangs until a task is rcvd
        print(f"WORKER_{worker_id}: task rcvd: {task['id']}")

        start = datetime.now()
        res = process_data(task["numbers"])
        time.sleep(5)
        end = datetime.now()

        print(
            f"WORKER_{worker_id}: task {task['id']}: {res} done in {(end - start).total_seconds()}s"
        )


def main():
    """main"""

    for worker_id in range(WORKERS_COUNT):
        p = mp.Process(
            target=work,
            args=(worker_id, QUEUE),
        )
        p.start()

    task_id = 0
    print("Clique [ENTER] para enviar uma tarefa, [CTRL+C] para sair.")
    while input() == "":
        task_id += 1
        task = {
            "id": task_id,
            "numbers": [random.randint(0, 1000) for _ in range(10_000)],
        }
        QUEUE.put(task)
        print("main: task sent!")


if __name__ == "__main__":
    main()
