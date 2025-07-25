import json
from uuid import uuid4

import pika


def main():
    """main"""
    parameters = pika.ConnectionParameters(
        "localhost",
        5672,
        "/",
        pika.PlainCredentials("itiufscar", "itiufscar"),
    )
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    queue_name = "compile.queue"
    channel.queue_declare(queue=queue_name)

    message = json.dumps(
        {
            "msgId": str(uuid4()),
            "repo": "my-example-repository",
            "branch": "prod",
        }
    )
    channel.basic_publish(exchange="", routing_key=queue_name, body=message)
    print(f" [x] Sent {message}")

    connection.close()


if __name__ == "__main__":
    main()
