from fluvii.fluvii_app import FluviiTableApp
from .metrics import NubiumMetricsManager
import logging
from nubium_utils.general_utils import write_kubernetes_healthcheck_file, del_kubernetes_healthcheck_file


LOGGER = logging.getLogger(__name__)


class NubiumTableApp(FluviiTableApp):
    def _init_metrics_manager(self):
        if not self.metrics_manager:
            LOGGER.info('Initializing the Nubium MetricsManager')
            self.metrics_manager = NubiumMetricsManager(
                metrics_config=self._config.metrics_manager_config, pusher_config=self._config.metrics_pusher_config)

    def run(self):
        write_kubernetes_healthcheck_file()
        super().run()
        del_kubernetes_healthcheck_file()