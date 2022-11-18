from fastapi.responses import HTMLResponse
from fastapi import WebSocket, WebSocketDisconnect, Request, Response, APIRouter
from . import schema
from .db.crud import CRUD


ws_router = APIRouter(
    prefix="/ws",
    tags=["Chat API WebSocket"]
)


class SocketManager:
    """ Socket manager for chat rooms, both private and global. """
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = {}
        self.paging_state = None

    async def connect(self, websocket: WebSocket, origin_id: int):
        """ Connect to a given origin. """
        await websocket.accept()
        
        if not self.active_connections.get(origin_id, 0):
            self.active_connections[origin_id] = []
        
        self.active_connections[origin_id].append(websocket)

    def disconnect(self, websocket: WebSocket, origin_id: int):
        try:
            self.active_connections[origin_id].remove(websocket)
        except ValueError:
            pass

    async def send_personal_msg(self, websocket: WebSocket, message: schema.Message):
        """ Send text to specific socket. """
        await websocket.send_json(message)

    async def broadcast(self, message: schema.Message, origin_id:int):
        """ Broadcast a message in a given origin. """
        for connection in self.active_connections[origin_id]:
            await connection.send_json(message)
    
    async def bind_paging_state(self, websocket, paging_state):
        self.paging_state[websocket] = paging_state


manager = SocketManager()
crud = CRUD()


@ws_router.websocket("/connect/{origin_id}")
async def websocket_endpoint(websocket: WebSocket, origin_id: int):
    await manager.connect(websocket, origin_id)
    
    # Download latest messages for origin_id
    data, staging_state = await crud.get_origin_messages()
    
    # Send latest messages to connected socket
    await websocket.send_json(data)

    # Bind paging state for further queries
    await manager.bind_paging_state(websocket, staging_state)

    try:
        while True:
            data = await websocket.receive_json()
            
            # Validate with Pydantic
            validated_data = schema.Message(**data)

            # Insert to DB
            if validated_data.chat_id:
                # Insert to private chats
                crud.insert_async_private(validated_data)
            else: 
                # Insert to origin chats
                crud.insert_async_origin(validated_data)

            await manager.broadcast({}, origin_id=origin_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, origin_id=origin_id)
        await manager.broadcast({}, origin_id=origin_id)
