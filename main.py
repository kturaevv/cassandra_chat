from fastapi import FastAPI

from apps.chat.api import chat

app = FastAPI()

app.include_router(chat)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}