from cassandra.cluster import Cluster
from cassandra import util
from cassandra.cqlengine import connection
from cassandra.query import dict_factory

from datetime import datetime, date
from faker import Faker

import random

from apps.chat.db import config, models

faker = Faker()


def get_session(keyspace=None, address: str = 'localhost', port: int=9042):
    cluster = Cluster([address],port=port, protocol_version=3)
    session = cluster.connect(keyspace)
    connection.register_connection(str(session), session=session)
    connection.set_default_connection(str(session))
    return session


if __name__ == "__main__":
    settings = config.get_settings()

    address = settings.address.split(':')
    
    session = get_session(settings.keyspace, address=address[0], port=address[1])
    session.row_factory = dict_factory

    print("Cassandra is UP!")

    message = {
        "user_id" : random.randint(1, 10000),
        "username" : faker.user_name(),
        "text" : faker.text(),
    }
    
    models.Origin.create(
        origin_id=random.randint(1,10), 
        date=date.today(),
        message_id=util.uuid_from_time(datetime.now()),
        message = models.message_info(**message)
    )

    models.Origin.create(
        origin_id=random.randint(1,10), 
        date=date.today(),
        message_id=util.uuid_from_time(datetime.now()),
        message = models.message_info(**message)
    )

    obj = models.Private.create(
        origin_id = random.randint(1, 10),
        user_id = random.randint(1, 10000),
        chat_id = random.randint(1, 10000),
        message_id = util.uuid_from_time(datetime.now()),
        message = models.message_info(**message)
    )
    
    assert models.Private(user_id=obj.user_id)    
    
    query = models.Origin.all().limit(5)
    
    print(type(query))

    for i in query:
        print(i)

    print(session.execute("select * from origin limit 1")[0])

    print("Connection is OK")
    session.shutdown()