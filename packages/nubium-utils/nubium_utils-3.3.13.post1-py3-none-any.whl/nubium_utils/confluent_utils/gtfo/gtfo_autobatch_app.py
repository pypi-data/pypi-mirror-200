from .gtfo_app import GtfoApp
from nubium_utils.confluent_utils.confluent_runtime_vars import env_vars


class GtfoAutoBatchApp(GtfoApp):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._app._config.consumer_config.batch_consume_max_count = int(env_vars()['NU_CONSUMER_DEFAULT_BATCH_CONSUME_MAX_COUNT'])
        self._app._config.consumer_config.batch_consume_max_time_seconds = int(env_vars()['NU_CONSUMER_DEFAULT_BATCH_CONSUME_MAX_TIME_SECONDS'])
