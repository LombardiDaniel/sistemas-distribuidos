import models
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement
from confluent_kafka import Consumer

BATCH_SIZE = 100
KAFKA_CONFIG = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "user-events-telemetry-sa-consumer-group-analytics-prod",
    "auto.offset.reset": "earliest",  # "latest",  # <- !!! recuperação em caso de crash do consumidor
}
CONSUMER = Consumer(KAFKA_CONFIG)
TOPIC = "user-events-telemetry-sa"

CASSANDRA_CLUSTER = Cluster(["127.0.0.1"], port=9042)
CASSANDRA_SESSION = CASSANDRA_CLUSTER.connect("telemetry")


def process(events: list[models.TelemetryEvent]):
    """process event batches"""
    insert_query = CASSANDRA_SESSION.prepare(
        "INSERT INTO user_telemetry (user_id, action, event_time) VALUES (?, ?, ?)"
    )

    batch = BatchStatement()

    for event in events:
        batch.add(
            insert_query,
            (
                event.user_id,
                event.action,
                event.timestamp,
            ),
        )

    CASSANDRA_SESSION.execute(batch)
    print(f"Inserted {BATCH_SIZE} records into Cassandra.")


def main():
    CONSUMER.subscribe([TOPIC])

    batch: list[models.TelemetryEvent] = []

    while True:
        msg = CONSUMER.poll(1.0)  # Wait for a message up to 1 second

        if msg is None:
            continue

        if msg.error():
            print(msg.error())
            continue

        event = models.TelemetryEvent()
        event.load(msg.value())
        batch.append(event)

        if len(batch) == BATCH_SIZE:
            process(batch)
            batch: list[models.TelemetryEvent] = []


if __name__ == "__main__":
    main()
