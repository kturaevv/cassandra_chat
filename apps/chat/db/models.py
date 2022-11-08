from cassandra.cqlengine.models import Model
from cassandra.cqlengine.usertype import UserType
from cassandra.cqlengine import columns

from .config import get_settings
# IMPORTANT! cassandra driver supports up to python 3.8

# Note: Mapper inserts Null values, creates tombstones
# use .setDefaultSaveOption(saveNullFields(false))  to turn off
# or use .unset(null_column)

# Materialized Views (A proxy for additional partitions)
# STATIC data types associate a value to whole partition
settings = get_settings()

class message_info(UserType):
    """ Message information UDT. """
    reply_to    = columns.TimeUUID(default=None, required=False)
    user_id     = columns.BigInt()
    username    = columns.Text(min_length=1, max_length=32, required=False) # TODO remove?
    text        = columns.Text(min_length=1, max_length=4096, required=True)
    attachment  = columns.Text(max_length=4096, default=None, required=False) # metadata
    read_status = columns.Boolean(default=False)

# --- todo: separate UDTs later.

class Origin(Model):
    """ Global chat data (any user). 

    Q: Get N latest messages in chat.
    """
    __table_name__ = 'origin'
    __keyspace__    = settings.keyspace
    origin_id       = columns.Integer(partition_key=True, required=True)
    year            = columns.Integer(partition_key=True, required=True)
    month           = columns.Integer(partition_key=True, required=True)
    message_id      = columns.TimeUUID(primary_key=True, required=True, clustering_order="DESC")
    message         = columns.UserDefinedType(message_info)


class Private(Model):
    """ User 1 - 1 chat data. 
    
    Q: Gen N last messages in user-user chat.
    """
    __table_name__ = 'private'
    __keyspace__    = settings.keyspace
    origin_id       = columns.Integer(partition_key=True, required=True)
    user_id         = columns.BigInt(partition_key=True)
    chat_id         = columns.BigInt()
    message_id      = columns.TimeUUID(primary_key=True, required=True, clustering_order="DESC")
    message         = columns.UserDefinedType(message_info)
