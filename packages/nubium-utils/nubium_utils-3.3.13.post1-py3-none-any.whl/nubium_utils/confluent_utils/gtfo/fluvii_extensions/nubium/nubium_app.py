from fluvii.fluvii_app import FluviiApp
from fluvii.transaction import Transaction
from .metrics import NubiumMetricsManager
from nubium_utils.confluent_utils.confluent_runtime_vars import env_vars
from nubium_utils.custom_exceptions import RetryTopicSend, FailureTopicSend, MaxRetriesReached
from nubium_utils.general_utils import write_kubernetes_healthcheck_file, del_kubernetes_healthcheck_file
import logging
import json
import datetime
from time import sleep


LOGGER = logging.getLogger(__name__)


class NubiumTransaction(Transaction):
    def _wait_until_message_time(self):
        """
        Wait until the message's timestamp + the deployments offset before handling
        """
        if wait_minutes := int(env_vars()['NU_CONSUMER_TIMESTAMP_OFFSET_MINUTES']):
            message_process_time = (self.message.timestamp()[1] // 1000) + (wait_minutes * 60)
            wait_time = message_process_time - datetime.datetime.timestamp(datetime.datetime.utcnow())
            if wait_time > 0:
                LOGGER.info(f'Waiting {wait_time} seconds before message processing continues; GUID {self.headers()["guid"]}')
                sleep(wait_time)
                return 'i sleep'
        return 'real shit'

    def consume(self, **kwargs):
        super().consume(**kwargs)
        self._wait_until_message_time()

    def produce_retry(self, exception=None):
        retry_topic = None
        headers = self.headers()
        guid = headers['guid']
        kafka_retry_count = int(headers.get('kafka_retry_count', '0'))

        if kafka_retry_count < int(env_vars()['NU_RETRY_COUNT_MAX']):
            headers['kafka_retry_count'] = str(kafka_retry_count + 1)
            retry_topic = env_vars()['NU_CONSUME_TOPICS']
        else:
            headers['kafka_retry_count'] = '0'
            retry_topic = env_vars().get('NU_PRODUCE_RETRY_TOPICS', '')

        if retry_topic:
            if not exception:
                exception = RetryTopicSend()
            LOGGER.warning('; '.join([str(exception), f'retrying GUID {guid}']))
            self.produce(dict(value=self.value(), topic=retry_topic, headers=headers))

        else:
            if not exception:
                exception = FailureTopicSend()
            LOGGER.error('; '.join([str(exception), f'GUID {guid}']))
            self.produce_failure(exception=MaxRetriesReached())

    def produce_failure(self, exception=None):
        headers = self.headers()
        guid = headers['guid']
        headers['kafka_retry_count'] = '0'
        failure_topic = env_vars()['NU_PRODUCE_FAILURE_TOPICS']

        if not exception:
            exception = FailureTopicSend()
        LOGGER.error('; '.join([type(exception).__name__, str(exception), f'failing GUID {guid}']))
        headers["exception"] = json.dumps({"name": type(exception).__name__, "description": str(exception)})

        LOGGER.debug(f'Adding a message to the produce queue for deadletter/failure topic {env_vars()["NU_PRODUCE_FAILURE_TOPICS"]}')
        self.produce(dict(value=self.value(), topic=failure_topic, headers=headers))
        LOGGER.info(f'Message added to the deadletter/failure topic produce queue; GUID {guid}')


class NubiumApp(FluviiApp):
    def __init__(self, *args, **kwargs):
        t_cls = kwargs.pop('transaction_cls', NubiumTransaction)
        super().__init__(*args, transaction_cls=t_cls, **kwargs)

    def _init_metrics_manager(self):
        if not self.metrics_manager:
            LOGGER.info('Initializing the Nubium MetricsManager')
            self.metrics_manager = NubiumMetricsManager(
                metrics_config=self._config.metrics_manager_config, pusher_config=self._config.metrics_pusher_config)

    def run(self):
        write_kubernetes_healthcheck_file()
        super().run()
        del_kubernetes_healthcheck_file()
