from uuid import UUID
from datetime import date, time

from pydantic import BaseModel

class BasicUserInfo(BaseModel):
    user_id: UUID | None = None
    username: str
    role: str | None = None


class MessageInfo(BaseModel):
    user: BasicUserInfo
    text: str
    reply_to: UUID
    attachment: str
    read_status: bool


class OriginChat(BaseModel):
    origin_id: UUID
    before_date: date | None = None
    before_time: time | None = None
    # msg_info: MessageInfo 


class PrivateChat(BaseModel):
    user_id: UUID
    chat_id: UUID
    origin_id: UUID
    before_date: date | None = None
    before_time: time | None = None
