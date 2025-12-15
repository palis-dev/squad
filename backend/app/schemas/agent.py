from typing import List

from pydantic import BaseModel


class AgentInfo(BaseModel):
    role: str
    name: str
    description: str
    responsibilities: List[str]
    tools: List[str]


class AgentListResponse(BaseModel):
    agents: List[AgentInfo]
