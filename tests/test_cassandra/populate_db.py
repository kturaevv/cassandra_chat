from cassandra import util
from datetime import datetime, date
from faker import Faker

import random

faker = Faker()

def orm_populate():
    for i in range(1000):
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

def cql_populate(session):
    origin_ = session.prepare("""INSERT INTO origin (
            origin_id, year, month, message_id, message)
            VALUES (?, ?, ?, now(), ?)""")
    
    private_ = session.prepare("""INSERT INTO private (
            origin_id, user_id, chat_id, message_id, message) 
            VALUES (?, ?, ?, now(), ?)""")

    
    for i in range(100000):
        message = {
            "user_id" : i,
            "username" : 'jon',
            "text" : f"{datetime.now()}",
        }

        session.execute_async(origin_, [random.randint(1,10), 2022, 11, models.message_info_udt(**message)])
        session.execute_async(private_, [random.randint(1,10),random.randint(1, 10000),random.randint(1, 10000), models.message_info_udt(**message)])
        if i % 100 == 0: print("100 items inserted...")
        

def cql_concurrent_populate(session):
    from cassandra.concurrent import execute_concurrent_with_args
    
    def message(i):
        message = {
                "user_id" : i,
                "username" : 'jon',
                "text" : f"{datetime.now()}",
        }
        return message

    origin_ = session.prepare("""INSERT INTO origin (
            origin_id, year, month, message_id, message)
            VALUES (?, ?, ?, now(), ?)""")

    params = [[random.randint(1,10), 2022, 11, models.message_info_udt(**message(i))] for i in range(100000)]

    execute_concurrent_with_args(session, origin_, params, concurrency=100)


if __name__ == "__main__":
    from app.db import models
    from app.db.manager import ConnManager

    session = ConnManager().session
    cql_concurrent_populate(session)