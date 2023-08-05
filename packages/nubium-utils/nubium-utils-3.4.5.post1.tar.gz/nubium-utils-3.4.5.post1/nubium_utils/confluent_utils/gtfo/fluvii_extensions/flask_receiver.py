import logging
from os import environ
from unittest import mock

from fluvii.fluvii_app import FluviiConfig
from fluvii.producer import Producer
from fluvii.schema_registry import SchemaRegistry
import threading
import time
from .nubium.metrics import NubiumMetricsManager

LOGGER = logging.getLogger(__name__)


def get_flask_fluvii_producer(fluvii_config, topic_schema_dict, metrics_manager):
    return Producer(
        urls=fluvii_config.client_urls,
        schema_registry=SchemaRegistry(
            url=fluvii_config.schema_registry_url, auth_config=fluvii_config.client_auth_config),
        client_auth_config=fluvii_config.client_auth_config,
        topic_schema_dict=topic_schema_dict,
        metrics_manager=metrics_manager
    )


class NubiumFlaskConfig:
    def __init__(self, producer=None, topic=None, schema=None, metrics_manager=None):
        self.LOGLEVEL = environ['LOGLEVEL']

        self.TOPIC = topic
        self.PRODUCER = producer
        self.SCHEMA = schema
        self.METRICS_MANAGER = metrics_manager

        if self.TOPIC is None:
            self.TOPIC = environ['OUTPUT_TOPIC']

        self.TOPIC_SCHEMA_DICT = {self.TOPIC: self.SCHEMA}

        fluvii_config = FluviiConfig()

        if not self.METRICS_MANAGER:
            self.METRICS_MANAGER = NubiumMetricsManager(
                metrics_config=fluvii_config.metrics_manager_config,
                pusher_config=fluvii_config.metrics_pusher_config)

        if self.PRODUCER is None:
            self.PRODUCER = get_flask_fluvii_producer(fluvii_config, self.TOPIC_SCHEMA_DICT, self.METRICS_MANAGER)

        self.PRODUCER_POLL_THREAD = threading.Thread(target=self._producer_poll_loop, daemon=True)
        self.PRODUCER_POLL_THREAD.start()

    def _producer_poll_loop(self):
        """So we dont get spammed with (harmless) re-auth errors"""
        while True:
            try:
                self.PRODUCER.poll(0)
            except:
                pass
            time.sleep(10)


class NubiumTestFlaskConfig:
    def __init__(self):
        self.TESTING = True
        self.LOGLEVEL = "DEBUG"
        self.TOPIC = mock.MagicMock()
        self.SCHEMA = mock.MagicMock()
        self.METRICS_MANAGER = mock.MagicMock()
        self.PRODUCER = mock.MagicMock()
