from .nubium import NubiumMultiMsgApp
from os import environ


class NubiumRestBulkSwitcher(NubiumMultiMsgApp):
    def _set_config(self):
        super()._set_config()
        self._config.consumer_config.batch_consume_trigger_message_age_seconds = int(environ.get('NU_RESTBULK_TRIGGER_MESSAGE_AGE_SECONDS', '60'))
        self._config.consumer_config.batch_consume_max_count = 0
        self._config.consumer_config.batch_consume_max_time_seconds = 120
