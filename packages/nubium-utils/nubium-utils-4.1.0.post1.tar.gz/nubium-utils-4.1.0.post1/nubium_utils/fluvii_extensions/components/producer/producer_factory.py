from fluvii.components.producer import ProducerFactory
from nubium_utils.fluvii_extensions.components.metrics import NubiumMetricsManager
from .config import NubiumProducerConfig


class NubiumProducerFactory(ProducerFactory):
    metrics_cls = NubiumMetricsManager
    producer_config_cls = NubiumProducerConfig
