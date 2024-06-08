import json

from confluent_kafka import OFFSET_BEGINNING, Consumer

KAFKA_MAX_HISTORY_DEPTH_ROLLBACK = 5

KAFKA_CONFIG = {
    "bootstrap.servers": "localhost:29092",
    "group.id": "credit-card-consumer-group-analytics-prod",
    "auto.offset.reset": "latest",  # "earliest",  # <- !!! recuperação em caso de crash
}

CONSUMER = Consumer(KAFKA_CONFIG)
TOPIC = "credit-card-transactions"


def process_transaction(transaction):
    """Process the credit card transaction."""
    print(f"Processing transaction: {transaction}")


# def kafka_on_assign_callback_rollback(consumer, topic_partitions):
#     for topic_partition in topic_partitions:
#         min_offset, max_offset = consumer.get_watermark_offsets(
#             topic_partition, cached=False
#         )
#         if max_offset <= 0:
#             topic_partition.offset = OFFSET_BEGINNING

#         else:
#             desired_offset = max_offset - KAFKA_MAX_HISTORY_DEPTH_ROLLBACK
#             if desired_offset <= min_offset:
#                 desired_offset = OFFSET_BEGINNING
#             topic_partition.offset = desired_offset
#             consumer.assign([topic_partition])


def main():
    # CONSUMER.subscribe([TOPIC], on_assign=kafka_on_assign_callback_rollback)
    CONSUMER.subscribe([TOPIC])

    while True:
        msg = CONSUMER.poll(1.0)  # Wait for a message up to 1 second

        if msg is None:
            continue

        if msg.error():
            print(msg.error())
        else:
            transaction = json.loads(msg.value().decode("utf-8"))
            process_transaction(transaction)


if __name__ == "__main__":
    main()
