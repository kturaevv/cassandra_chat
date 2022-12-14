""" Very simple test to check local setup. """

import sys, random, pytest
sys.path.append("../..")  # path lead to root dir to import module

from app.db import models, config
from app.db.manager import ConnManager

from datetime import datetime
from faker import Faker

from cassandra import util

faker = Faker()

settings = config.get_settings()

@pytest.fixture(scope='session', autouse=True)
def session():
    """ Fixture to init and teardown Cassandra DB. """
    session = ConnManager().session
    ConnManager().create_keyspace()
    yield session
    session.shutdown()

def test_connection(session):
    assert not session.is_shutdown

def test_db():
    message = {
        "user_id" : random.randint(1, 10000),
        "username" : faker.user_name(),
        "text" : faker.text(),
    }

    obj = models.Private.create(
        origin_id = random.randint(1, 10),
        user_id = random.randint(1, 10000),
        chat_id = random.randint(1, 10000),
        message_id = util.uuid_from_time(datetime.now()),
        message = models.message_info_udt(**message)
    )
    
    assert models.Private(user_id=obj.user_id)    