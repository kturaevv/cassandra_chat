from cassandra import util
from cassandra.concurrent import execute_concurrent_with_args

from datetime import datetime, date
from faker import Faker

import multiprocessing
import random

from app.db import models

from app.db.manager import ConnManager

import itertools

faker = Faker()

def orm_populate(n = None):
    for i in range(n):
        message = {
            "user_id" : i,
            "username" : faker.user_name(),
            "text" : f'{datetime.now()}',
        }
        
        models.Origin.create(
            origin_id=random.randint(1,10), 
            year='2022',
            month=11,
            message_id=util.uuid_from_time(datetime.now()),
            message = models.message_info_udt(**message)
        )

        models.Private.create(
            origin_id = random.randint(1, 10),
            user_id = random.randint(1, 10000),
            chat_id = random.randint(1, 10000),
            message_id = util.uuid_from_time(datetime.now()),
            message = models.message_info_udt(**message)
        )

def h(*args):
    import time
    print(*args)
    time.sleep(5)

class QueryManager:
    
    prepared = None
    concurrency = 100
    batch_size = 10

    def __init__(self, process_count):
        self.pool = multiprocessing.Pool(
            processes=process_count,
            initializer=self._setup
        )

    @classmethod
    def _setup(cls):
        cls.session = ConnManager().session
        cls.prepared = cls.session.prepare(cls.prepared)

    @classmethod
    def _execute_request(cls, params):
        print(params)
        return cls.session.execute(cls.prepared, params)

    @classmethod
    def _execute_concurrent(cls, params):
        print("A batch of ", len(params), " inserted")
        return [list(results[1]) for results in execute_concurrent_with_args(cls.session, cls.prepared, params)]

    def close_pool(self):
        self.pool.close()
        self.pool.join()
    
    def get_results(self, params):
        results = self.pool.imap(self._execute_request, params, self.batch_size)
        return results

    def get_concurrent_results(self, params):
        params = list(params)
        results = self.pool.imap(
            self._execute_concurrent,
            (params[n:n+self.concurrency] for n in range(0, len(params), self.concurrency))
        )
        return list(itertools.chain(*results))
    
    @staticmethod
    def fake_origin_data():
        return [
            random.randint(1,10), 
            2022, 
            11, 
            models.message_info_udt(**QueryManager.fake_message_udt_data())]

    @staticmethod
    def fake_private_data():
        return [
            random.randint(1,10), 
            random.randint(1, 10000), 
            random.randint(1, 10000), 
            models.message_info_udt(**QueryManager.fake_message_udt_data())]

    @staticmethod        
    def fake_message_udt_data(i = None):
        i = random.randint(0, 1000) if i is None else i

        message = {
                "user_id" : i,
                "username" : faker.name(),
                "text" : f"{datetime.now()}",
        }
        return message

class InsertOrigin(QueryManager):

    prepared = """INSERT INTO origin (
            origin_id, year, month, message_id, message)
            VALUES (?, ?, ?, now(), ?)"""

class InsertPrivate(QueryManager):

    prepared = """INSERT INTO private (
            origin_id, user_id, chat_id, message_id, message) 
            VALUES (?, ?, ?, now(), ?)"""


if __name__ == "__main__":
    PROCESSES = multiprocessing.cpu_count() - 1

    params = QueryManager.fake_private_data()
    
    p = InsertPrivate(process_count=PROCESSES)

    p.get_concurrent_results(params)
    p.close_pool()