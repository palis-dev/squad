from typing import Any, Dict, List

from app.agents.base import AgentOutput, AgentRole, BaseAgent


class FrontendDevAgent(BaseAgent):
    role = AgentRole.FRONTEND_DEV
    name = "Frontend Developer"
    description = "Implements UI features and components using React"
    responsibilities = [
        "Implement UI components",
        "Handle state management",
        "Integrate with backend APIs",
        "Ensure responsive design",
        "Write frontend tests",
    ]
    tools = ["code_generate", "devin_request", "file_write", "npm_run"]
    system_prompt = """You are a Frontend Developer in a software development squad.

Your responsibilities:
1. Implement UI components using React and TypeScript
2. Handle state management and data flow
3. Integrate with backend APIs
4. Ensure responsive and accessible design
5. Write tests for frontend components

When implementing a task:
1. Understand the UI requirements and acceptance criteria
2. Plan the component structure and state management
3. Write clean, maintainable React code
4. Use TypeScript for type safety
5. Follow best practices for accessibility and performance

You have access to Devin for complex coding tasks. Use it when:
- Implementing complex UI logic
- Creating new components from scratch
- Refactoring existing code
- Writing comprehensive tests

Output format:
- Implementation plan
- Code snippets or full implementations
- Any API requirements for the backend team
- Testing approach
- Flag if you need to call Devin for complex implementations

Focus on creating intuitive, performant user interfaces."""

    async def process(
        self,
        task_description: str,
        context: Dict[str, Any],
        messages: List[Dict[str, str]],
    ) -> AgentOutput:
        response = await self._call_llm(task_description, context, messages)
        
        artifacts = []
        if "```" in response:
            artifacts.append({
                "type": "code",
                "name": "frontend_implementation",
                "content": response,
            })
        
        next_agent = None
        if "backend" in response.lower() or "api" in response.lower():
            if "need" in response.lower() or "require" in response.lower():
                next_agent = AgentRole.BACKEND_DEV
        
        return AgentOutput(
            content=response,
            next_agent=next_agent,
            artifacts=artifacts,
            requires_approval=False,
        )
