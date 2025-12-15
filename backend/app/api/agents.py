from fastapi import APIRouter

from app.agents.orchestrator import SquadOrchestrator
from app.schemas.agent import AgentListResponse

router = APIRouter(prefix="/api/agents", tags=["agents"])

orchestrator = SquadOrchestrator()


@router.get("", response_model=AgentListResponse)
async def list_agents():
    agents_info = orchestrator.get_agents_info()
    return AgentListResponse(agents=agents_info)
