"""
TeeDesign AI — Listing Model
"""
import enum
import uuid
from typing import Any, Optional
from sqlalchemy import ForeignKey, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from app.database.base import Base


class ListingStatus(str, enum.Enum):
    DRAFT = "draft"
    READY = "ready"
    PUBLISHED = "published"


class Listing(Base):
    __tablename__ = "listings"

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
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    primary_keyword: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    tags: Mapped[Optional[list[str]]] = mapped_column(
        JSON,
        nullable=True,
        default=list,
    )
    category: Mapped[str] = mapped_column(
        String(100),
        default="Apparel",
        nullable=False,
    )
    platform: Mapped[str] = mapped_column(
        String(50),
        default="TeePublic",
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        default=ListingStatus.DRAFT.value,
        nullable=False,
        index=True,
    )
    metadata_json: Mapped[Optional[dict[str, Any]]] = mapped_column(
        "metadata",
        JSON,
        nullable=True,
        default=dict,
    )

    # Relationship
    design: Mapped["Design"] = relationship(  # type: ignore # noqa: F821
        "Design",
        back_populates="listings",
    )
