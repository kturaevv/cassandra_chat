""" Pydantic's models to repersent API schema."""

from uuid import UUID
from datetime import date, time

from pydantic import BaseModel


class MessageBase(BaseModel):
    message_id: UUID
    user_id: int | None = None
    username: str
    text: str
    reply_to: UUID
    attachment: str
    read_status: bool


class MessageOrigin(MessageBase):
    origin_id: int
    

class MessagePrivate(MessageBase):
    chat_id: int


class OriginChat(BaseModel):
    """ Query params for Origin chats"""
    origin_id: int
    before_date: date | None = None
    before_time: time | None = None


class PrivateChat(BaseModel):
    """ Query params for Private chats"""
    origin_id: int
    user_id: int
    before_date: date | None = None
    before_time: time | None = None
