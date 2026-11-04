"""
TeeDesign AI — Schemas Package
"""
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token, TokenPayload
from app.schemas.agent import AgentResponse, AgentLogResponse, AgentStatusUpdate
from app.schemas.task import TaskCreate, TaskResponse, WorkflowCreate, WorkflowResponse
from app.schemas.design import (
    DesignConceptCreate,
    DesignConceptResponse,
    DesignGenerateRequest,
    DesignResponse,
    DesignListResponse,
)
from app.schemas.quality import QualityEvaluateRequest, QualityReviewResponse, ComplianceReviewResponse
from app.schemas.listing import ListingCreate, ListingUpdate, ListingResponse, SEOGenerateRequest
from app.schemas.analytics import AnalyticsOverview, CostSummary, PerformanceData
from app.schemas.settings import SettingsUpdate, SettingsResponse
from app.schemas.research import ResearchStartRequest, ResearchReportResponse, NicheResponse

__all__ = [
    "UserCreate",
    "UserLogin",
    "UserResponse",
    "Token",
    "TokenPayload",
    "AgentResponse",
    "AgentLogResponse",
    "AgentStatusUpdate",
    "TaskCreate",
    "TaskResponse",
    "WorkflowCreate",
    "WorkflowResponse",
    "DesignConceptCreate",
    "DesignConceptResponse",
    "DesignGenerateRequest",
    "DesignResponse",
    "DesignListResponse",
    "QualityEvaluateRequest",
    "QualityReviewResponse",
    "ComplianceReviewResponse",
    "ListingCreate",
    "ListingUpdate",
    "ListingResponse",
    "SEOGenerateRequest",
    "AnalyticsOverview",
    "CostSummary",
    "PerformanceData",
    "SettingsUpdate",
    "SettingsResponse",
    "ResearchStartRequest",
    "ResearchReportResponse",
    "NicheResponse",
]
