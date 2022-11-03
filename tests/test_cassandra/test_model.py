from tokenize import Triple
from uuid import uuid1

from cassandra.cluster import Cluster

from cassandra.cqlengine.models import Model
from cassandra.cqlengine.usertype import UserType
from cassandra.cqlengine import columns
from cassandra.cqlengine.management import sync_table


# IMPORTANT! cassandra driver supports up to python 3.8

# Note: Mapper inserts Null values, creates tombstones
# use .setDefaultSaveOption(saveNullFields(false))  to turn off
# or use .unset(null_column)

KEYSPACE = 'messages'


class basic_user_info(UserType):
    """ User information UDT. 
    
    CREATE TYPE basic_user_info(
        id		    uuid,
        username	text
    );

    """
    user_id     = columns.UUID()
    username    = columns.Text(min_length=5, max_length=32, required=False)


class message_info(UserType):
    """ Message information UDT. 
    
    CREATE TYPE message_info(
        id		    uuid,
        user		frozen <basic_user_info>,
        text	 	text,
        reply_to	uuid,
        attachment	text,
    );

    """
    user        = columns.UserDefinedType(basic_user_info)
    text        = columns.Text(min_length=None, max_length=4096, required=True)
    reply_to    = columns.UUID()
    attachment  = columns.Text(min_length=1, max_length=4096) # metadata

# --- todo: separate UDTs later.

class GlobalChat(Model):
    """ Global chat data (any user). 

    Q: Get N latest messages in chat.

    This corresponds to following CQL:

    CREATE TABLE GlobalChat (
        chat_id		uuid,			# Partition	    | Search Nodes by this column
        date		text,			# Partition 	| Additional partition for each day
        timestamp 	datetime,		# Cluster 	    | Search info by this column, sorted gives N(1)
	    -------------------------
        msg_info	frozen <info>,
    PRIMARY KEY ((chat_id, date), tiemuuid) 	
    ) WITH CLUSTERING ORDER BY (timestamp DESC)
    """
    __keyspace__ = KEYSPACE
    chat_id         = columns.UUID(primary_key=True)
    date            = columns.Date(primary_key=True, required=True)
    time            = columns.TimeUUID(primary_key=True, clustering_order="DESC", required=True)
    msg_info        = columns.UserDefinedType(message_info)


class PrivateChat(Model):
    """ User 1 - 1 chat data. 
    
    Q: Gen N last messages in user-user chat.
    
    CREATE TABLE PrivateChat (
        chat_id		UUID,
        date		text,	
        time		timeuuid
        -------------------------
        msg_info	FROZEN <info>,
    PRIMARY KEY ((chat_id, date), timestamp)
    ) WITH CLUSTERING ORDER BY (timestamp DESC)
    """
    __keyspace__ = KEYSPACE
    chat_id         = columns.UUID(primary_key=True)
    date            = columns.Date(required=True, primary_key=True, clustering_order="DESC")
    time            = columns.TimeUUID(required=True)
    msg_info        = columns.UserDefinedType(message_info)
    

class UserConversations(Model):
    """ User chats. 
    
    Q: Get related chats of specific <user> sorted by status?

    CRATE TABLE UserConversations (
        user_id		UUID PRIMARY KEY,	
        chats		list[UUID],
    )
    """
    __keyspace__ = KEYSPACE
    user_id         = columns.UUID(primary_key=True)
    chats           = columns.List(value_type=columns.UUID) # Note: collection types may lead to tombstone generation.
    

class ClientChats(Model):
    """ Client chats. 

    Q: Get all chats of <client> X.

    CREATE TABLE ClientChats(
        client_id 	UUID PRIMARY KEY,
        chats		set<UUIDS>,
    )
    """
    __keyspace__ = KEYSPACE
    client_id       = columns.UUID(primary_key=True)
    chats           = columns.List(value_type=columns.UUID)
    

if __name__ == "__main__":
    cluster = Cluster(['0.0.0.0'],port=9042)
    session = cluster.connect(KEYSPACE)

    session.execute(f'USE {KEYSPACE}')
    sync_table(GlobalChat) # apply ORM models to CQL - sync

    schema_info = session.execute("DESC SCHEMA")
    print(schema_info)
