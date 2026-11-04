"""
TeeDesign AI — Designs API
"""
from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
import uuid

from app.api.deps import get_current_user, get_db
from app.models.design import Design, DesignConcept
from app.models.user import User
from app.models.analytics import CostRecord

router = APIRouter()


class GenerateDesignRequest(BaseModel):
    concept: str
    niche: str | None = "general"
    style: str = "minimalist"
    color_palette: str | None = None
    provider: str | None = None
    custom_instructions: str | None = None
    num_variations: int = 1


class DesignResponse(BaseModel):
    id: str
    title: str
    style: str
    status: str
    file_path: str | None
    preview_path: str | None
    width: int | None
    height: int | None
    file_size_bytes: int | None
    generation_provider: str | None
    generation_model: str | None
    generation_cost_usd: float
    quality_score: float | None
    is_stub: bool
    created_at: str
    updated_at: str


def _design_to_response(d: Design) -> DesignResponse:
    return DesignResponse(
        id=str(d.id),
        title=d.title,
        style=d.style,
        status=d.status,
        file_path=d.file_path,
        preview_path=d.preview_path,
        width=d.width,
        height=d.height,
        file_size_bytes=d.file_size_bytes,
        generation_provider=d.generation_provider,
        generation_model=d.generation_model,
        generation_cost_usd=d.generation_cost_usd,
        quality_score=d.quality_score,
        is_stub=d.is_stub,
        created_at=d.created_at.isoformat(),
        updated_at=d.updated_at.isoformat(),
    )


async def _run_generation(
    design_id: uuid.UUID,
    request: GenerateDesignRequest,
    db_session_factory: Any,
):
    """Background task: generate image and update DB."""
    from agents.agents import CreativeDirectorAgent, IllustrationGeneratorAgent, QualityControlAgent
    from app.database.base import AsyncSessionLocal

    async with AsyncSessionLocal() as db:
        # Update status to generating
        result = await db.execute(select(Design).where(Design.id == design_id))
        design = result.scalar_one_or_none()
        if not design:
            return

        design.status = "generating"
        await db.commit()

        try:
            # Build generation prompt
            if request.custom_instructions:
                prompt = request.custom_instructions
            else:
                # Use Creative Director to build prompt
                creative = CreativeDirectorAgent()
                creative_result = await creative.execute_with_tracking({
                    "niche": request.niche,
                    "style": request.style,
                    "concept": request.concept,
                })
                concepts = creative_result.output.get("concepts", [])
                prompt = concepts[0].get("generation_prompt", request.concept) if concepts else request.concept

            # Generate image
            generator = IllustrationGeneratorAgent()
            gen_result = await generator.execute_with_tracking({
                "generation_prompt": prompt,
                "title": request.concept,
                "num_variations": request.num_variations,
            })

            generated_list = gen_result.output.get("generated", [])
            if generated_list and "file_path" in generated_list[0]:
                g = generated_list[0]

                # Run quality check
                quality_agent = QualityControlAgent()
                quality_result = await quality_agent.execute_with_tracking({
                    "file_path": g["file_path"],
                    "niche": request.niche,
                })

                # Update design record
                result = await db.execute(select(Design).where(Design.id == design_id))
                design = result.scalar_one_or_none()
                if design:
                    design.file_path = g.get("file_path")
                    design.preview_path = g.get("preview_path")
                    design.master_path = g.get("file_path")
                    design.width = g.get("width", 1024)
                    design.height = g.get("height", 1024)
                    design.generation_provider = g.get("provider", "stub")
                    design.generation_model = g.get("model", "stub")
                    design.generation_cost_usd = g.get("cost_usd", 0.0)
                    design.generation_prompt = prompt
                    design.quality_score = quality_result.output.get("overall_score")
                    design.is_stub = g.get("is_stub", True)
                    design.status = "approved" if quality_result.output.get("is_approved") else "draft"
                    if design.preview_path:
                        try:
                            size = os.path.getsize(design.file_path)
                            design.file_size_bytes = size
                        except Exception:
                            pass
                    await db.commit()

                    # Record cost
                    if g.get("cost_usd", 0) > 0:
                        cost_record = CostRecord(
                            id=uuid.uuid4(),
                            service_type="image_generation",
                            provider=g.get("provider", "unknown"),
                            model=g.get("model", "unknown"),
                            images_generated=1,
                            cost_usd=g.get("cost_usd", 0),
                        )
                        db.add(cost_record)
                        await db.commit()
            else:
                result = await db.execute(select(Design).where(Design.id == design_id))
                design = result.scalar_one_or_none()
                if design:
                    design.status = "failed"
                    await db.commit()

        except Exception as e:
            result = await db.execute(select(Design).where(Design.id == design_id))
            design = result.scalar_one_or_none()
            if design:
                design.status = "failed"
                await db.commit()


@router.post("/generate", response_model=DesignResponse, status_code=202)
async def generate_design(
    request: GenerateDesignRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Start design generation (async background task)."""
    design_id = uuid.uuid4()
    design = Design(
        id=design_id,
        title=request.concept[:255],
        style=request.style,
        status="queued",
        is_stub=False,
        generation_cost_usd=0.0,
    )
    db.add(design)
    await db.commit()
    await db.refresh(design)

    background_tasks.add_task(_run_generation, design_id, request, None)

    return _design_to_response(design)


@router.get("", response_model=list[DesignResponse])
async def list_designs(
    status: str | None = None,
    style: str | None = None,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = select(Design).order_by(desc(Design.created_at)).limit(limit).offset(offset)
    if status:
        query = query.where(Design.status == status)
    if style:
        query = query.where(Design.style == style)
    result = await db.execute(query)
    designs = result.scalars().all()
    return [_design_to_response(d) for d in designs]


@router.get("/{design_id}", response_model=DesignResponse)
async def get_design(
    design_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Design).where(Design.id == uuid.UUID(design_id)))
    design = result.scalar_one_or_none()
    if not design:
        raise HTTPException(status_code=404, detail="Design not found")
    return _design_to_response(design)


@router.delete("/{design_id}", status_code=204)
async def delete_design(
    design_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Design).where(Design.id == uuid.UUID(design_id)))
    design = result.scalar_one_or_none()
    if not design:
        raise HTTPException(status_code=404, detail="Design not found")
    await db.delete(design)
    await db.commit()


@router.get("/{design_id}/download")
async def download_design(
    design_id: str,
    file_type: str = "master",
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Design).where(Design.id == uuid.UUID(design_id)))
    design = result.scalar_one_or_none()
    if not design:
        raise HTTPException(status_code=404, detail="Design not found")

    file_path = design.file_path if file_type == "master" else design.preview_path
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found on disk")

    return FileResponse(
        path=file_path,
        filename=f"{design.title[:50].replace(' ', '_')}.png",
        media_type="image/png",
    )
