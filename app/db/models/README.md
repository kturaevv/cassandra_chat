## Chat keyspace general structure:

QUERIES:
// Read messages from website's global chat
// Read private messages in a website's subchat
// Read chat's that a user has
// Multiple QA accounts can have access to same chats with users

```
CREATE KEYSPACE messages WITH replication = {'class': 'NetworkTopologyStrategy', 'datacenter1': '3'}  AND durable_writes = true;

CREATE TYPE messages.basic_user_info (
    user_id uuid,
    username text,
    avatar text,
    roles text,
);

CREATE TYPE messages.message_info (
    user frozen<basic_user_info>,
    message_id bigint,
    text text,
    reply_to uuid,
    attachment text,
    status bool,
);

CREATE TABLE messages.global_chat (
    origin_id uuid,
    date date,
    time timeuuid,
    msg_info frozen<message_info>,
    PRIMARY KEY ((chat_id, date), time)
) WITH CLUSTERING ORDER BY (time DESC)

CREATE TABLE messages.private_chat (
    user_id uuid,
    chat_id uuid,
    origin_id uuid,

    time timeuuid,
    date date,
    msg_info frozen<message_info>,
    PRIMARY KEY ((user_id, chat_id), time)
) WITH CLUSTERING ORDER BY (time DESC)
```