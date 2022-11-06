## Chat keyspace general structure:

QUERIES:
// Read messages from website's global chat
// Read private messages in a website's subchat
// Read chat's that a user has
// Multiple QA accounts can have access to same chats with users

```
CCREATE TYPE messages.basic_user_info (
    user_id uuid,
    username text
);

CREATE TYPE messages.message_info (
    user frozen<basic_user_info>,
    text text,
    reply_to uuid,
    attachment text,
    read_status boolean
);

CREATE TABLE messages.global_chat (
    origin_id uuid,
    date date,
    time timeuuid,
    msg_info frozen<message_info>,
    PRIMARY KEY ((origin_id, date), time)
) WITH CLUSTERING ORDER BY (time DESC)

CREATE TABLE messages.private_chat (
    user_id uuid,
    chat_id uuid,
    time timeuuid,
    date date,
    msg_info frozen<message_info>,
    origin_id uuid,
    PRIMARY KEY ((user_id, chat_id), time)
) WITH CLUSTERING ORDER BY (time DESC)

```