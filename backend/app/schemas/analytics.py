"""
TeeDesign AI — Analytics Pydantic Schemas
"""
import uuid
from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, ConfigDict


class CostSummary(BaseModel):
    daily_spend_usd: float
    monthly_spend_usd: float
    total_spend_usd: float
    spend_by_service: dict[str, float]
    spend_by_provider: dict[str, float]
    total_tokens_input: int
    total_tokens_output: int
    total_images_generated: int


class PerformanceData(BaseModel):
    id: uuid.UUID
    design_id: Optional[uuid.UUID] = None
    metric_type: str
    value: float
    unit: str
    period: str
    source: str
    notes: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AnalyticsOverview(BaseModel):
    total_designs: int
    approved_designs: int
    rejected_designs: int
    draft_designs: int
    exported_designs: int
    total_spent_usd: float
    avg_quality_score: float
    active_agents: int
    completed_workflows: int
    cost_summary: CostSummary
    recent_metrics: list[PerformanceData]
