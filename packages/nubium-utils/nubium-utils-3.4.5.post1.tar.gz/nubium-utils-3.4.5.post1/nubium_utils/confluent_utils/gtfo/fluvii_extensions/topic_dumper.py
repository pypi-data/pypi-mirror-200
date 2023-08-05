from fluvii.fluvii_app import FluviiMultiMessageApp
from confluent_kafka import TopicPartition
import logging
from time import sleep

LOGGER = logging.getLogger(__name__)


class NubiumTopicDumperApp(FluviiMultiMessageApp):
    """Note: this should just be converted to a regular consumer, but I already had most of the code so whatever. """
    def __init__(self, consume_topics_list, app_function=None, **kwargs):
        super().__init__(app_function, consume_topics_list, **kwargs)
        self._consumer_offset_dict = None

    def _set_config(self):
        super()._set_config()
        self._config.consumer_config.batch_consume_max_count = None
        self._config.consumer_config.batch_consume_max_time_seconds = None

    def _init_metrics_manager(self):
        pass

    def _get_partition_assignment(self):
        LOGGER.debug('Getting partition assignments...')
        self._consumer.poll(5)
        partitions = self._consumer.assignment()  # Note: this actually can change in-place as partitions get assigned in the background!
        assign_count_prev = 0
        checks = 2
        while checks:
            assign_count_current = len(partitions)
            if (assign_count_current > assign_count_prev) or assign_count_current == 0:
                assign_count_prev = assign_count_current
            else:
                checks -= 1
            sleep(1)
        LOGGER.debug(f'All partition assignments retrieved: {partitions}')
        return partitions

    def _seek_consumer_to_offsets(self, consumer_offset_dict=None):
        LOGGER.info('Setting up consumer to pull from the beginning of the topics...')
        partitions = self._get_partition_assignment()
        if not consumer_offset_dict:
            consumer_offset_dict = {}
        for partition in partitions:
            p = partition.partition
            topic = partition.topic
            if topic not in consumer_offset_dict:
                consumer_offset_dict[topic] = {}
            if p not in consumer_offset_dict[topic]:
                consumer_offset_dict[topic][p] = self._consumer.get_watermark_offsets(partition)[0]
        for topic, partitions in consumer_offset_dict.items():
            for p, offset in partitions.items():
                LOGGER.debug(f'Seeking {topic} p{p} to offset {offset}')
                self._consumer.seek(TopicPartition(topic=topic, partition=p, offset=offset))

    def _finalize_app_batch(self):
        if self._app_function:
            LOGGER.info('Transforming all messages to desired format...')
            self._consumer._messages = self._app_function(self.transaction, *self._app_function_arglist)
        raise Exception('Got all messages!')

    def _app_shutdown(self):
        LOGGER.info('App is shutting down...')
        self._shutdown = True
        self.kafka_cleanup()

    def _runtime_init(self):
        super()._runtime_init()
        self._seek_consumer_to_offsets(consumer_offset_dict=self._consumer_offset_dict)

    def run(self, consumer_offset_dict=None, **kwargs):
        self._consumer_offset_dict = consumer_offset_dict
        try:
            super().run(**kwargs)
        finally:
            return self.transaction.messages()
