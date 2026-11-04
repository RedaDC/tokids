"""
TeeDesign AI — Design Service
"""
import uuid
from typing import Optional
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.asset import Asset, AssetType
from app.models.design import Design, DesignStatus, DesignVersion
from app.services.storage_service import storage_service


async def get_designs(
    db: AsyncSession,
    status: Optional[str] = None,
    style: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
) -> tuple[list[Design], int]:
    stmt = select(Design)
    if status:
        stmt = stmt.where(Design.status == status)
    if style:
        stmt = stmt.where(Design.style.ilike(f"%{style}%"))

    # Total count
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total_result = await db.execute(count_stmt)
    total = total_result.scalar_one()

    # Paginate
    offset = (page - 1) * page_size
    stmt = stmt.order_by(Design.created_at.desc()).offset(offset).limit(page_size)
    result = await db.execute(stmt)
    items = list(result.scalars().all())

    return items, total


async def get_design_by_id(
    db: AsyncSession,
    design_id: uuid.UUID,
) -> Optional[Design]:
    stmt = select(Design).where(Design.id == design_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_design(
    db: AsyncSession,
    title: str,
    file_path: str,
    concept_id: Optional[uuid.UUID] = None,
    style: str = "illustration",
    preview_path: Optional[str] = None,
    master_path: Optional[str] = None,
    width: int = 1024,
    height: int = 1024,
    file_size_bytes: int = 0,
    generation_provider: str = "stub",
    generation_model: str = "stub-model",
    generation_cost_usd: float = 0.0,
    quality_score: Optional[float] = None,
) -> Design:
    design = Design(
        title=title,
        concept_id=concept_id,
        style=style,
        status=DesignStatus.DRAFT.value,
        file_path=file_path,
        preview_path=preview_path,
        master_path=master_path or file_path,
        width=width,
        height=height,
        file_size_bytes=file_size_bytes,
        generation_provider=generation_provider,
        generation_model=generation_model,
        generation_cost_usd=generation_cost_usd,
        quality_score=quality_score,
        version_number=1,
        is_master=True,
    )
    db.add(design)
    await db.flush()

    # Initial version record
    version = DesignVersion(
        design_id=design.id,
        version_number=1,
        file_path=file_path,
        changes_description="Initial generation",
        quality_score=quality_score,
    )
    db.add(version)

    # Initial master asset record
    asset = Asset(
        design_id=design.id,
        asset_type=AssetType.MASTER.value,
        file_path=file_path,
        file_name=file_path.split("/")[-1].split("\\")[-1],
        mime_type="image/png",
        file_size_bytes=file_size_bytes,
        width=width,
        height=height,
        is_transparent=True,
    )
    db.add(asset)

    await db.flush()
    await db.refresh(design)
    return design


async def update_design_status(
    db: AsyncSession,
    design_id: uuid.UUID,
    status: str,
) -> Optional[Design]:
    design = await get_design_by_id(db, design_id)
    if not design:
        return None
    design.status = status
    await db.flush()
    await db.refresh(design)
    return design


async def delete_design(
    db: AsyncSession,
    design_id: uuid.UUID,
) -> bool:
    design = await get_design_by_id(db, design_id)
    if not design:
        return False

    # Delete physical files
    if design.file_path:
        storage_service.delete_file(design.file_path)
    if design.preview_path:
        storage_service.delete_file(design.preview_path)
    if design.master_path and design.master_path != design.file_path:
        storage_service.delete_file(design.master_path)

    await db.delete(design)
    await db.flush()
    return True
