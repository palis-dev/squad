from typing import Any, Dict, List

from app.agents.base import AgentOutput, AgentRole, BaseAgent


class TechLeadAgent(BaseAgent):
    role = AgentRole.TECH_LEAD
    name = "Tech Lead"
    description = (
        "Reviews technical plans, identifies risks, and approves implementations"
    )
    responsibilities = [
        "Review technical approaches",
        "Identify technical risks and blockers",
        "Approve implementation plans",
        "Ensure code quality standards",
        "Coordinate between frontend and backend teams",
    ]
    tools = ["code_review", "architecture_review", "approve_plan"]
    system_prompt = """You are a Tech Lead in a software development squad.

Your responsibilities:
1. Review technical approaches and implementation plans
2. Identify potential risks, blockers, and technical debt
3. Ensure the solution aligns with the overall architecture
4. Approve or request changes to implementation plans
5. Coordinate work between frontend and backend developers

When reviewing a task:
1. Analyze the technical requirements
2. Consider scalability, maintainability, and security
3. Identify potential risks and mitigation strategies
4. Create a high-level implementation plan
5. Decide which developer should implement (frontend_dev or backend_dev)

Output format:
- Technical analysis of the task
- Implementation plan with key steps
- Identified risks and mitigations
- Recommendation for which developer should implement
- Flag if the approach needs human approval (for major architectural
  decisions)

Be thorough but pragmatic. Focus on delivering working software while
maintaining quality."""

    async def process(
        self,
        task_description: str,
        context: Dict[str, Any],
        messages: List[Dict[str, str]],
    ) -> AgentOutput:
        response = await self._call_llm(task_description, context, messages)
        
        next_agent = AgentRole.FRONTEND_DEV
        task_lower = task_description.lower()
        backend_keywords = ["api", "database", "backend"]
        frontend_keywords = ["ui", "frontend", "component"]
        if any(kw in task_lower for kw in backend_keywords):
            next_agent = AgentRole.BACKEND_DEV
        elif any(kw in task_lower for kw in frontend_keywords):
            next_agent = AgentRole.FRONTEND_DEV
        
        approval_keywords = ["architecture", "database schema", "security", "auth"]
        requires_approval = any(keyword in task_lower for keyword in approval_keywords)
        
        return AgentOutput(
            content=response,
            next_agent=next_agent,
            artifacts=[],
            requires_approval=requires_approval,
        )
