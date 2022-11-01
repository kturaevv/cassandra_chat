""" Live Chat API """

from fastapi import FastAPI
from pydantic import BaseModel

import asyncio

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    ...

class Message(BaseModel):
    ...

class Chat(BaseModel):
    ...


# send_message(user_id, receiver_id, channel_type, message)
# get_messages(user_id, user_id2, channel_type, earliest_message_id)
# join_group(user_id, group_id)

@app.get("/items")
async def update_item(item_id: int | None = None, item: Item | None = None):
    results = {"item_id": item_id, "item": item}
    import random
    text = random.random()
    
    return text

@app.get("/item")
async def update_item():
    await asyncio.sleep(10)
    return {"SUCCESS":"Good work!"}