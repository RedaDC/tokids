"""
TeeDesign AI — LangGraph Production Workflow State
"""
from typing import Any, Optional, TypedDict


class WorkflowState(TypedDict, total=False):
    workflow_id: str
    name: str
    niche: str
    style: str
    current_step: int
    total_steps: int
    status: str
    retry_count: int
    max_retries: int
    total_cost_usd: float
    error_message: Optional[str]
    research_data: Optional[dict[str, Any]]
    creative_concept: Optional[dict[str, Any]]
    generation_output: Optional[dict[str, Any]]
    quality_review: Optional[dict[str, Any]]
    compliance_review: Optional[dict[str, Any]]
    seo_metadata: Optional[dict[str, Any]]
    portfolio_package: Optional[dict[str, Any]]
    analytics_summary: Optional[dict[str, Any]]
    logs: list[str]
