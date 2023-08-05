from .gtfo_app import GtfoApp
from nubium_utils.confluent_utils.confluent_runtime_vars import env_vars
from .fluvii_extensions.nubium import NubiumTableApp
from fluvii.transaction import TableTransaction


class GtfoTableApp(GtfoApp):
    def __init__(self, app_function, consume_topic, **kwargs):
        super().__init__(app_function, [consume_topic], **kwargs)

    def _get_config(self, topics):
        config = super()._get_config(topics)
        config.table_folder_path = env_vars()['NU_TABLE_PATH']
        return config

    def _get_app(self, *args, **kwargs):
        if not kwargs.get('transaction_cls'):
            kwargs['transaction_cls'] = TableTransaction
        return NubiumTableApp(*args, fluvii_config=self._config, **kwargs)
