import random
import sys
import threading
from datetime import datetime
from time import sleep

import models
from confluent_kafka import Producer

SLEEP_BUFFER = 0.01

KAFKA_CONFIG = {"bootstrap.servers": "localhost:9092"}
PRODUCER = Producer(KAFKA_CONFIG)
TOPIC = "user-events-telemetry-sa"

USER_IDS: list[str] = []
with open("users.txt", "r", encoding="utf-8") as f:
    USER_IDS = f.readlines()


def delivery_report(err, msg):
    """called on message production"""
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")


def generate_event() -> models.TelemetryEvent:
    """Generate a random telemetry measurement"""

    event = models.TelemetryEvent(
        user_id=random.choice(USER_IDS),
        action=random.choice(list(models.ActionTypes)).name,
        timestamp=datetime.now(),
    )

    return event


def main():
    try:
        while True:
            sleep(SLEEP_BUFFER)
            event = generate_event()

            # Produce the message asynchronously
            PRODUCER.produce(TOPIC, event.dump(), callback=delivery_report)

            PRODUCER.poll(0.1)  # wait UP TO 0.1 sec, callbacks invoked here

    except KeyboardInterrupt:
        pass
    finally:
        PRODUCER.flush()


if __name__ == "__main__":
    count = 1
    if len(sys.argv) > 1:
        count = int(sys.argv[1])

    for _ in range(count - 1):
        threading.Thread(target=main).start()
    main()
