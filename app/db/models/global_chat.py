from cassandra.cqlengine.models import Model
from cassandra.cqlengine.usertype import UserType
from cassandra.cqlengine import columns

# IMPORTANT! cassandra driver supports up to python 3.8

# Note: Mapper inserts Null values, creates tombstones
# use .setDefaultSaveOption(saveNullFields(false))  to turn off
# or use .unset(null_column)

# Materialized Views (A proxy for additional partitions)
# STATIC data types associate a value to whole partition


KEYSPACE = 'messages'


class basic_user_info(UserType):
    """ User information UDT. """
    user_id     = columns.UUID()
    username    = columns.Text(min_length=5, max_length=32, required=False)


class message_info(UserType):
    """ Message information UDT. """
    user        = columns.UserDefinedType(basic_user_info)
    text        = columns.Text(min_length=None, max_length=4096, required=True)
    reply_to    = columns.UUID()
    attachment  = columns.Text(min_length=1, max_length=4096) # metadata
    read_status = columns.Boolean()

# --- todo: separate UDTs later.

class GlobalChat(Model):
    """ Global chat data (any user). 

    Q: Get N latest messages in chat.
    """
    __keyspace__ = KEYSPACE
    origin_id         = columns.UUID(partition_key=True)
    date            = columns.Date(partition_key=True, required=True)
    time            = columns.TimeUUID(primary_key=True, clustering_order="DESC", required=True)
    msg_info        = columns.UserDefinedType(message_info)


class PrivateChat(Model):
    """ User 1 - 1 chat data. 
    
    Q: Gen N last messages in user-user chat.
    """
    __keyspace__ = KEYSPACE
    user_id         = columns.UUID(partition_key=True)
    chat_id         = columns.UUID(partition_key=True)
    origin_id       = columns.UUID(required=True)
    time            = columns.TimeUUID(primary_key=True, required=True, clustering_order="DESC")
    date            = columns.Date(required=True)
    msg_info        = columns.UserDefinedType(message_info)
