"""
TeeDesign AI — Analytics Service
"""
import uuid
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.agent import Agent, AgentStatus
from app.models.analytics import CostRecord, PerformanceMetric
from app.models.design import Design, DesignStatus
from app.models.task import WorkflowExecution, WorkflowStatus
from app.schemas.analytics import AnalyticsOverview, CostSummary, PerformanceData


async def get_cost_summary(db: AsyncSession) -> CostSummary:
    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # All-time totals
    all_time_stmt = select(
        func.coalesce(func.sum(CostRecord.cost_usd), 0.0),
        func.coalesce(func.sum(CostRecord.tokens_input), 0),
        func.coalesce(func.sum(CostRecord.tokens_output), 0),
        func.coalesce(func.sum(CostRecord.images_generated), 0),
    )
    all_res = (await db.execute(all_time_stmt)).one()
    total_spend, total_in_tokens, total_out_tokens, total_imgs = all_res

    # Daily spend
    daily_stmt = select(func.coalesce(func.sum(CostRecord.cost_usd), 0.0)).where(
        CostRecord.created_at >= today_start
    )
    daily_spend = (await db.execute(daily_stmt)).scalar_one()

    # Monthly spend
    monthly_stmt = select(func.coalesce(func.sum(CostRecord.cost_usd), 0.0)).where(
        CostRecord.created_at >= month_start
    )
    monthly_spend = (await db.execute(monthly_stmt)).scalar_one()

    # By service
    service_stmt = select(
        CostRecord.service_type,
        func.coalesce(func.sum(CostRecord.cost_usd), 0.0),
    ).group_by(CostRecord.service_type)
    by_service_res = await db.execute(service_stmt)
    spend_by_service = {str(row[0]): float(row[1]) for row in by_service_res.all()}

    # By provider
    provider_stmt = select(
        CostRecord.provider,
        func.coalesce(func.sum(CostRecord.cost_usd), 0.0),
    ).group_by(CostRecord.provider)
    by_provider_res = await db.execute(provider_stmt)
    spend_by_provider = {str(row[0]): float(row[1]) for row in by_provider_res.all()}

    return CostSummary(
        daily_spend_usd=round(float(daily_spend), 4),
        monthly_spend_usd=round(float(monthly_spend), 4),
        total_spend_usd=round(float(total_spend), 4),
        spend_by_service=spend_by_service,
        spend_by_provider=spend_by_provider,
        total_tokens_input=int(total_in_tokens),
        total_tokens_output=int(total_out_tokens),
        total_images_generated=int(total_imgs),
    )


async def get_overview_stats(db: AsyncSession) -> AnalyticsOverview:
    # Design status counts
    status_stmt = select(Design.status, func.count(Design.id)).group_by(Design.status)
    status_res = await db.execute(status_stmt)
    status_counts = {str(row[0]): int(row[1]) for row in status_res.all()}

    total_designs = sum(status_counts.values())
    approved_designs = status_counts.get(DesignStatus.APPROVED.value, 0)
    rejected_designs = status_counts.get(DesignStatus.REJECTED.value, 0)
    draft_designs = status_counts.get(DesignStatus.DRAFT.value, 0)
    exported_designs = status_counts.get(DesignStatus.EXPORTED.value, 0)

    # Average quality score
    avg_score_stmt = select(func.avg(Design.quality_score)).where(
        Design.quality_score.isnot(None)
    )
    avg_score_res = await db.execute(avg_score_stmt)
    avg_score = avg_score_res.scalar_one() or 0.0

    # Active agents
    active_agents_stmt = select(func.count(Agent.id)).where(
        Agent.status == AgentStatus.WORKING.value
    )
    active_agents = (await db.execute(active_agents_stmt)).scalar_one() or 0

    # Completed workflows
    completed_wf_stmt = select(func.count(WorkflowExecution.id)).where(
        WorkflowExecution.status == WorkflowStatus.COMPLETED.value
    )
    completed_wf = (await db.execute(completed_wf_stmt)).scalar_one() or 0

    cost_summary = await get_cost_summary(db)

    # Recent performance metrics
    metrics_stmt = (
        select(PerformanceMetric)
        .order_by(PerformanceMetric.created_at.desc())
        .limit(10)
    )
    metrics_res = await db.execute(metrics_stmt)
    recent_metrics = [
        PerformanceData.model_validate(m) for m in metrics_res.scalars().all()
    ]

    return AnalyticsOverview(
        total_designs=total_designs,
        approved_designs=approved_designs,
        rejected_designs=rejected_designs,
        draft_designs=draft_designs,
        exported_designs=exported_designs,
        total_spent_usd=cost_summary.total_spend_usd,
        avg_quality_score=round(float(avg_score), 2),
        active_agents=int(active_agents),
        completed_workflows=int(completed_wf),
        cost_summary=cost_summary,
        recent_metrics=recent_metrics,
    )


async def get_performance_data(
    db: AsyncSession,
    metric_type: Optional[str] = None,
    design_id: Optional[uuid.UUID] = None,
    limit: int = 50,
) -> list[PerformanceData]:
    stmt = select(PerformanceMetric)
    if metric_type:
        stmt = stmt.where(PerformanceMetric.metric_type == metric_type)
    if design_id:
        stmt = stmt.where(PerformanceMetric.design_id == design_id)

    stmt = stmt.order_by(PerformanceMetric.created_at.desc()).limit(limit)
    result = await db.execute(stmt)
    items = result.scalars().all()
    return [PerformanceData.model_validate(item) for item in items]
