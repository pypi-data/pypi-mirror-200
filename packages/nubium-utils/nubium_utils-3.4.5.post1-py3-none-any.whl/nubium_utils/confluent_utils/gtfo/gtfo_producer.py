from fluvii.auth import SaslOauthClientConfig
from fluvii.producer import Producer
from fluvii.schema_registry import SchemaRegistry
from nubium_utils.confluent_utils.confluent_runtime_vars import env_vars
from nubium_utils.yaml_parser import load_yaml_fp
from os import environ


def gtfo_producer(topic_schema_dict):
    cluster_config = load_yaml_fp(env_vars()['NU_KAFKA_CLUSTERS_CONFIGS_YAML'])[load_yaml_fp(env_vars()['NU_TOPIC_CONFIGS_YAML'])[list(topic_schema_dict.keys())[0]]['cluster']]
    auth = SaslOauthClientConfig(
        cluster_config['username'],
        cluster_config['password'],
        environ['FLUVII_OAUTH_URL'],
        environ['FLUVII_OAUTH_SCOPE'],
    )

    return Producer(
        cluster_config['url'],
        schema_registry=SchemaRegistry(env_vars()['NU_SCHEMA_REGISTRY_URL'], auth_config=auth),
        client_auth_config=auth,
        topic_schema_dict=topic_schema_dict,
    )
