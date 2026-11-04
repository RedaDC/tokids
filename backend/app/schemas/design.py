"""
TeeDesign AI — Design and Concept Pydantic Schemas
"""
import uuid
from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, ConfigDict, Field


class DesignConceptCreate(BaseModel):
    niche_id: Optional[uuid.UUID] = None
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    style: str = Field(default="illustration", max_length=100)
    color_palette: Optional[list[str]] = None
    composition_notes: Optional[str] = None
    generation_prompt: str


class DesignConceptResponse(BaseModel):
    id: uuid.UUID
    niche_id: Optional[uuid.UUID] = None
    title: str
    description: Optional[str] = None
    style: str
    color_palette: Optional[list[str]] = None
    composition_notes: Optional[str] = None
    generation_prompt: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DesignGenerateRequest(BaseModel):
    concept_id: Optional[uuid.UUID] = None
    title: Optional[str] = None
    prompt: Optional[str] = None
    style: Optional[str] = "vintage t-shirt illustration"
    provider: Optional[str] = None
    model: Optional[str] = None
    width: Optional[int] = 1024
    height: Optional[int] = 1024


class DesignResponse(BaseModel):
    id: uuid.UUID
    concept_id: Optional[uuid.UUID] = None
    title: str
    style: str
    status: str
    file_path: str
    preview_path: Optional[str] = None
    master_path: Optional[str] = None
    width: int
    height: int
    file_size_bytes: int
    generation_provider: str
    generation_model: str
    generation_cost_usd: float
    quality_score: Optional[float] = None
    version_number: int
    is_master: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DesignListResponse(BaseModel):
    items: list[DesignResponse]
    total: int
    page: int
    page_size: int
