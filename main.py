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
    read_status: bool
    

class OriginChat(BaseModel):
    origin_id: UUID
    before_date: date | None = None
    before_time: UUID | None = None
    # msg_info: MessageInfo 


class PrivateChat(BaseModel):
    user_id: UUID
    chat_id: UUID
    origin_id: UUID
    before_date: date | None = None
    before_time: UUID | None = None


@app.get("/read/global")
async def read_global_messages(body: OriginChat):
    ...
    
@app.get("/read/private")
async def read_private_messages(body: PrivateChat):
    ...

@app.post("/send")
async def send_message(MessageInfo):
    ...
