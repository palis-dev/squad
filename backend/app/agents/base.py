from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from app.config import get_settings


class AgentRole(str, Enum):
    PM = "pm"
    TECH_LEAD = "tech_lead"
    FRONTEND_DEV = "frontend_dev"
    BACKEND_DEV = "backend_dev"


class AgentOutput(BaseModel):
    content: str
    next_agent: Optional[AgentRole] = None
    artifacts: List[Dict[str, Any]] = []
    requires_approval: bool = False


class BaseAgent(ABC):
    role: AgentRole
    name: str
    description: str
    responsibilities: List[str]
    tools: List[str]
    system_prompt: str

    def __init__(self):
        settings = get_settings()
        self.llm = ChatOpenAI(
            model=settings.openai_model,
            api_key=settings.openai_api_key,
            temperature=0.7,
        )

    @abstractmethod
    async def process(
        self,
        task_description: str,
        context: Dict[str, Any],
        messages: List[Dict[str, str]],
    ) -> AgentOutput:
        pass

    async def _call_llm(
        self,
        task_description: str,
        context: Dict[str, Any],
        messages: List[Dict[str, str]],
    ) -> str:
        system_message = SystemMessage(content=self.system_prompt)
        
        context_str = f"""
Task: {task_description}

Context:
- Status: {context.get('status', 'pending')}
- Previous decisions: {context.get('decisions', [])}
- Artifacts: {context.get('artifacts', [])}
"""
        
        chat_messages = [system_message, HumanMessage(content=context_str)]
        
        for msg in messages:
            if msg.get("role") == "assistant":
                chat_messages.append(AIMessage(content=msg["content"]))
            else:
                chat_messages.append(HumanMessage(content=msg["content"]))
        
        response = await self.llm.ainvoke(chat_messages)
        return response.content

    def get_info(self) -> Dict[str, Any]:
        return {
            "role": self.role.value,
            "name": self.name,
            "description": self.description,
            "responsibilities": self.responsibilities,
            "tools": self.tools,
        }
