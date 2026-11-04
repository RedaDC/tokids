"""
TeeDesign AI — Asset Model
"""
import enum
import uuid
from sqlalchemy import Boolean, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class AssetType(str, enum.Enum):
    MASTER = "master"
    PREVIEW = "preview"
    EXPORT = "export"
    THUMBNAIL = "thumbnail"


class Asset(Base):
    __tablename__ = "assets"

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
    asset_type: Mapped[str] = mapped_column(
        String(50),
        default=AssetType.MASTER.value,
        nullable=False,
        index=True,
    )
    file_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )
    file_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    mime_type: Mapped[str] = mapped_column(
        String(100),
        default="image/png",
        nullable=False,
    )
    file_size_bytes: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    width: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    height: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    is_transparent: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # Relationship
    design: Mapped["Design"] = relationship(  # type: ignore # noqa: F821
        "Design",
        back_populates="assets",
    )
