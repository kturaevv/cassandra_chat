""" Very simple test to check local setup. """

import pytest

from cassandra.cluster import Cluster
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.connection import register_connection, set_default_connection

from .check_cluster_conn import get_session

import sys
sys.path.append("../..")  # path lead to root dir to import module

from apps.chat.db import models


def init_database(session, keyspace):
    session.execute(f"DROP KEYSPACE IF EXISTS {keyspace}")
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS %s 
        WITH REPLICATION = { 'class': 'SimpleStrategy', 'replication_factor':1 }
        """ % keyspace)
    session.execute(f"USE {keyspace}")

    register_connection(str(session), session=session)
    set_default_connection(str(session))

    # apply ORM models to CQL - sync
    sync_table(models.GlobalChat)
    sync_table(models.PrivateChat)


@pytest.fixture(scope='session', autouse=True)
def session():
    """ Fixture to init and teardown Cassandra DB. """
    session = get_session(models.KEYSPACE)
    print("Initializing Cassandra.")
    init_database(session, models.KEYSPACE)
    yield session
    

def test_connection(session):
    assert not session.is_shutdown
