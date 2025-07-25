"""
Multiple parallel execution
"""

import multiprocessing
import time


def do_something():
    print("sleeping 1 second...")
    time.sleep(1)
    print("done sleeping.")


def main():
    t0 = time.perf_counter()

    p = multiprocessing.Process(target=do_something)  # dispatcher
    p.start()  # inicia
    p.join()  # espera finalizar

    # processes = []
    # for _ in range(10):  # inicia todos os processos
    #     p = multiprocessing.Process(target=do_something)
    #     p.start()  # inicia
    #     processes.append(p)

    # for p in processes:  # espera todos ao mesmo tempo (collect)
    #     p.join()

    t1 = time.perf_counter()

    delta = t1 - t0
    print(f"Finished in {round(delta, 2)} seconds")


if __name__ == "__main__":
    main()
