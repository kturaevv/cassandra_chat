from tokenize import Triple

from cassandra.cluster import Cluster

from cassandra.cqlengine.models import Model
from cassandra.cqlengine.usertype import UserType
from cassandra.cqlengine import columns

from pydantic import UUID1

# IMPORTANT! cassandra driver supports up to python 3.8

# Note: Mapper inserts Null values, creates tombstones
# use .setDefaultSaveOption(saveNullFields(false))  to turn off
# or use .unset(null_column)

KEYSPACE = 'messages'


class basic_user_info(UserType):
    """ User information UDT. """
    user_id     = columns.UUID()
    username    = columns.Text(min_length=5, max_length=32, required=False)


class message_info(UserType):
    """ Message information UDT. """
    user        = columns.UserDefinedType(basic_user_info)
    text        = columns.Text(min_lenght=None, max_length=4096, required=True)
    reply_to    = columns.UUID()
    attachment  = columns.Text(min_length=1, max_length=4096) # metadata

# --- todo: separate UDTs later.

class GlobalChat(Model):
    """ Global chat data (any user). """
    __keyspace__ = KEYSPACE
    chat_id         = columns.UUID()
    date            = columns.Date(required=True)
    time            = columns.TimeUUID(required=True)
    msg_info        = columns.UserDefinedType(message_info)


class PrivateChat(Model):
    """ User 1 - 1 chat data. """
    __keyspace__ = KEYSPACE
    chat_id         = columns.UUID()
    date            = columns.Date(required=True)
    time            = columns.TimeUUID(required=True)
    msg_info        = columns.UserDefinedType(message_info)
    

class UserConversations(Model):
    """ User chats. """
    __keyspace__ = KEYSPACE
    user_id         = columns.UUID()
    chats           = columns.List(value_type=UUID1) # Note: collection types may lead to tombstone generation.
    

class ClientChats(Model):
    """ Client chats. """
    __keyspace__ = KEYSPACE
    client_id       = columns.UUID()
    chats           = columns.List(value_type=UUID1)
    

if __name__ == "__main__":
    cluster = Cluster(['0.0.0.0'],port=9042)
    session = cluster.connect(KEYSPACE)
    session.execute(f'USE {KEYSPACE}')

    