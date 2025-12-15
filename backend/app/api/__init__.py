from app.api.agents import router as agents_router
from app.api.tasks import router as tasks_router
from app.api.websocket import router as websocket_router

__all__ = [
    "tasks_router",
    "agents_router",
    "websocket_router",
]
