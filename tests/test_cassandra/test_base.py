""" Very simple test to check local setup. """

import pytest

from cassandra import util
from cassandra.cluster import Cluster
from cassandra.cqlengine.management import sync_table, sync_type
from cassandra.cqlengine import connection

from datetime import date

import sys
sys.path.append("../..")  # path lead to root dir to import module

from apps.chat.db import models, config

from .check_connection import get_session


settings = config.get_settings()

def init_database(session, keyspace):
    session.execute(f"DROP KEYSPACE IF EXISTS {keyspace}")
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS %s 
        WITH REPLICATION = { 'class': 'SimpleStrategy', 'replication_factor':1 }
        """ % keyspace)
    session.execute(f"USE {keyspace}")

    connection.register_connection(str(session), session=session)
    connection.set_default_connection(str(session))

    # apply ORM models to CQL - sync
    sync_table(models.Origin)
    sync_table(models.Private)


@pytest.fixture(scope='session', autouse=True)
def session():
    """ Fixture to init and teardown Cassandra DB. """
    session = get_session(settings.keyspace)
    init_database(session, settings.keyspace)
    yield session
    

def test_connection(session):
    assert not session.is_shutdown
