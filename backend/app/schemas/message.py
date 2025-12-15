from datetime import datetime

from pydantic import BaseModel, Field


class MessageCreate(BaseModel):
    agent_role: str = Field(..., min_length=1, max_length=50)
    content: str = Field(..., min_length=1)
    message_type: str = Field(default="message", max_length=50)


class MessageResponse(BaseModel):
    id: int
    task_id: int
    agent_role: str
    content: str
    message_type: str
    created_at: datetime

    class Config:
        from_attributes = True
