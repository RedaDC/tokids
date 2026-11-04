"""
TeeDesign AI — Research and Niche Pydantic Schemas
"""
import uuid
from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, ConfigDict, Field


class ResearchStartRequest(BaseModel):
    niche_query: str = Field(..., min_length=2, max_length=200)
    target_audience: Optional[str] = None
    seasonal_focus: Optional[bool] = False
    season: Optional[str] = None


class ResearchReportResponse(BaseModel):
    id: uuid.UUID
    niche_id: uuid.UUID
    summary: str
    evidence: Optional[str] = None
    competition_assessment: Optional[str] = None
    creative_opportunity: Optional[str] = None
    confidence_score: float
    raw_data: Optional[dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NicheResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str] = None
    target_audience: Optional[str] = None
    competition_level: str
    opportunity_score: float
    is_seasonal: bool
    season: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    reports: Optional[list[ResearchReportResponse]] = None

    model_config = ConfigDict(from_attributes=True)
