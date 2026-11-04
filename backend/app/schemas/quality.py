"""
TeeDesign AI — Quality and Compliance Pydantic Schemas
"""
import uuid
from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, ConfigDict, Field


class QualityEvaluateRequest(BaseModel):
    design_id: uuid.UUID
    notes: Optional[str] = None


class QualityReviewResponse(BaseModel):
    id: uuid.UUID
    design_id: uuid.UUID
    overall_score: float
    visual_quality_score: float
    originality_score: float
    composition_score: float
    print_suitability_score: float
    niche_relevance_score: float
    is_approved: bool
    rejection_reason: Optional[str] = None
    notes: Optional[str] = None
    reviewed_by: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ComplianceReviewResponse(BaseModel):
    id: uuid.UUID
    design_id: uuid.UUID
    risk_level: str
    flags: Optional[list[Any]] = None
    is_cleared: bool
    review_notes: Optional[str] = None
    reviewed_at: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
