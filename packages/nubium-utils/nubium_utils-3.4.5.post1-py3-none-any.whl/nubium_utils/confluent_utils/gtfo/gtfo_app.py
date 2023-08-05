from fluvii.fluvii_app import FluviiConfig
from fluvii.auth import SaslOauthClientConfig
from .fluvii_extensions.nubium import NubiumTransaction, NubiumApp
from nubium_utils.confluent_utils.confluent_runtime_vars import env_vars
from nubium_utils.yaml_parser import load_yaml_fp
from os import environ


class GtfoApp:
    def __init__(self, app_function, consume_topics_list, produce_topic_schema_dict=None, **kwargs):
        self._produce_dict = produce_topic_schema_dict
        self._config = self._get_config(consume_topics_list)
        self._app = self._get_app(app_function, consume_topics_list, produce_topic_schema_dict=produce_topic_schema_dict, **kwargs)

    def _get_cluster_name(self, consume_topics_list):
        topic = consume_topics_list[0] if isinstance(consume_topics_list, list) else consume_topics_list
        return load_yaml_fp(env_vars()['NU_TOPIC_CONFIGS_YAML'])[topic]['cluster']

    def _get_config(self, topics):
        cluster_config = load_yaml_fp(env_vars()['NU_KAFKA_CLUSTERS_CONFIGS_YAML'])[self._get_cluster_name(topics if topics else list(self._produce_dict.keys()))]
        auth = SaslOauthClientConfig(
            cluster_config['username'],
            cluster_config['password'],
            environ['FLUVII_OAUTH_URL'],
            environ['FLUVII_OAUTH_SCOPE']
            )
        config = FluviiConfig(
            client_urls=cluster_config['url'],
            client_auth_config=auth,
            schema_registry_url=env_vars()['NU_SCHEMA_REGISTRY_URL'],
            schema_registry_auth_config=auth,
        )
        config.app_name = env_vars()['NU_APP_NAME']
        config.hostname = env_vars()['NU_HOSTNAME']

        config.consumer_config.batch_consume_max_count = 1
        config.consumer_config.timeout_minutes = int(env_vars()['NU_CONSUMER_TIMEOUT_LIMIT_MINUTES']) + int(env_vars()['NU_CONSUMER_TIMESTAMP_OFFSET_MINUTES'])
        config.consumer_config.heartbeat_timeout_ms = int(env_vars()['NU_CONSUMER_HEARTBEAT_TIMEOUT_SECONDS']) * 1000
        config.consumer_config.auto_offset_reset = env_vars()['NU_CONSUMER_AUTO_OFFSET_RESET']

        config.metrics_manager_config.app_name = config.app_name
        config.metrics_manager_config.hostname = config.hostname

        enable_pushing = env_vars()['NU_DO_METRICS_PUSHING']
        if enable_pushing.lower() == 'true':
            enable_pushing = True
        else:
            enable_pushing = False
        config.metrics_pusher_config.enable_pushing = enable_pushing
        config.metrics_pusher_config.push_rate_seconds = int(env_vars()['NU_METRICS_PUSH_RATE'])
        config.metrics_pusher_config.headless_service_name = env_vars()['NU_METRICS_SERVICE_NAME']
        config.metrics_pusher_config.headless_service_port = env_vars()['NU_METRICS_SERVICE_PORT']
        config.metrics_pusher_config.metrics_port = env_vars()['NU_METRICS_POD_PORT']

        return config

    def _get_app(self, *args, **kwargs):
        t_cls = kwargs.pop('transaction_cls', NubiumTransaction)
        return NubiumApp(*args, fluvii_config=self._config, transaction_cls=t_cls, **kwargs)

    def run(self):
        self._app.run()
