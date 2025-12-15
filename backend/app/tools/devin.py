from typing import Optional

import httpx

from app.config import get_settings
from app.tools.base import BaseTool, ToolResult


class DevinTool(BaseTool):
    name = "devin_request"
    description = "Request Devin AI to perform a coding task"
    
    def __init__(self):
        self.settings = get_settings()
    
    async def execute(
        self,
        task: str,
        repo: Optional[str] = None,
        branch: Optional[str] = None,
        context: Optional[str] = None,
    ) -> ToolResult:
        if not self.settings.devin_api_key:
            return ToolResult(
                success=False,
                output=None,
                error=(
                    "Devin API key not configured. "
                    "Please set DEVIN_API_KEY in environment."
                ),
            )
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.settings.devin_api_url}/v1/sessions",
                    headers={
                        "Authorization": f"Bearer {self.settings.devin_api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "prompt": task,
                        "repo": repo,
                        "branch": branch,
                        "context": context,
                    },
                    timeout=30.0,
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return ToolResult(
                        success=True,
                        output={
                            "session_id": data.get("session_id"),
                            "status": data.get("status"),
                            "url": data.get("url"),
                        },
                    )
                else:
                    return ToolResult(
                        success=False,
                        output=None,
                        error=(
                            f"Devin API error: {response.status_code} - "
                            f"{response.text}"
                        ),
                    )
        except httpx.TimeoutException:
            return ToolResult(
                success=False,
                output=None,
                error="Devin API request timed out",
            )
        except Exception as e:
            return ToolResult(
                success=False,
                output=None,
                error=f"Failed to call Devin API: {str(e)}",
            )
    
    async def get_session_status(self, session_id: str) -> ToolResult:
        if not self.settings.devin_api_key:
            return ToolResult(
                success=False,
                output=None,
                error="Devin API key not configured",
            )
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.settings.devin_api_url}/v1/sessions/{session_id}",
                    headers={
                        "Authorization": f"Bearer {self.settings.devin_api_key}",
                    },
                    timeout=30.0,
                )
                
                if response.status_code == 200:
                    return ToolResult(
                        success=True,
                        output=response.json(),
                    )
                else:
                    return ToolResult(
                        success=False,
                        output=None,
                        error=f"Failed to get session status: {response.status_code}",
                    )
        except Exception as e:
            return ToolResult(
                success=False,
                output=None,
                error=f"Failed to get session status: {str(e)}",
            )
