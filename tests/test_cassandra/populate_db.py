from cassandra import util
from datetime import datetime, date
from faker import Faker

import random

faker = Faker()

def populate_test_database():
    for i in range(1000):
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
        if i % 100 == 0: print("100 items created...")

        
if __name__ == "__main__":
    import sys
    sys.path.append("../..")  # path lead to root dir to import module
    from apps.chat.db import models

    from check_connection import get_session

    session = get_session()
    populate_test_database()