"""
race condition example
"""

import threading
from time import sleep

LOCK = threading.Lock()

ITERS = 100000
NUM_THREADS = 4
COUNTER = [0]


def add_to_counter_with_lock(counter):
    """adds to global sum"""

    with LOCK:
        for _ in range(ITERS):
            val = counter[0] + 1

            # este sleep força uma troca de contexto
            # (necessário pq nosso código é mt simples/pequeno)
            sleep(0)

            counter[0] = val


def add_to_counter(counter):
    """adds to global sum"""

    for _ in range(ITERS):
        val = counter[0] + 1

        # este sleep força uma troca de contexto
        # (necessário pq nosso código é mt simples/pequeno)
        sleep(0)

        counter[0] = val


def main():
    """main"""
    threads = []
    for _ in range(NUM_THREADS):
        t = threading.Thread(target=add_to_counter, args=(COUNTER,))
        threads.append(t)

    for thread in threads:
        thread.start()

    for t in threads:
        t.join()

    print(f"Expected COUNTER={NUM_THREADS*ITERS}")
    print(f"Got      COUNTER={COUNTER[0]}")


if __name__ == "__main__":
    main()
