"""
TeeDesign AI — Workflows, Research, Quality, SEO, Settings APIs
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.models.task import WorkflowExecution, Task
from app.models.niche import Niche, ResearchReport
from app.models.quality import QualityReview, ComplianceReview
from app.models.listing import Listing
from app.models.design import Design
from app.models.settings import SystemSettings

# ─── Workflows ────────────────────────────────────────────────────────────────
workflows_router = APIRouter()


class WorkflowStartRequest(BaseModel):
    niche: str
    style: str = "minimalist"
    custom_instructions: str | None = None
    num_designs: int = 1


class WorkflowResponse(BaseModel):
    id: str
    name: str
    status: str
    current_step: str | None
    total_steps: int
    completed_steps: int
    total_cost_usd: float
    started_at: str | None
    completed_at: str | None


def _wf_to_resp(wf: WorkflowExecution) -> WorkflowResponse:
    return WorkflowResponse(
        id=str(wf.id),
        name=wf.name,
        status=wf.status,
        current_step=wf.current_step,
        total_steps=wf.total_steps or 8,
        completed_steps=wf.completed_steps or 0,
        total_cost_usd=wf.total_cost_usd or 0.0,
        started_at=wf.started_at.isoformat() if wf.started_at else None,
        completed_at=wf.completed_at.isoformat() if wf.completed_at else None,
    )


@workflows_router.post("/start", response_model=WorkflowResponse, status_code=202)
async def start_workflow(
    request: WorkflowStartRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    wf = WorkflowExecution(
        id=uuid.uuid4(),
        name=f"Production: {request.niche}",
        status="running",
        current_step="research",
        total_steps=8,
        completed_steps=0,
        started_at=datetime.now(timezone.utc),
        input_data={"niche": request.niche, "style": request.style},
    )
    db.add(wf)
    await db.commit()
    await db.refresh(wf)

    # Start async
    from workflows.production_workflow import ProductionWorkflow
    workflow = ProductionWorkflow()
    import asyncio
    asyncio.create_task(workflow.execute_step({
        "workflow_id": str(wf.id),
        "niche": request.niche,
        "style": request.style,
        "custom_instructions": request.custom_instructions or "",
    }))

    return _wf_to_resp(wf)


@workflows_router.get("", response_model=list[WorkflowResponse])
async def list_workflows(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(WorkflowExecution).order_by(desc(WorkflowExecution.created_at)).limit(50))
    return [_wf_to_resp(wf) for wf in result.scalars().all()]


@workflows_router.get("/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow(
    workflow_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(WorkflowExecution).where(WorkflowExecution.id == uuid.UUID(workflow_id)))
    wf = result.scalar_one_or_none()
    if not wf:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return _wf_to_resp(wf)


@workflows_router.post("/{workflow_id}/cancel")
async def cancel_workflow(
    workflow_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(WorkflowExecution).where(WorkflowExecution.id == uuid.UUID(workflow_id)))
    wf = result.scalar_one_or_none()
    if not wf:
        raise HTTPException(status_code=404, detail="Workflow not found")
    wf.status = "cancelled"
    wf.completed_at = datetime.now(timezone.utc)
    await db.commit()
    return {"message": "Workflow cancelled"}


# ─── Research ─────────────────────────────────────────────────────────────────
research_router = APIRouter()


class ResearchStartRequest(BaseModel):
    query: str
    num_niches: int = 3


@research_router.post("/start")
async def start_research(
    request: ResearchStartRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from agents.agents import ResearchAgent
    agent = ResearchAgent()
    result = await agent.execute_with_tracking({
        "query": request.query,
        "num_niches": request.num_niches,
    })

    # Save niches and reports to DB
    created_niches = []
    for niche_data in result.output.get("niches", []):
        # Upsert niche
        existing = await db.execute(select(Niche).where(Niche.name == niche_data["name"]))
        niche = existing.scalar_one_or_none()
        if not niche:
            niche = Niche(
                id=uuid.uuid4(),
                name=niche_data["name"],
                target_audience=niche_data.get("target_audience", ""),
                competition_level=niche_data.get("competition_level", "medium"),
                opportunity_score=niche_data.get("confidence_score", 50.0),
                keywords=niche_data.get("keywords", []),
                is_seasonal=niche_data.get("is_seasonal", False),
                season=niche_data.get("season"),
            )
            db.add(niche)
            await db.flush()

        # Save research report
        report = ResearchReport(
            id=uuid.uuid4(),
            niche_id=niche.id,
            summary=niche_data.get("evidence", ""),
            evidence=niche_data.get("evidence", ""),
            competition_assessment=niche_data.get("competition_level", ""),
            creative_opportunity=niche_data.get("creative_opportunity", ""),
            confidence_score=niche_data.get("confidence_score", 50.0),
            is_stub=result.is_stub,
        )
        db.add(report)
        created_niches.append(niche_data["name"])

    await db.commit()
    return {
        "success": result.success,
        "niches_created": created_niches,
        "is_stub": result.is_stub,
        "data": result.output,
    }


@research_router.get("/reports")
async def get_research_reports(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(ResearchReport, Niche)
        .join(Niche, ResearchReport.niche_id == Niche.id)
        .order_by(desc(ResearchReport.created_at))
        .limit(50)
    )
    rows = result.all()
    return [
        {
            "id": str(r.id),
            "niche": n.name,
            "niche_id": str(n.id),
            "target_audience": n.target_audience,
            "competition_level": n.competition_level,
            "opportunity_score": n.opportunity_score,
            "summary": r.summary,
            "creative_opportunity": r.creative_opportunity,
            "confidence_score": r.confidence_score,
            "is_stub": r.is_stub,
            "created_at": r.created_at.isoformat(),
        }
        for r, n in rows
    ]


@research_router.get("/niches")
async def get_niches(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Niche).where(Niche.is_active == True).order_by(desc(Niche.opportunity_score)))
    niches = result.scalars().all()
    return [
        {
            "id": str(n.id),
            "name": n.name,
            "description": n.description,
            "target_audience": n.target_audience,
            "competition_level": n.competition_level,
            "opportunity_score": n.opportunity_score,
            "is_seasonal": n.is_seasonal,
            "season": n.season,
            "keywords": n.keywords,
        }
        for n in niches
    ]


# ─── Quality ──────────────────────────────────────────────────────────────────
quality_router = APIRouter()


@quality_router.post("/evaluate/{design_id}")
async def evaluate_quality(
    design_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from agents.agents import QualityControlAgent, ComplianceAgent

    result = await db.execute(select(Design).where(Design.id == uuid.UUID(design_id)))
    design = result.scalar_one_or_none()
    if not design:
        raise HTTPException(status_code=404, detail="Design not found")
    if not design.file_path:
        raise HTTPException(status_code=400, detail="Design has no generated file")

    # Quality
    qa = QualityControlAgent()
    q_result = await qa.execute_with_tracking({
        "file_path": design.file_path,
        "niche": "general",
    })

    review = QualityReview(
        id=uuid.uuid4(),
        design_id=design.id,
        overall_score=q_result.output.get("overall_score", 0),
        visual_quality_score=q_result.output.get("visual_quality_score", 0),
        originality_score=q_result.output.get("originality_score", 0),
        composition_score=q_result.output.get("composition_score", 0),
        print_suitability_score=q_result.output.get("print_suitability_score", 0),
        niche_relevance_score=q_result.output.get("niche_relevance_score", 0),
        is_approved=q_result.output.get("is_approved", False),
        rejection_reason=q_result.output.get("rejection_reason"),
        notes=q_result.output.get("notes", ""),
        is_stub=q_result.is_stub,
    )
    db.add(review)

    # Compliance
    ca = ComplianceAgent()
    c_result = await ca.execute_with_tracking({
        "generation_prompt": design.generation_prompt or "",
    })
    comp_review = ComplianceReview(
        id=uuid.uuid4(),
        design_id=design.id,
        risk_level=c_result.output.get("risk_level", "low"),
        flags=c_result.output.get("flags", []),
        is_cleared=c_result.output.get("is_cleared", True),
        review_notes=c_result.output.get("review_notes", ""),
        is_stub=c_result.is_stub,
    )
    db.add(comp_review)

    # Update design quality score
    design.quality_score = q_result.output.get("overall_score", 0)
    if q_result.output.get("is_approved") and c_result.output.get("is_cleared"):
        design.status = "approved"

    await db.commit()
    return {
        "quality": q_result.output,
        "compliance": c_result.output,
        "design_status": design.status,
    }


@quality_router.get("/reviews")
async def get_quality_reviews(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(QualityReview).order_by(desc(QualityReview.created_at)).limit(50)
    )
    reviews = result.scalars().all()
    return [
        {
            "id": str(r.id),
            "design_id": str(r.design_id),
            "overall_score": r.overall_score,
            "visual_quality_score": r.visual_quality_score,
            "originality_score": r.originality_score,
            "composition_score": r.composition_score,
            "print_suitability_score": r.print_suitability_score,
            "niche_relevance_score": r.niche_relevance_score,
            "is_approved": r.is_approved,
            "rejection_reason": r.rejection_reason,
            "is_stub": r.is_stub,
            "created_at": r.created_at.isoformat(),
        }
        for r in reviews
    ]


# ─── SEO ──────────────────────────────────────────────────────────────────────
seo_router = APIRouter()


class ListingUpdateRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    primary_keyword: str | None = None
    tags: list[str] | None = None
    category: str | None = None


@seo_router.post("/generate/{design_id}")
async def generate_seo(
    design_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from agents.agents import SEOAgent

    result = await db.execute(select(Design).where(Design.id == uuid.UUID(design_id)))
    design = result.scalar_one_or_none()
    if not design:
        raise HTTPException(status_code=404, detail="Design not found")

    seo = SEOAgent()
    seo_result = await seo.execute_with_tracking({
        "title": design.title,
        "description": "",
        "niche": "general",
        "style": design.style,
    })

    # Upsert listing
    existing = await db.execute(select(Listing).where(Listing.design_id == design.id))
    listing = existing.scalar_one_or_none()

    seo_data = seo_result.output
    if not listing:
        listing = Listing(
            id=uuid.uuid4(),
            design_id=design.id,
            title=seo_data.get("title", design.title)[:200],
            description=seo_data.get("description", ""),
            primary_keyword=seo_data.get("primary_keyword", ""),
            tags=seo_data.get("tags", []),
            category=seo_data.get("category", ""),
            status="ready",
            is_stub=seo_result.is_stub,
        )
        db.add(listing)
    else:
        listing.title = seo_data.get("title", listing.title)[:200]
        listing.description = seo_data.get("description", listing.description)
        listing.primary_keyword = seo_data.get("primary_keyword", listing.primary_keyword)
        listing.tags = seo_data.get("tags", listing.tags)
        listing.category = seo_data.get("category", listing.category)

    await db.commit()
    await db.refresh(listing)
    return {"listing_id": str(listing.id), "seo_data": seo_data, "is_stub": seo_result.is_stub}


@seo_router.get("/listings")
async def get_listings(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Listing, Design)
        .join(Design, Listing.design_id == Design.id)
        .order_by(desc(Listing.created_at))
        .limit(50)
    )
    rows = result.all()
    return [
        {
            "id": str(l.id),
            "design_id": str(l.design_id),
            "design_title": d.title,
            "title": l.title,
            "description": l.description,
            "primary_keyword": l.primary_keyword,
            "tags": l.tags,
            "category": l.category,
            "status": l.status,
            "is_stub": l.is_stub,
            "created_at": l.created_at.isoformat(),
        }
        for l, d in rows
    ]


@seo_router.put("/listings/{listing_id}")
async def update_listing(
    listing_id: str,
    update: ListingUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Listing).where(Listing.id == uuid.UUID(listing_id)))
    listing = result.scalar_one_or_none()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    if update.title:
        listing.title = update.title[:200]
    if update.description:
        listing.description = update.description
    if update.primary_keyword:
        listing.primary_keyword = update.primary_keyword
    if update.tags is not None:
        listing.tags = update.tags
    if update.category:
        listing.category = update.category

    await db.commit()
    return {"message": "Listing updated", "listing_id": listing_id}


# ─── Settings ─────────────────────────────────────────────────────────────────
settings_router = APIRouter()


@settings_router.get("")
async def get_settings(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(SystemSettings))
    settings = result.scalars().all()
    return [
        {
            "id": str(s.id),
            "key": s.key,
            "value": "***" if s.is_secret else s.value,
            "description": s.description,
            "category": s.category,
            "is_secret": s.is_secret,
        }
        for s in settings
    ]


class SettingsUpdateRequest(BaseModel):
    updates: dict


@settings_router.put("")
async def update_settings(
    request: SettingsUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updated = []
    for key, value in request.updates.items():
        result = await db.execute(select(SystemSettings).where(SystemSettings.key == key))
        setting = result.scalar_one_or_none()
        if setting:
            setting.value = value
            updated.append(key)
        else:
            new_setting = SystemSettings(id=uuid.uuid4(), key=key, value=value)
            db.add(new_setting)
            updated.append(key)
    await db.commit()
    return {"message": f"Updated {len(updated)} settings", "keys": updated}
