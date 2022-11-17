""" Pydantic's models to repersent API schema."""

from uuid import UUID
from datetime import date, time

from pydantic import BaseModel
from cassandra.util import uuid_from_time

class Message(BaseModel):
    reply_to: UUID | None = None
    user_id: int | None = None
    username: str
    text: str
    attachment: str | None = None
    read_status: bool


class MessageOrigin(BaseModel):
    origin_id: int
    year: int = date.today().year
    month: int = date.today().month
    message: Message
    

class MessagePrivate(BaseModel):
    origin_id: int
    user_id: int
    chat_id: int
    message: Message


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
