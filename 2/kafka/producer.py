import json
import random
import time
from time import sleep

from confluent_kafka import Producer

SLEEP_BUFFER = 0.1

KAFKA_CONFIG = {"bootstrap.servers": "localhost:29092"}
PRODUCER = Producer(KAFKA_CONFIG)
TOPIC = "credit-card-transactions"


def delivery_report(err, msg):
    """Called once for each message produced to indicate delivery result.
    Triggered by poll() or flush()."""
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")


def generate_transaction():
    """Generate a random credit card transaction."""
    transaction = {
        "transaction_id": random.randint(100000, 999999),
        "card_number": f"{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
        "amount": round(random.uniform(1.00, 1000.00), 2),
        "currency": random.choice(["USD", "EUR", "GBP", "BRL"]),
        "timestamp": int(time.time()),
    }
    return transaction


def main():
    try:
        while True:
            sleep(SLEEP_BUFFER)
            transaction = generate_transaction()
            transaction_json = json.dumps(transaction)

            # Produce the message asynchronously
            PRODUCER.produce(
                TOPIC, transaction_json.encode("utf-8"), callback=delivery_report
            )

            PRODUCER.poll(1)  # wait UP TO 1 sec, callbacks invoked here

    except KeyboardInterrupt:
        pass
    finally:
        PRODUCER.flush()


if __name__ == "__main__":
    main()
