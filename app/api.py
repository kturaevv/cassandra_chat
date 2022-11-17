from fastapi import APIRouter, Depends
from datetime import date

from . import schema
from .db import models, config
from .db.methods import CRUD

from fastapi import Request

settings = config.get_settings()

chat = APIRouter(
    prefix="/chat",
    tags=["Chat API"]
)

@chat.get("/global", summary="Read messages from OG chat")
async def read_global_messages(r: Request, params: schema.OriginChat = Depends()):
    """
    Read latest messages for specific website:

    - **origin_id**: Website's id
    - **before_date**: messages before this date
    - **before_time**: messages before this time

    This API will return certain amount of messages. So, in other words to get "older" messages, \
    provide the earliest message date and API will return N messages before this date.
    """
    current_date = date.today()

    q = models.Origin.filter(
        origin_id=params.origin_id, 
        year=current_date.year, 
        month=current_date.month).limit(5)
    return list(q)

@chat.get("/private")
async def read_private_messages(params: schema.PrivateChat = Depends()):
    """
    Send message to private chat, i.e. 1 to 1 chat.
    """
    q = models.Private.filter(
        origin_id=params.origin_id,
        user_id=params.user_id
    ).limit(5)
    return list(q)

@chat.post("/send/global", status_code=201)
async def send_global_messages(body: schema.MessageOrigin):
    """
    Send message to Origin (Global) chat:

    - **origin_id**: Website's id
    - **message**: Message info nested json
    """
    CRUD.insert_async_origin(params = body)
    return {"Success":200}

@chat.post("/send/private", status_code=201)
async def send_private_messages(body: schema.MessagePrivate):
    """
    Send message to Origin (Global) chat:
    
    - **origin_id**: Website's id
    - **chat_id**: Conversation id
    - **message**: Message info nested json
    """
    CRUD.insert_async_private(params = body)
    return {"Success":200}
