from datetime import datetime

from pydantic import BaseModel, Field


class ArtifactCreate(BaseModel):
    artifact_type: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)


class ArtifactResponse(BaseModel):
    id: int
    task_id: int
    artifact_type: str
    name: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True
