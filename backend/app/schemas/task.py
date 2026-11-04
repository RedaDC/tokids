"""
TeeDesign AI — Task and Workflow Pydantic Schemas
"""
import uuid
from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    workflow_id: Optional[uuid.UUID] = None
    agent_id: Optional[uuid.UUID] = None
    input_data: Optional[dict[str, Any]] = None


class TaskResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str] = None
    status: str
    workflow_id: Optional[uuid.UUID] = None
    agent_id: Optional[uuid.UUID] = None
    input_data: Optional[dict[str, Any]] = None
    output_data: Optional[dict[str, Any]] = None
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    retry_count: int
    cost_usd: float
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WorkflowCreate(BaseModel):
    name: str = Field(..., max_length=255)
    niche: Optional[str] = None
    style: Optional[str] = "vintage illustration"
    target_count: int = Field(default=1, ge=1, le=10)
    parameters: Optional[dict[str, Any]] = None


class WorkflowResponse(BaseModel):
    id: uuid.UUID
    name: str
    status: str
    current_step: int
    total_steps: int
    state_data: Optional[dict[str, Any]] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    total_cost_usd: float
    created_at: datetime
    updated_at: datetime
    tasks: Optional[list[TaskResponse]] = None

    model_config = ConfigDict(from_attributes=True)
