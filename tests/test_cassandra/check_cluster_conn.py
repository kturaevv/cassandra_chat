from tokenize import Triple
from uuid import uuid1
from cassandra.cluster import Cluster


def get_session(keyspace = None, address: str = 'localhost', port: int=9042):
    cluster = Cluster([address],port=port, protocol_version=3)
    session = cluster.connect(keyspace)
    return session


if __name__ == "__main__":

    import sys
    sys.path.append("../..")  # path lead to root dir to import module
    from app.db.models import global_chat

    session = get_session(global_chat.KEYSPACE)
    assert not session.is_shutdown
    print("Cassandra is UP!")
