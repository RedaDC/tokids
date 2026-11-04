"""
TeeDesign AI — Agents API
"""
from __future__ import annotations

from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import Any

from app.api.deps import get_current_user, get_db
from app.models.agent import Agent, AgentLog
from app.models.user import User
import uuid

router = APIRouter()


class AgentResponse(BaseModel):
    id: str
    name: str
    role: str
    description: str
    status: str
    current_task: str | None
    last_activity: str | None
    total_tasks: int
    successful_tasks: int
    failed_tasks: int
    success_rate: float
    tokens_used: int
    cost_usd: float
    avatar_config: dict | None
    created_at: str

    class Config:
        from_attributes = True


class AgentLogResponse(BaseModel):
    id: str
    level: str
    message: str
    task_id: str | None
    metadata: dict | None
    timestamp: str


class AgentStatusUpdate(BaseModel):
    status: str
    current_task: str | None = None


def _agent_to_response(agent: Agent) -> AgentResponse:
    return AgentResponse(
        id=str(agent.id),
        name=agent.name,
        role=agent.role,
        description=agent.description,
        status=agent.status,
        current_task=agent.current_task,
        last_activity=agent.last_activity.isoformat() if agent.last_activity else None,
        total_tasks=agent.total_tasks,
        successful_tasks=agent.successful_tasks,
        failed_tasks=agent.failed_tasks,
        success_rate=agent.success_rate,
        tokens_used=agent.tokens_used,
        cost_usd=agent.cost_usd,
        avatar_config=agent.avatar_config,
        created_at=agent.created_at.isoformat(),
    )


@router.get("", response_model=list[AgentResponse])
async def list_agents(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Agent).order_by(Agent.created_at))
    agents = result.scalars().all()
    return [_agent_to_response(a) for a in agents]


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Agent).where(Agent.id == uuid.UUID(agent_id)))
    agent = result.scalar_one_or_none()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return _agent_to_response(agent)


@router.get("/{agent_id}/logs", response_model=list[AgentLogResponse])
async def get_agent_logs(
    agent_id: str,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(AgentLog)
        .where(AgentLog.agent_id == uuid.UUID(agent_id))
        .order_by(desc(AgentLog.timestamp))
        .limit(limit)
    )
    logs = result.scalars().all()
    return [
        AgentLogResponse(
            id=str(log.id),
            level=log.level,
            message=log.message,
            task_id=log.task_id,
            metadata=log.metadata,
            timestamp=log.timestamp.isoformat(),
        )
        for log in logs
    ]


@router.put("/{agent_id}/status")
async def update_agent_status(
    agent_id: str,
    update: AgentStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Agent).where(Agent.id == uuid.UUID(agent_id)))
    agent = result.scalar_one_or_none()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    agent.status = update.status
    agent.current_task = update.current_task
    agent.last_activity = datetime.now(timezone.utc)
    await db.commit()
    return {"message": "Status updated", "agent_id": agent_id, "status": update.status}
