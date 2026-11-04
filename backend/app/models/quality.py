"""
TeeDesign AI — QualityReview and ComplianceReview Models
"""
import enum
import uuid
from datetime import datetime
from typing import Any, Optional
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from app.database.base import Base


class ReviewerType(str, enum.Enum):
    AI = "ai"
    HUMAN = "human"


class ComplianceRiskLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class QualityReview(Base):
    __tablename__ = "quality_reviews"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    design_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("designs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    overall_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    visual_quality_score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )
    originality_score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )
    composition_score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )
    print_suitability_score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )
    niche_relevance_score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )
    is_approved: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    rejection_reason: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    reviewed_by: Mapped[str] = mapped_column(
        String(20),
        default=ReviewerType.AI.value,
        nullable=False,
    )

    # Relationship
    design: Mapped["Design"] = relationship(  # type: ignore # noqa: F821
        "Design",
        back_populates="quality_reviews",
    )


class ComplianceReview(Base):
    __tablename__ = "compliance_reviews"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    design_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("designs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    risk_level: Mapped[str] = mapped_column(
        String(20),
        default=ComplianceRiskLevel.LOW.value,
        nullable=False,
    )
    flags: Mapped[Optional[list[Any]]] = mapped_column(
        JSON,
        nullable=True,
        default=list,
    )
    is_cleared: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    review_notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    reviewed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Relationship
    design: Mapped["Design"] = relationship(  # type: ignore # noqa: F821
        "Design",
        back_populates="compliance_reviews",
    )
