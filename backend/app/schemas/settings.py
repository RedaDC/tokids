"""
TeeDesign AI — Settings Pydantic Schemas
"""
import uuid
from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, ConfigDict


class SettingsUpdate(BaseModel):
    value: Any
    description: Optional[str] = None
    is_secret: Optional[bool] = None


class SettingsResponse(BaseModel):
    id: uuid.UUID
    key: str
    value: Any
    description: Optional[str] = None
    is_secret: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
