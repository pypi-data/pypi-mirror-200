from fluvii.exceptions import FinishedTransactionBatch, PartitionsAssigned, SignalRaise
from fluvii.fluvii_app.fluvii_table_app import TableTransaction
from .nubium import NubiumTableApp
import logging
from os import environ
from time import sleep

LOGGER = logging.getLogger(__name__)


class SalesforceRetrieverTransaction(TableTransaction):
    """
    Necessary because we aren't usually consuming a message while producing table messages. We can mock out what
    that message is.
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


class NubiumSalesforceRetrieverApp(NubiumTableApp):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, transaction_cls=SalesforceRetrieverTransaction)

    def _handle_message(self):
        self._producer.poll(0)
        self._app_function(self.transaction, *self._app_function_arglist)  # this app doesn't loop, its a one time call
        self._shutdown = True
        LOGGER.info('stopping event loop...')
        self.transaction.event_loop.stop()

    def _app_shutdown(self):
        super()._app_shutdown()
        sleep_time = int(environ.get('NU_SALESFORCE_RETRIEVER_SHUTDOWN_SLEEP_SECONDS', '90'))
        try:
            LOGGER.info(f'Sleeping for up to {sleep_time}s to allow rebalance to finish by keeping this app alive. '
                        f'This can be interrupted safely via termination signal or keyboard interrupt.')
            sleep(sleep_time)
        except SignalRaise:
            LOGGER.info('Sleep interrupted gracefully!')
        LOGGER.info('Sleep finished.')

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
