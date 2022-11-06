from cassandra.cluster import Cluster
from cassandra import util
from cassandra.cqlengine import connection

from datetime import datetime, date
from faker import Faker

import random


def get_session(keyspace=None, address: str = 'localhost', port: int=9042):
    cluster = Cluster([address],port=port, protocol_version=3)
    session = cluster.connect(keyspace)
    connection.register_connection(str(session), session=session)
    connection.set_default_connection(str(session))
    return session


if __name__ == "__main__":
    import sys
    sys.path.append("../..")  # path lead to root dir to import module
    from apps.chat.db import models

    session = get_session(models.KEYSPACE)
    print("Cassandra is UP!")
    

    faker = Faker()

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

    models.Private.create(
        origin_id = random.randint(1, 10),
        user_id = random.randint(1, 10000),
        chat_id = random.randint(1, 10000),
        message_id = util.uuid_from_time(datetime.now()),
        message = models.message_info(**message)
    )