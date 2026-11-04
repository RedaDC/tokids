"""
TeeDesign AI — Agent Pydantic Schemas
"""
import uuid
from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, ConfigDict, Field


class AgentStatusUpdate(BaseModel):
    status: str = Field(..., pattern="^(idle|working|completed|failed)$")
    current_task: Optional[str] = None


class AgentLogResponse(BaseModel):
    id: uuid.UUID
    agent_id: uuid.UUID
    level: str
    message: str
    task_id: Optional[str] = None
    metadata_json: Optional[dict[str, Any]] = Field(default=None, alias="metadata")
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class AgentResponse(BaseModel):
    id: uuid.UUID
    name: str
    role: str
    status: str
    current_task: Optional[str] = None
    last_activity: Optional[datetime] = None
    total_tasks: int
    success_rate: float
    tokens_used: int
    cost_usd: float
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
