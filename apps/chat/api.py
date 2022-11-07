from fastapi import APIRouter, Depends
from datetime import date

from . import schema
from .db import models

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

    if q.before_date is not None: 
        query = models.Origin.objects(
            origin_id = q.origin_id, 
            date = q.before_date,
        ).limit(5)
        
        print(query)
        s = list(query)
        return s

    if q.before_time is not None: 
        q.update({"before_time": q.before_time})
    
    
@chat.get("/p", response_model=schema.Message)
async def read_private_messages(params: schema.PrivateChat = Depends()):
    ...

@chat.post("/send")
async def send_message(body: schema.Message):
    
    ...