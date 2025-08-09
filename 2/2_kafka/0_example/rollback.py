from confluent_kafka import OFFSET_BEGINNING

KAFKA_MAX_HISTORY_DEPTH_ROLLBACK = 5


def kafka_on_assign_callback_rollback(consumer, topic_partitions) -> None:
    for topic_partition in topic_partitions:
        min_offset, max_offset = consumer.get_watermark_offsets(
            topic_partition, cached=False
        )
        if max_offset <= 0:
            topic_partition.offset = OFFSET_BEGINNING

        else:
            desired_offset = max_offset - KAFKA_MAX_HISTORY_DEPTH_ROLLBACK
            if desired_offset <= min_offset:
                desired_offset = OFFSET_BEGINNING
            topic_partition.offset = desired_offset
            consumer.assign([topic_partition])
