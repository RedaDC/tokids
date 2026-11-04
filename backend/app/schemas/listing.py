"""
TeeDesign AI — Listing and SEO Pydantic Schemas
"""
import uuid
from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, ConfigDict, Field


class SEOGenerateRequest(BaseModel):
    design_id: uuid.UUID
    niche: Optional[str] = None
    target_keywords: Optional[list[str]] = None
    category: Optional[str] = "Apparel"
    platform: Optional[str] = "TeePublic"


class ListingCreate(BaseModel):
    design_id: uuid.UUID
    title: str = Field(..., max_length=255)
    description: str
    primary_keyword: str = Field(..., max_length=100)
    tags: Optional[list[str]] = Field(default_factory=list)
    category: str = Field(default="Apparel", max_length=100)
    platform: str = Field(default="TeePublic", max_length=50)
    status: str = Field(default="draft", pattern="^(draft|ready|published)$")
    metadata_json: Optional[dict[str, Any]] = None


class ListingUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    primary_keyword: Optional[str] = None
    tags: Optional[list[str]] = None
    category: Optional[str] = None
    platform: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(draft|ready|published)$")
    metadata_json: Optional[dict[str, Any]] = None


class ListingResponse(BaseModel):
    id: uuid.UUID
    design_id: uuid.UUID
    title: str
    description: str
    primary_keyword: str
    tags: Optional[list[str]] = None
    category: str
    platform: str
    status: str
    metadata_json: Optional[dict[str, Any]] = Field(default=None, alias="metadata")
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
