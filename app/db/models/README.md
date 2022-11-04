## Chat keyspace general structure:

```
CREATE KEYSPACE messages WITH replication = {'class': 'NetworkTopologyStrategy', 'datacenter1': '3'}  AND durable_writes = true;

CREATE TYPE messages.basic_user_info (
    user_id uuid,
    username text
);

CREATE TYPE messages.message_info (
    user frozen<basic_user_info>,
    text text,
    reply_to uuid,
    attachment text
);

CREATE TABLE messages.client_chats (
    client_id uuid PRIMARY KEY,
    chats list<uuid>
) WITH additional_write_policy = '99p'

CREATE TABLE messages.global_chat (
    chat_id uuid,
    date date,
    time timeuuid,
    msg_info frozen<message_info>,
    PRIMARY KEY ((chat_id, date), time)
) WITH CLUSTERING ORDER BY (time DESC)

CREATE TABLE messages.private_chat (
    chat_id uuid,
    date date,
    time timeuuid,
    msg_info frozen<message_info>,
    PRIMARY KEY ((chat_id, date), time)
) WITH CLUSTERING ORDER BY (time DESC)

CREATE TABLE messages.user_conversations (
    user_id uuid PRIMARY KEY,
    chats list<uuid>
) WITH additional_write_policy = '99p'
```