import json
from time import sleep

import pika


def work(msg: dict) -> None:
    """processing"""
    print(msg)
    sleep(2)


def callback(ch, method, properties, body):
    """msg callback"""
    ch.basic_ack(delivery_tag=method.delivery_tag)  # <- !!! confirmação
    print(f" [x] Received {body}")
    msg = json.loads(body)
    work(msg)
    # ch.basic_ack(delivery_tag=method.delivery_tag)  # <- !!! confirmação


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
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=False
    )

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    main()
