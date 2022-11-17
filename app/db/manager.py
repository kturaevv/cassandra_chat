""" Cassandra connection manager class. """

from cassandra.cqlengine import connection
from cassandra.cluster import Cluster
from cassandra.policies import DCAwareRoundRobinPolicy

from .utils import SingletonMeta

from . import config

settings = config.get_settings()


class ConnManager(metaclass=SingletonMeta):
    """ Cassandra connection management class. """

    def __init__(self) -> None:
        self.cluster = Cluster(
            [settings.address], 
            port=settings.port, 
            protocol_version=3, 
            load_balancing_policy=DCAwareRoundRobinPolicy()
        )
        self.session = self.cluster.connect(settings.keyspace)
        connection.register_connection(str(self.session), session=self.session)
        connection.set_default_connection(str(self.session))
