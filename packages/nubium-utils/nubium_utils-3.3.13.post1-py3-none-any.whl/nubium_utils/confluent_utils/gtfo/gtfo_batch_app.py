from .gtfo_app import GtfoApp, NubiumTransaction
from fluvii.fluvii_app import FluviiMultiMessageApp
from nubium_utils.confluent_utils.confluent_runtime_vars import env_vars
from nubium_utils.general_utils import write_kubernetes_healthcheck_file, del_kubernetes_healthcheck_file


class GtfoBatchApp(GtfoApp):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._app._config.consumer_config.batch_consume_max_count = int(env_vars()['NU_CONSUMER_DEFAULT_BATCH_CONSUME_MAX_COUNT'])
        self._app._config.consumer_config.batch_consume_max_time_seconds = int(env_vars()['NU_CONSUMER_DEFAULT_BATCH_CONSUME_MAX_TIME_SECONDS'])

    def _get_app(self, *args, **kwargs):
        t_cls = kwargs.pop('transaction_cls', NubiumTransaction)
        return FluviiMultiMessageApp(*args, fluvii_config=self._config, transaction_cls=t_cls, **kwargs)

    def run(self):
        write_kubernetes_healthcheck_file()
        super().run()
        del_kubernetes_healthcheck_file()
