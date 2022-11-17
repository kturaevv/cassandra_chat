from fastapi import FastAPI

from app.api import chat
from app.ws import ws_router
from app.db import config, methods

app = FastAPI()

app.include_router(chat)
app.include_router(ws_router)

settings = config.get_settings()


@app.on_event('startup')
def connect_db():
    address = settings.address.split(':')
    cluster = Cluster([address[0]], port=address[1], protocol_version=3, load_balancing_policy=DCAwareRoundRobinPolicy())
    session = cluster.connect(settings.keyspace)
    connection.register_connection(str(session), session=session)
    connection.set_default_connection(str(session))
    cassandra_manager.session = session
    cassandra_manager.prep_statements()
    

@app.on_event('shutdown')
def close_db_conn():
    print("Shutting down cassandra connections...")
    settings.session.shutdown()
    settings.cluster.shutdown()
    print("Graceful shutdown complete.")

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}