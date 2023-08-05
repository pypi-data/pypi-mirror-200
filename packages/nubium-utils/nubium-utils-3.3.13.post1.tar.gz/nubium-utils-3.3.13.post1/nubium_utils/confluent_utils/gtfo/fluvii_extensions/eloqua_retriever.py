from .nubium import NubiumTableApp
from fluvii.exceptions import FinishedTransactionBatch, PartitionsAssigned
from fluvii.transaction import TableTransaction
import logging
from nubium_utils.general_utils import write_kubernetes_healthcheck_file, del_kubernetes_healthcheck_file


LOGGER = logging.getLogger(__name__)


class EloquaRetrieverTransaction(TableTransaction):
    """
    Necessary because we aren't usually consuming a message while producing table messages. We can mock out what
    we would need from a message by returning static values for the necessary items called.
    """
    def key(self):
        return 'timestamp'

    def headers(self):
        try:
            return super().headers()
        except Exception:
            return {'guid': 'none', 'last_updated_by': 'self'}

    def partition(self):
        return 0


class NubiumEloquaRetrieverApp(NubiumTableApp):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, transaction_cls=EloquaRetrieverTransaction)

    def _set_config(self):
        super()._set_config()
        self._config.consumer_config.poll_timeout_seconds = 5
        self._config.consumer_config.batch_consume_max_time_seconds = 4

    def _handle_message(self, **kwargs):
        self.consume(**kwargs)
        timestamp = self.transaction.value()['timestamp']
        LOGGER.info(f'External timestamp update received: {timestamp} UTC')
        self.transaction.update_table_entry(timestamp)

    def _no_message_callback(self):
        self._producer.poll(0)
        self._app_function(self.transaction, *self._app_function_arglist)
        self._finalize_app_batch()
        self.commit_tables()

    def _run(self, **kwargs):
        self._init_transaction_handler()
        assignments = self._consumer.assignment()
        while len(assignments) != 2:
            try:
                self.consume(**kwargs)
            except FinishedTransactionBatch:
                self._producer.poll(0)
                LOGGER.info('Waiting on rebalance to complete...')
            except PartitionsAssigned:
                self._handle_rebalance()
            finally:
                assignments = self._consumer.assignment()
        super()._run(**kwargs)

    def run(self):
        write_kubernetes_healthcheck_file()
        super().run()
        del_kubernetes_healthcheck_file()
