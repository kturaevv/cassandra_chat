

class CassandraManager:
    INSERT_ORIGIN = """INSERT INTO origin (
            origin_id, year, month, message_id, message)
            VALUES (?, ?, ?, now(), ?)"""

    INSERT_PRIVATE = """INSERT INTO private (
            origin_id, user_id, chat_id, message_id, message) 
            VALUES (?, ?, ?, now(), ?)"""
    
    def __init__(self) -> None:
        ...

    def get_session():
        ...
    
    def paginator():
        ...

