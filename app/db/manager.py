""" Cassandra connection manager class. """

from cassandra.cqlengine import connection
from cassandra.cluster import Cluster
from cassandra.policies import DCAwareRoundRobinPolicy
from cassandra.cqlengine.management import sync_table

from .utils import SingletonMeta

from . import config, models


settings = config.get_settings()


class ConnManager(metaclass=SingletonMeta):
    """ Cassandra connection management class. """

    def __init__(self, keyspace = settings.keyspace) -> None:
        self.cluster = None
        self.session = None
        
        try:
            self._connect(keyspace)
        except:
            self.create_keyspace()

    def _connect(self, keyspace = None):
        self.cluster = Cluster(
            [settings.address], 
            port=settings.port, 
            protocol_version=3, 
            load_balancing_policy=DCAwareRoundRobinPolicy()
        )
        self.session = self.cluster.connect(keyspace)
        connection.register_connection(str(self.session), session=self.session)
        connection.set_default_connection(str(self.session))

    def create_keyspace(self):
        self._connect()
        self.session.execute("""
        CREATE KEYSPACE IF NOT EXISTS %s 
        WITH REPLICATION = { 'class': 'SimpleStrategy', 'replication_factor':1 }
        """ % settings.keyspace)
        self.session.execute(f"USE {settings.keyspace}")

        # apply ORM models to CQL - sync
        sync_table(models.Origin)
        sync_table(models.Private)

    def drop_keyspace(self):
        self.session.execute("""DROP KEYSPACE IF EXISTS %s""" % settings.keyspace)
