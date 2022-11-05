""" Live Chat API """

from fastapi import FastAPI
from pydantic import BaseModel

import asyncio

app = FastAPI()

from uuid import UUID
from datetime import date


class BasicUserInfo(BaseModel):
    user_id: UUID
    username: str


class MessageInfo(BaseModel):
    user: BasicUserInfo
    text: str
    reply_to: UUID
    attachment: str


class OriginChat(BaseModel):
    chat_id: UUID
    date: date
    time: UUID | None = None
    # msg_info: MessageInfo 


class PrivateChat(BaseModel):
    user_id: UUID
    chat_id: UUID
    origin_id: UUID
    date: date


@app.get("/")
async def read_global_messages(OriginChat):
    ...
    
@app.get("/")
async def read_private_messages(PrivateChat):
    ...

@app.post("/")
async def send_message(MessageInfo):
    ...
