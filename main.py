from fastapi import FastAPI

from app.api import chat
from app.ws import ws_router
from app.db import config, methods, manager

app = FastAPI()

app.include_router(chat)
app.include_router(ws_router)

settings = config.get_settings()


@app.on_event('startup')
def connect_db():
    manager.ConnManager(settings.keyspace)


@app.on_event('shutdown')
def close_db_conn():
    print("Shutting down cassandra connections...")
    settings.session.shutdown()
    settings.cluster.shutdown()
    print("Graceful shutdown complete.")

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}