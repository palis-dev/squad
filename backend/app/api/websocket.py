import json
from typing import Dict, Set

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(tags=["websocket"])


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, task_id: int):
        await websocket.accept()
        if task_id not in self.active_connections:
            self.active_connections[task_id] = set()
        self.active_connections[task_id].add(websocket)

    def disconnect(self, websocket: WebSocket, task_id: int):
        if task_id in self.active_connections:
            self.active_connections[task_id].discard(websocket)
            if not self.active_connections[task_id]:
                del self.active_connections[task_id]

    async def broadcast_to_task(self, task_id: int, message: dict):
        if task_id in self.active_connections:
            message_json = json.dumps(message)
            for connection in self.active_connections[task_id]:
                try:
                    await connection.send_text(message_json)
                except Exception:
                    pass


manager = ConnectionManager()


@router.websocket("/ws/tasks/{task_id}")
async def websocket_endpoint(websocket: WebSocket, task_id: int):
    await manager.connect(websocket, task_id)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            await manager.broadcast_to_task(
                task_id,
                {
                    "type": "user_message",
                    "content": message.get("content", ""),
                },
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket, task_id)
    except Exception:
        manager.disconnect(websocket, task_id)


def get_connection_manager() -> ConnectionManager:
    return manager
