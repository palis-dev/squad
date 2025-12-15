from typing import Any, Dict, List

from app.agents.base import AgentOutput, AgentRole, BaseAgent


class PMAgent(BaseAgent):
    role = AgentRole.PM
    name = "Product Manager"
    description = (
        "Manages product requirements, creates tasks, and defines acceptance criteria"
    )
    responsibilities = [
        "Create and prioritize tasks",
        "Define acceptance criteria",
        "Communicate with stakeholders",
        "Review completed work against requirements",
    ]
    tools = ["task_create", "task_update", "notify_stakeholder"]
    system_prompt = """You are a Product Manager (PM) in a software development squad.

Your responsibilities:
1. Analyze feature requests and break them down into actionable tasks
2. Define clear acceptance criteria for each task
3. Prioritize work based on business value
4. Review completed work to ensure it meets requirements

When given a task or feature request:
1. First, understand the business context and user needs
2. Break down complex features into smaller, manageable tasks
3. Write clear acceptance criteria using the format:
   "Given [context], When [action], Then [expected result]"
4. Identify dependencies and risks
5. Decide which team member should work on the task next

Output format:
- Provide a clear analysis of the task
- List acceptance criteria
- Recommend the next agent to handle the task (tech_lead for technical
  planning, frontend_dev or backend_dev for implementation)
- Flag if human approval is needed for major decisions

Always be concise and action-oriented. Focus on delivering value to users."""

    async def process(
        self,
        task_description: str,
        context: Dict[str, Any],
        messages: List[Dict[str, str]],
    ) -> AgentOutput:
        response = await self._call_llm(task_description, context, messages)
        
        next_agent = AgentRole.TECH_LEAD
        task_lower = task_description.lower()
        if "frontend" in task_lower and "backend" not in task_lower:
            next_agent = AgentRole.FRONTEND_DEV
        elif "backend" in task_lower or "api" in task_lower:
            next_agent = AgentRole.BACKEND_DEV
        
        return AgentOutput(
            content=response,
            next_agent=next_agent,
            artifacts=[],
            requires_approval=False,
        )
