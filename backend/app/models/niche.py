"""
TeeDesign AI — Niche and ResearchReport Models
"""
import uuid
from typing import Any, Optional
from sqlalchemy import Boolean, Float, ForeignKey, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from app.database.base import Base


class Niche(Base):
    __tablename__ = "niches"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(
        String(200),
        unique=True,
        index=True,
        nullable=False,
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    target_audience: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    competition_level: Mapped[str] = mapped_column(
        String(50),
        default="medium",
        nullable=False,
    )
    opportunity_score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )
    is_seasonal: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    season: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )

    # Relationships
    research_reports: Mapped[list["ResearchReport"]] = relationship(
        "ResearchReport",
        back_populates="niche",
        cascade="all, delete-orphan",
        order_by="desc(ResearchReport.created_at)",
    )
    design_concepts: Mapped[list["DesignConcept"]] = relationship(  # type: ignore # noqa: F821
        "DesignConcept",
        back_populates="niche",
    )


class ResearchReport(Base):
    __tablename__ = "research_reports"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    niche_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("niches.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    summary: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    evidence: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    competition_assessment: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    creative_opportunity: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    confidence_score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )
    raw_data: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSON,
        nullable=True,
        default=dict,
    )

    # Relationship
    niche: Mapped["Niche"] = relationship(
        "Niche",
        back_populates="research_reports",
    )
