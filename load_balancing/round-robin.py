import random
import string
import time

SERVERS = [
    "server1",
    "server2",
    "server3",
]


def send_request(server: str, req: str):
    print(f"{server}::{req}")
    time.sleep(0.1)


def gen_random_str(length=10):
    return "".join(random.choice(string.ascii_letters) for i in range(length))


def main():
    requests = [gen_random_str() for _ in range(100)]

    servers_idx = 0
    for req in requests:
        server_to_send = SERVERS[servers_idx % len(SERVERS)]
        send_request(server_to_send, req)
        servers_idx += 1


if __name__ == "__main__":
    main()
