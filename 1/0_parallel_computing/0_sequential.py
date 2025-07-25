"""
Sequential vs parallel example
"""

import time


def do_something():
    print("sleeping 1 second...")
    time.sleep(1)
    print("done sleeping.")


def main():
    t0 = time.perf_counter()
    do_something()
    # do_something()
    t1 = time.perf_counter()

    delta = t1 - t0
    print(f"Finished in {round(delta, 2)} seconds")


if __name__ == "__main__":
    main()
