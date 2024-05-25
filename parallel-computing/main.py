import time
from threading import Thread


def fazer_algo(segundos: int = 10):
    print(f"dormindo por {segundos} segundo...")
    time.sleep(segundos)
    print("terminado")


# using sequential
start = time.perf_counter()

fazer_algo()
fazer_algo()

end = time.perf_counter()

# using processes
# start = time.perf_counter()

# t1 = Thread(target=fazer_algo)
# t2 = Thread(target=fazer_algo)

# t1.start()
# t2.start()

# t1.join()
# t2.start()

# end = time.perf_counter()

# using fors
# start = time.perf_counter()

# threads = []
# for _ in range(10):
#     t1 = Thread(target=fazer_algo)
#     t1.start()
#     threads.append(t)

# for thread in threads:
#     thread.join()

# end = time.perf_counter()

print(f"Durou em {round(end-start, 2)} segundos")
