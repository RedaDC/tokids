"""
TeeDesign AI — Analytics API
"""
from __future__ import annotations

from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc

from app.api.deps import get_current_user, get_db
from app.models.design import Design
from app.models.agent import Agent
from app.models.task import Task, WorkflowExecution
from app.models.analytics import CostRecord, PerformanceMetric
from app.models.user import User

router = APIRouter()


class OverviewResponse(BaseModel):
    total_designs: int
    approved_designs: int
    rejected_designs: int
    draft_designs: int
    active_agents: int
    completed_tasks: int
    total_cost_usd: float
    avg_quality_score: float
    approval_rate: float
    is_stub: bool = False


class CostSummaryResponse(BaseModel):
    total_cost_usd: float
    daily_cost_usd: float
    monthly_cost_usd: float
    cost_per_design: float
    cost_by_service: list[dict]
    recent_records: list[dict]


class DailyProductionPoint(BaseModel):
    date: str
    generated: int
    approved: int
    rejected: int
    cost_usd: float


@router.get("/overview", response_model=OverviewResponse)
async def get_overview(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Design counts
    total_q = await db.execute(select(func.count(Design.id)))
    total_designs = total_q.scalar() or 0

    approved_q = await db.execute(select(func.count(Design.id)).where(Design.status == "approved"))
    approved_designs = approved_q.scalar() or 0

    rejected_q = await db.execute(select(func.count(Design.id)).where(Design.status == "rejected"))
    rejected_designs = rejected_q.scalar() or 0

    draft_q = await db.execute(select(func.count(Design.id)).where(Design.status.in_(["draft", "queued"])))
    draft_designs = draft_q.scalar() or 0

    # Active agents
    active_q = await db.execute(select(func.count(Agent.id)).where(Agent.status == "working"))
    active_agents = active_q.scalar() or 0

    # Completed tasks
    tasks_q = await db.execute(select(func.count(Task.id)).where(Task.status == "completed"))
    completed_tasks = tasks_q.scalar() or 0

    # Total cost
    cost_q = await db.execute(select(func.sum(CostRecord.cost_usd)))
    total_cost = float(cost_q.scalar() or 0)

    # Avg quality
    qual_q = await db.execute(select(func.avg(Design.quality_score)).where(Design.quality_score.isnot(None)))
    avg_quality = float(qual_q.scalar() or 0)

    approval_rate = (approved_designs / total_designs * 100) if total_designs > 0 else 0

    return OverviewResponse(
        total_designs=total_designs,
        approved_designs=approved_designs,
        rejected_designs=rejected_designs,
        draft_designs=draft_designs,
        active_agents=active_agents,
        completed_tasks=completed_tasks,
        total_cost_usd=round(total_cost, 4),
        avg_quality_score=round(avg_quality, 1),
        approval_rate=round(approval_rate, 1),
    )


@router.get("/costs", response_model=CostSummaryResponse)
async def get_costs(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Total
    total_q = await db.execute(select(func.sum(CostRecord.cost_usd)))
    total_cost = float(total_q.scalar() or 0)

    # Daily
    daily_q = await db.execute(
        select(func.sum(CostRecord.cost_usd)).where(CostRecord.created_at >= today_start)
    )
    daily_cost = float(daily_q.scalar() or 0)

    # Monthly
    monthly_q = await db.execute(
        select(func.sum(CostRecord.cost_usd)).where(CostRecord.created_at >= month_start)
    )
    monthly_cost = float(monthly_q.scalar() or 0)

    # Cost per design
    total_designs_q = await db.execute(select(func.count(Design.id)).where(Design.status == "approved"))
    total_approved = total_designs_q.scalar() or 1
    cost_per_design = total_cost / total_approved

    # Cost by service
    service_q = await db.execute(
        select(CostRecord.service_type, func.sum(CostRecord.cost_usd))
        .group_by(CostRecord.service_type)
    )
    cost_by_service = [
        {"service": row[0], "cost_usd": round(float(row[1]), 4)}
        for row in service_q.all()
    ]

    # Recent records
    recent_q = await db.execute(
        select(CostRecord).order_by(desc(CostRecord.created_at)).limit(20)
    )
    recent = recent_q.scalars().all()
    recent_records = [
        {
            "id": str(r.id),
            "service_type": r.service_type,
            "provider": r.provider,
            "model": r.model,
            "cost_usd": r.cost_usd,
            "timestamp": r.created_at.isoformat(),
        }
        for r in recent
    ]

    return CostSummaryResponse(
        total_cost_usd=round(total_cost, 4),
        daily_cost_usd=round(daily_cost, 4),
        monthly_cost_usd=round(monthly_cost, 4),
        cost_per_design=round(cost_per_design, 4),
        cost_by_service=cost_by_service,
        recent_records=recent_records,
    )


@router.get("/designs")
async def get_design_analytics(
    days: int = 30,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Daily production data for charts."""
    now = datetime.now(timezone.utc)
    start_date = now - timedelta(days=days)

    # Get designs grouped by date
    result = await db.execute(
        select(Design.created_at, Design.status, Design.generation_cost_usd)
        .where(Design.created_at >= start_date)
        .order_by(Design.created_at)
    )
    rows = result.all()

    # Aggregate by day
    daily: dict[str, dict] = {}
    for row in rows:
        day = row[0].strftime("%Y-%m-%d")
        if day not in daily:
            daily[day] = {"date": day, "generated": 0, "approved": 0, "rejected": 0, "cost_usd": 0.0}
        daily[day]["generated"] += 1
        daily[day]["cost_usd"] += float(row[2] or 0)
        if row[1] == "approved":
            daily[day]["approved"] += 1
        elif row[1] == "rejected":
            daily[day]["rejected"] += 1

    return {"data": list(daily.values()), "period_days": days}


@router.get("/performance")
async def get_performance(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Performance metrics — only real data, no fabrication."""
    result = await db.execute(
        select(PerformanceMetric).order_by(desc(PerformanceMetric.created_at)).limit(100)
    )
    metrics = result.scalars().all()
    return {
        "metrics": [
            {
                "id": str(m.id),
                "type": m.metric_type,
                "value": m.value,
                "unit": m.unit,
                "period": m.period,
                "source": m.source,
                "timestamp": m.created_at.isoformat(),
            }
            for m in metrics
        ],
        "note": "Data reflects actual production records only. Marketplace performance data shown only when lawfully available.",
    }
