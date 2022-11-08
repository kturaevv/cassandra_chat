from fastapi import APIRouter, Depends
from datetime import date

from . import schema
from .db import models, config

settings = config.get_settings()

chat = APIRouter(
    prefix="/chat",
    tags=["Chat API"],
)

@chat.get("/g", summary="Read messages from OG chat")
async def read_global_messages(q: schema.OriginChat = Depends()):
    """
    Read latest messages for specific website:

    - **origin_id**: Website's id
    - **before_date**: messages before this date
    - **before_time**: messages before this time

    This API will return certain amount of messages. So, in other words to get "older" messages, \
    provide the earliest message date and API will return N messages before this date.
    """
    q = models.Origin.all().limit(5)
    return list(q)

@chat.get("/p", response_model=schema.MessageBase)
async def read_private_messages(params: schema.PrivateChat = Depends()):
    """
    Send message to private chat, i.e. 1 to 1 chat.
    """

@chat.post("/send/g")
async def send_message(body: schema.MessageOrigin):
    """
    Send message to Origin (Global) chat.
    """
    insert_origin = settings.session.prepare("""INSERT INTO origin (
            origin_id, year, month, message_id, message)
            VALUES (?, ?, ?, now(), ?)""")
        

@chat.post("/send/g")
async def send_message(body: schema.MessagePrivate):
    """
    Send message to Origin (Global) chat.
    """
    insert_origin = settings.session.prepare("""INSERT INTO private (
            origin_id, user_id, chat_id, message_id, message) 
            VALUES (?, ?, ?, now(), ?)""")