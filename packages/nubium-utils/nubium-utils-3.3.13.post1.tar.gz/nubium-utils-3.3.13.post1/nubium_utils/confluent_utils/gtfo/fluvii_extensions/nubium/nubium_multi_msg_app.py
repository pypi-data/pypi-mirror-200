from fluvii.fluvii_app import FluviiMultiMessageApp
from .metrics import NubiumMetricsManager
from .nubium_app import NubiumTransaction
from nubium_utils.general_utils import write_kubernetes_healthcheck_file, del_kubernetes_healthcheck_file
import logging


LOGGER = logging.getLogger(__name__)


class NubiumMultiMsgApp(FluviiMultiMessageApp):
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
