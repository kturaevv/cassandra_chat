from fastapi import APIRouter, Depends

from .schema import OriginChat, PrivateChat

from cassandra.cqlengine.connection import session

chat = APIRouter(
    prefix="/chat",
    tags=["Chat API"],
)


@chat.get("/read/global")
async def read_global_messages(params: OriginChat = Depends()):
    ...    
    
@chat.get("/read/private")
async def read_private_messages(params: PrivateChat):
    ...

@chat.post("/send")
async def send_message(MessageInfo):
    ...