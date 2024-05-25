import json
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

    queue_name = "tasks.queue"
    channel.queue_declare(queue=queue_name)

    message = json.dumps(
        {
            "text": "hello!",
        }
    )

    while True:
        channel.basic_publish(exchange="", routing_key=queue_name, body=message)
        print(f" [x] Sent {message}")
        time.sleep(0.5)

    connection.close()


if __name__ == "__main__":
    main()
