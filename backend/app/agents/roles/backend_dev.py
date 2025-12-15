from typing import Any, Dict, List

from app.agents.base import AgentOutput, AgentRole, BaseAgent


class BackendDevAgent(BaseAgent):
    role = AgentRole.BACKEND_DEV
    name = "Backend Developer"
    description = "Implements API endpoints, database models, and business logic"
    responsibilities = [
        "Implement API endpoints",
        "Design database schemas",
        "Write business logic",
        "Handle authentication and authorization",
        "Write backend tests",
    ]
    tools = ["code_generate", "devin_request", "file_write", "database_migrate"]
    system_prompt = """You are a Backend Developer in a software development squad.

Your responsibilities:
1. Implement API endpoints using FastAPI
2. Design and implement database schemas
3. Write business logic and services
4. Handle authentication and authorization
5. Write tests for backend functionality

When implementing a task:
1. Understand the API requirements and data models
2. Design the database schema if needed
3. Implement clean, well-structured API endpoints
4. Use proper error handling and validation
5. Follow RESTful best practices

You have access to Devin for complex coding tasks. Use it when:
- Implementing complex business logic
- Creating database migrations
- Writing comprehensive API tests
- Refactoring existing code

Output format:
- Implementation plan
- API endpoint specifications
- Database schema changes (if any)
- Code snippets or full implementations
- Testing approach
- Flag if you need to call Devin for complex implementations

Focus on creating robust, scalable backend services."""

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
                "name": "backend_implementation",
                "content": response,
            })
        
        next_agent = None
        if "frontend" in response.lower():
            if "ready" in response.lower() or "can now" in response.lower():
                next_agent = AgentRole.FRONTEND_DEV
        
        return AgentOutput(
            content=response,
            next_agent=next_agent,
            artifacts=artifacts,
            requires_approval=False,
        )
