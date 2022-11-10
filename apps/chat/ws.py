from fastapi.responses import HTMLResponse
from fastapi import WebSocket, WebSocketDisconnect, Request, Response, APIRouter
from . import schema

ws_router = APIRouter(
    prefix="/ws",
    tags=["Chat API WebSocket"]
)


class SocketManager:
    """ Socket manager for chat rooms, both private and global. """
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = {}

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


manager = SocketManager()


@ws_router.websocket("/connect/{origin_id}")
async def websocket_endpoint(websocket: WebSocket, origin_id: int):
    await manager.connect(websocket, origin_id)
    await websocket.send_json({"Connected to socket: ":origin_id})

    try:
        while True:
            data = await websocket.receive_json()
            # await manager.send_text(f"You wrote: {data}", websocket)
            await manager.broadcast({}, origin_id=origin_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, origin_id=origin_id)
        await manager.broadcast({}, origin_id=origin_id)
