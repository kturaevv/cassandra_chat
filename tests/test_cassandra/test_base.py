""" Very simple test to check local setup. """

import pytest
from test_model import KEYSPACE
from cassandra.cluster import Cluster


@pytest.fixture(scope='session', autouse=True)
def init_db():
    """ Fixture to init and teardown Cassandra DB. """

    cluster = Cluster(['0.0.0.0'],port=9042)
    session = cluster.connect(KEYSPACE)
    session.execute(f'USE {KEYSPACE}')
    
    yield 1


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
