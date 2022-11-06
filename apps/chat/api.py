from fastapi import APIRouter

from .schema import OriginChat, PrivateChat

chat = APIRouter(
    prefix="/chat",
    tags=["Chat API"],
)


@chat.get("/read/global")
async def read_global_messages(body: OriginChat):
    ...
    
@chat.get("/read/private")
async def read_private_messages(body: PrivateChat):
    ...

@chat.post("/send")
async def send_message(MessageInfo):
    ...