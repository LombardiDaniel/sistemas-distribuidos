import json
import random
import time

import pika


def main():
    parameters = pika.ConnectionParameters(
        "localhost",
        5672,
        "/",
        pika.PlainCredentials("ufscar", "iti"),
    )
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    queue_name = "tasks.queue.daniel-lombardi"
    channel.queue_declare(queue=queue_name)

    while True:
        message = json.dumps(
            {
                "id": random.randint(0, 99999),
                "text": "hello!",
            }
        )
        channel.basic_publish(exchange="", routing_key=queue_name, body=message)
        print(f" [x] Sent {message}")
        time.sleep(0.5)

    connection.close()


if __name__ == "__main__":
    main()
