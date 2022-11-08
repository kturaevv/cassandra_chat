from fastapi import FastAPI

from apps.chat.api import chat
from apps.chat.db import config

from cassandra.cqlengine import connection
from cassandra.cluster import Cluster
from cassandra.policies import DCAwareRoundRobinPolicy

app = FastAPI()

app.include_router(chat)

settings = config.get_settings()

@app.on_event('startup')
def connect_db():
    address = settings.address.split(':')
    cluster = Cluster([address[0]], port=address[1], protocol_version=3, load_balancing_policy=DCAwareRoundRobinPolicy())
    session = cluster.connect(settings.keyspace)
    connection.register_connection(str(session), session=session)
    connection.set_default_connection(str(session))
    settings.cluster = cluster
    settings.session = session

@app.on_event('shutdown')
def close_db_conn():
    print("Shutting down cassandra connections...")
    settings.cluster.shutdown()
    settings.session.shutdown()
    print("Graceful shutdown complete.")

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}