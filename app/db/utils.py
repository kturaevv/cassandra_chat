from cassandra import util
from cassandra.cluster import Cluster
from cassandra.query import dict_factory
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table

from datetime import datetime, date

from app.db import models


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


def get_cassandra_session(keyspace=None, address: str = 'localhost', port: int=9042):
    cluster = Cluster([address],port=port, protocol_version=3)
    session = cluster.connect(keyspace)
    connection.register_connection(str(session), session=session)
    connection.set_default_connection(str(session))
    return session

def init_database(session, keyspace):
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS %s 
        WITH REPLICATION = { 'class': 'SimpleStrategy', 'replication_factor':1 }
        """ % keyspace)
    session.execute(f"USE {keyspace}")

    # apply ORM models to CQL - sync
    sync_table(models.Origin)
    sync_table(models.Private)