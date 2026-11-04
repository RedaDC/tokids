"""
TeeDesign AI — PerformanceMetric and CostRecord Models
"""
import enum
import uuid
from typing import Optional
from sqlalchemy import Float, ForeignKey, Integer, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class ServiceType(str, enum.Enum):
    LLM = "llm"
    IMAGE_GENERATION = "image_generation"
    OTHER = "other"


class PerformanceMetric(Base):
    __tablename__ = "performance_metrics"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    design_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("designs.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    metric_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )
    value: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    unit: Mapped[str] = mapped_column(
        String(50),
        default="count",
        nullable=False,
    )
    period: Mapped[str] = mapped_column(
        String(50),
        default="daily",
        nullable=False,
    )
    source: Mapped[str] = mapped_column(
        String(100),
        default="system",
        nullable=False,
    )
    notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )


class CostRecord(Base):
    __tablename__ = "cost_records"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    service_type: Mapped[str] = mapped_column(
        String(50),
        default=ServiceType.LLM.value,
        nullable=False,
        index=True,
    )
    provider: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    model: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    tokens_input: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    tokens_output: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    images_generated: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    cost_usd: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )
    task_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("tasks.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    agent_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("agents.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
