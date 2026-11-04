"""
TeeDesign AI — DesignConcept, Design, and DesignVersion Models
"""
import enum
import uuid
from typing import Any, Optional
from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from app.database.base import Base


class DesignStatus(str, enum.Enum):
    DRAFT = "draft"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPORTED = "exported"


class DesignConcept(Base):
    __tablename__ = "design_concepts"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    niche_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("niches.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    style: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    color_palette: Mapped[Optional[list[str]]] = mapped_column(
        JSON,
        nullable=True,
        default=list,
    )
    composition_notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    generation_prompt: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        default="pending",
        nullable=False,
    )

    # Relationships
    niche: Mapped[Optional["Niche"]] = relationship(  # type: ignore # noqa: F821
        "Niche",
        back_populates="design_concepts",
    )
    designs: Mapped[list["Design"]] = relationship(
        "Design",
        back_populates="concept",
        cascade="all, delete-orphan",
    )


class Design(Base):
    __tablename__ = "designs"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    concept_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("design_concepts.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    style: Mapped[str] = mapped_column(
        String(100),
        default="illustration",
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        default=DesignStatus.DRAFT.value,
        nullable=False,
        index=True,
    )
    file_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )
    preview_path: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )
    master_path: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )
    width: Mapped[int] = mapped_column(
        Integer,
        default=1024,
        nullable=False,
    )
    height: Mapped[int] = mapped_column(
        Integer,
        default=1024,
        nullable=False,
    )
    file_size_bytes: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    generation_provider: Mapped[str] = mapped_column(
        String(50),
        default="stub",
        nullable=False,
    )
    generation_model: Mapped[str] = mapped_column(
        String(100),
        default="stub-model",
        nullable=False,
    )
    generation_cost_usd: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )
    quality_score: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )
    version_number: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )
    is_master: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # Relationships
    concept: Mapped[Optional["DesignConcept"]] = relationship(
        "DesignConcept",
        back_populates="designs",
    )
    versions: Mapped[list["DesignVersion"]] = relationship(
        "DesignVersion",
        back_populates="design",
        cascade="all, delete-orphan",
        order_by="DesignVersion.version_number",
    )
    quality_reviews: Mapped[list["QualityReview"]] = relationship(  # type: ignore # noqa: F821
        "QualityReview",
        back_populates="design",
        cascade="all, delete-orphan",
    )
    compliance_reviews: Mapped[list["ComplianceReview"]] = relationship(  # type: ignore # noqa: F821
        "ComplianceReview",
        back_populates="design",
        cascade="all, delete-orphan",
    )
    listings: Mapped[list["Listing"]] = relationship(  # type: ignore # noqa: F821
        "Listing",
        back_populates="design",
        cascade="all, delete-orphan",
    )
    assets: Mapped[list["Asset"]] = relationship(  # type: ignore # noqa: F821
        "Asset",
        back_populates="design",
        cascade="all, delete-orphan",
    )


class DesignVersion(Base):
    __tablename__ = "design_versions"

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
    version_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    file_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )
    changes_description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    quality_score: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )

    # Relationship
    design: Mapped["Design"] = relationship(
        "Design",
        back_populates="versions",
    )
