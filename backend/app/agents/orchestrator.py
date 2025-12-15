from typing import Annotated, Any, Dict, List, Optional, TypedDict

from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

from app.agents.base import AgentRole
from app.agents.roles import BackendDevAgent, FrontendDevAgent, PMAgent, TechLeadAgent


class SquadState(TypedDict):
    task_id: int
    task_description: str
    messages: Annotated[List[Dict[str, Any]], add_messages]
    current_agent: Optional[str]
    artifacts: List[Dict[str, Any]]
    status: str
    requires_approval: bool
    iteration_count: int


class SquadOrchestrator:
    def __init__(self):
        self.agents = {
            AgentRole.PM: PMAgent(),
            AgentRole.TECH_LEAD: TechLeadAgent(),
            AgentRole.FRONTEND_DEV: FrontendDevAgent(),
            AgentRole.BACKEND_DEV: BackendDevAgent(),
        }
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        workflow = StateGraph(SquadState)

        workflow.add_node("pm", self._pm_node)
        workflow.add_node("tech_lead", self._tech_lead_node)
        workflow.add_node("frontend_dev", self._frontend_dev_node)
        workflow.add_node("backend_dev", self._backend_dev_node)
        workflow.add_node("human_approval", self._human_approval_node)

        workflow.set_entry_point("pm")

        workflow.add_conditional_edges(
            "pm",
            self._route_from_pm,
            {
                "tech_lead": "tech_lead",
                "frontend_dev": "frontend_dev",
                "backend_dev": "backend_dev",
                "end": END,
            },
        )

        workflow.add_conditional_edges(
            "tech_lead",
            self._route_from_tech_lead,
            {
                "frontend_dev": "frontend_dev",
                "backend_dev": "backend_dev",
                "human_approval": "human_approval",
                "end": END,
            },
        )

        workflow.add_conditional_edges(
            "frontend_dev",
            self._route_from_dev,
            {
                "backend_dev": "backend_dev",
                "tech_lead": "tech_lead",
                "end": END,
            },
        )

        workflow.add_conditional_edges(
            "backend_dev",
            self._route_from_dev,
            {
                "frontend_dev": "frontend_dev",
                "tech_lead": "tech_lead",
                "end": END,
            },
        )

        workflow.add_conditional_edges(
            "human_approval",
            self._route_after_approval,
            {
                "frontend_dev": "frontend_dev",
                "backend_dev": "backend_dev",
                "end": END,
            },
        )

        return workflow.compile()

    async def _pm_node(self, state: SquadState) -> Dict[str, Any]:
        agent = self.agents[AgentRole.PM]
        output = await agent.process(
            state["task_description"],
            {"status": state["status"], "artifacts": state["artifacts"]},
            state["messages"],
        )

        return {
            "messages": [{"role": "pm", "content": output.content}],
            "current_agent": output.next_agent.value if output.next_agent else None,
            "artifacts": state["artifacts"] + output.artifacts,
            "requires_approval": output.requires_approval,
            "iteration_count": state["iteration_count"] + 1,
        }

    async def _tech_lead_node(self, state: SquadState) -> Dict[str, Any]:
        agent = self.agents[AgentRole.TECH_LEAD]
        output = await agent.process(
            state["task_description"],
            {"status": state["status"], "artifacts": state["artifacts"]},
            state["messages"],
        )

        return {
            "messages": [{"role": "tech_lead", "content": output.content}],
            "current_agent": output.next_agent.value if output.next_agent else None,
            "artifacts": state["artifacts"] + output.artifacts,
            "requires_approval": output.requires_approval,
            "iteration_count": state["iteration_count"] + 1,
        }

    async def _frontend_dev_node(self, state: SquadState) -> Dict[str, Any]:
        agent = self.agents[AgentRole.FRONTEND_DEV]
        output = await agent.process(
            state["task_description"],
            {"status": state["status"], "artifacts": state["artifacts"]},
            state["messages"],
        )

        return {
            "messages": [{"role": "frontend_dev", "content": output.content}],
            "current_agent": output.next_agent.value if output.next_agent else None,
            "artifacts": state["artifacts"] + output.artifacts,
            "requires_approval": output.requires_approval,
            "iteration_count": state["iteration_count"] + 1,
        }

    async def _backend_dev_node(self, state: SquadState) -> Dict[str, Any]:
        agent = self.agents[AgentRole.BACKEND_DEV]
        output = await agent.process(
            state["task_description"],
            {"status": state["status"], "artifacts": state["artifacts"]},
            state["messages"],
        )

        return {
            "messages": [{"role": "backend_dev", "content": output.content}],
            "current_agent": output.next_agent.value if output.next_agent else None,
            "artifacts": state["artifacts"] + output.artifacts,
            "requires_approval": output.requires_approval,
            "iteration_count": state["iteration_count"] + 1,
        }

    async def _human_approval_node(self, state: SquadState) -> Dict[str, Any]:
        return {
            "messages": [
                {
                    "role": "system",
                    "content": "Awaiting human approval for the proposed approach.",
                }
            ],
            "status": "awaiting_approval",
            "requires_approval": False,
        }

    def _route_from_pm(self, state: SquadState) -> str:
        if state["iteration_count"] > 10:
            return "end"
        next_agent = state.get("current_agent")
        if next_agent == "tech_lead":
            return "tech_lead"
        elif next_agent == "frontend_dev":
            return "frontend_dev"
        elif next_agent == "backend_dev":
            return "backend_dev"
        return "tech_lead"

    def _route_from_tech_lead(self, state: SquadState) -> str:
        if state["iteration_count"] > 10:
            return "end"
        if state.get("requires_approval"):
            return "human_approval"
        next_agent = state.get("current_agent")
        if next_agent == "frontend_dev":
            return "frontend_dev"
        elif next_agent == "backend_dev":
            return "backend_dev"
        return "end"

    def _route_from_dev(self, state: SquadState) -> str:
        if state["iteration_count"] > 10:
            return "end"
        next_agent = state.get("current_agent")
        if next_agent == "frontend_dev":
            return "frontend_dev"
        elif next_agent == "backend_dev":
            return "backend_dev"
        elif next_agent == "tech_lead":
            return "tech_lead"
        return "end"

    def _route_after_approval(self, state: SquadState) -> str:
        next_agent = state.get("current_agent")
        if next_agent == "frontend_dev":
            return "frontend_dev"
        elif next_agent == "backend_dev":
            return "backend_dev"
        return "end"

    async def run(
        self,
        task_id: int,
        task_description: str,
        initial_messages: List[Dict[str, Any]] = None,
    ) -> SquadState:
        initial_state: SquadState = {
            "task_id": task_id,
            "task_description": task_description,
            "messages": initial_messages or [],
            "current_agent": None,
            "artifacts": [],
            "status": "in_progress",
            "requires_approval": False,
            "iteration_count": 0,
        }

        final_state = await self.graph.ainvoke(initial_state)
        return final_state

    def get_agents_info(self) -> List[Dict[str, Any]]:
        return [agent.get_info() for agent in self.agents.values()]
