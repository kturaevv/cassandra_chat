""" Very simple test to check local setup. """

import pytest

from cassandra.cluster import Cluster
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.connection import register_connection, set_default_connection

from .check_cluster_conn import get_session

import sys
sys.path.append("../..")  # path lead to root dir to import module

from app.db.models import global_chat


def init_database(session, keyspace):
    session.execute("""CREATE KEYSPACE IF NOT EXISTS messages WITH REPLICATION = { 'class': 'SimpleStrategy', 'replication_factor':1 }""")
    session.set_keyspace(keyspace)

    register_connection(str(session), session=session)
    set_default_connection(str(session))

    # apply ORM models to CQL - sync
    sync_table(global_chat.GlobalChat)
    sync_table(global_chat.PrivateChat)
    sync_table(global_chat.ClientChats)
    sync_table(global_chat.UserConversations)


@pytest.fixture(scope='session', autouse=True)
def session():
    """ Fixture to init and teardown Cassandra DB. """
    session = get_session()

    print("INITING DB")
    init_database(session, global_chat.KEYSPACE)
    
    yield session
    

def test_connection():
    assert 1

def test_create():
    assert 1

def test_read():
    assert 1

def test_update():
    assert 1

def test_delete():
    assert 1
