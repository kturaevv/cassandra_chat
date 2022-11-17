from functools import lru_cache
from cassandra.cluster import Session
from datetime import date

from .. import schema

from .manager import ConnManager

# TODO: add logger


class CRUD:
    """ There should be only 1 instance allowed, thus Singleton is used. """
    
    query_insert_origin = """INSERT INTO origin (
            origin_id, year, month, message_id, message)
            VALUES (?, ?, ?, now(), ?)"""

    query_insert_private = """INSERT INTO private (
            origin_id, user_id, chat_id, message_id, message) 
            VALUES (?, ?, ?, now(), ?)"""

    def __init__(self) -> None:
        self.session: Session = ConnManager().session
        self.statement_insert_origin = None
        self.statement_insert_private = None
        self._prep_statements()

    def _prep_statements(self):
        self.statement_insert_origin = self.session.prepare(self.query_insert_origin)
        self.statement_insert_private= self.session.prepare(self.query_insert_private)

    def insert_async_origin(self, params: schema.MessageOrigin):
        """ Returns session execution future. Call .result() to get result (blocking). """
        future = self.session.execute_async(
            self.statement_insert_origin, 
            [params.origin_id, params.year, params.month, params.message]
        )
        future.add_callbacks(
            callback=self.__query_on_success,
            errback=self.__query_on_failure
            )
        return future

    def insert_async_private(self, params: schema.MessagePrivate):
        """ Returns session execution future. Call .result() to get result (blocking). """
        future = self.session.execute_async(
            self.statement_insert_private, 
            [params.origin_id, params.user_id, params.chat_id, params.message]
        )
        future.add_callbacks(
            callback=self.__query_on_success,
            errback=self.__query_on_failure
            )
        return future

    def __query_on_success(self):
        ...

    def __query_on_failure(self):
        ...

    def paging(self):
        # future = session.execute_async("SELECT * FROM origin LIMIT 50;")
        # future.add_callback(print_row_count, 'Async')
        # future.add_errback(print_err)

        # # Call this once so that the future has_more_pages value is set
        # future_res = future.result()
        # while future.has_more_pages:
        #     future.start_fetching_next_page()
        #     future_res = future.result()
        ...
