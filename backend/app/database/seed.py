"""
TeeDesign AI — Database Seed Script
Idempotent — safe to run multiple times.
"""
import asyncio
import uuid
from datetime import datetime, timezone

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base import AsyncSessionLocal
from app.core.config import settings
from app.core.security import hash_password
from app.models.user import User
from app.models.agent import Agent
from app.models.niche import Niche
from app.models.settings import SystemSettings

log = structlog.get_logger(__name__)


AGENTS_DATA = [
    {
        "name": "CEO Orchestrator",
        "role": "Chief Executive AI",
        "description": "Coordinates all AI agents, assigns tasks, monitors workflows, enforces budget limits, and produces daily operational summaries.",
        "avatar_config": {"type": "sphere", "color": "#F59E0B", "size": 1.4, "rings": True},
    },
    {
        "name": "Market Research Agent",
        "role": "Market Research Specialist",
        "description": "Identifies promising illustration niches, analyzes customer interests, detects seasonal opportunities, and proposes creative opportunities.",
        "avatar_config": {"type": "book", "color": "#3B82F6", "size": 1.0},
    },
    {
        "name": "Creative Director",
        "role": "Creative Director AI",
        "description": "Develops original design concepts, defines illustration styles, chooses color palettes, and creates image-generation prompts.",
        "avatar_config": {"type": "crystal", "color": "#7C3AED", "size": 1.0},
    },
    {
        "name": "Illustration Generator",
        "role": "AI Illustration Engine",
        "description": "Generates original illustrations using configured image generation APIs. Saves files, maintains version history, and tracks generation costs.",
        "avatar_config": {"type": "gear", "color": "#06B6D4", "size": 1.0},
    },
    {
        "name": "Quality Control Agent",
        "role": "Quality Inspector AI",
        "description": "Inspects image quality, detects blur, evaluates composition, validates dimensions, and assigns quality scores across 5 weighted categories.",
        "avatar_config": {"type": "shield", "color": "#10B981", "size": 1.0},
    },
    {
        "name": "Copyright Compliance Agent",
        "role": "IP Compliance Specialist",
        "description": "Screens for recognizable protected characters, flags brand logos and trademarks, and maintains review records. Does not guarantee legal clearance.",
        "avatar_config": {"type": "lock", "color": "#F59E0B", "size": 1.0},
    },
    {
        "name": "SEO Specialist",
        "role": "SEO & Listing Optimizer",
        "description": "Generates optimized product titles, natural descriptions, and relevant tags. Avoids keyword stuffing and unauthorized trademarks.",
        "avatar_config": {"type": "search", "color": "#EC4899", "size": 1.0},
    },
    {
        "name": "Portfolio Manager",
        "role": "Portfolio & Asset Manager",
        "description": "Organizes artwork into collections, tracks design versions, manages approval status, prepares export packages, and detects duplicates.",
        "avatar_config": {"type": "folder", "color": "#8B5CF6", "size": 1.0},
    },
    {
        "name": "Analytics Agent",
        "role": "Data Analytics Specialist",
        "description": "Monitors production statistics, analyzes design quality trends, tracks AI expenses, and provides data-driven recommendations.",
        "avatar_config": {"type": "chart", "color": "#F97316", "size": 1.0},
    },
]

NICHES_DATA = [
    {"name": "Space & Astronomy", "description": "Cosmic art featuring planets, stars, galaxies, astronauts, and space exploration themes.", "target_audience": "Science enthusiasts, students, dreamers", "competition_level": "medium", "opportunity_score": 78.5, "keywords": ["space", "galaxy", "astronaut", "cosmic", "stars", "universe"]},
    {"name": "Cute Animals", "description": "Adorable animal illustrations with kawaii aesthetic — cats, dogs, bunnies, foxes.", "target_audience": "Animal lovers, children, gift buyers", "competition_level": "high", "opportunity_score": 65.0, "keywords": ["cute", "kawaii", "cat", "dog", "animal", "adorable"]},
    {"name": "Retro Gaming", "description": "Pixel art and retro gaming nostalgia — 8-bit characters, classic consoles, retro aesthetics.", "target_audience": "Gamers aged 25-45, nostalgia seekers", "competition_level": "high", "opportunity_score": 70.0, "keywords": ["retro", "gaming", "pixel art", "8-bit", "vintage", "arcade"]},
    {"name": "Botanical Art", "description": "Detailed botanical illustrations — tropical plants, succulents, wildflowers, herbal motifs.", "target_audience": "Plant lovers, home decorators, nature enthusiasts", "competition_level": "medium", "opportunity_score": 82.0, "keywords": ["botanical", "plants", "floral", "tropical", "succulent", "wildflower"]},
    {"name": "Ocean Life", "description": "Marine-themed artwork — sea creatures, coral reefs, waves, nautical elements.", "target_audience": "Beach lovers, environmentalists, divers", "competition_level": "medium", "opportunity_score": 75.0, "keywords": ["ocean", "whale", "fish", "coral", "nautical", "marine"]},
]

SETTINGS_DATA = [
    {"key": "min_quality_score", "value": 70.0, "description": "Minimum quality score (0-100) required for design approval", "category": "quality"},
    {"key": "max_retries_per_design", "value": 3, "description": "Maximum number of generation retry attempts per design", "category": "workflow"},
    {"key": "max_daily_spend_usd", "value": 50.0, "description": "Maximum daily spending limit in USD", "category": "costs"},
    {"key": "max_monthly_spend_usd", "value": 500.0, "description": "Maximum monthly spending limit in USD", "category": "costs"},
    {"key": "image_provider", "value": "stub", "description": "Active image generation provider: openai | replicate | stub", "category": "providers"},
    {"key": "llm_provider", "value": "stub", "description": "Active LLM provider: openai | anthropic | stub", "category": "providers"},
    {"key": "export_width", "value": 5000, "description": "Export image width in pixels", "category": "image_processing"},
    {"key": "export_height", "value": 5500, "description": "Export image height in pixels", "category": "image_processing"},
    {"key": "autonomous_mode", "value": False, "description": "Enable fully autonomous production mode", "category": "workflow"},
    {"key": "auto_approve_threshold", "value": 85.0, "description": "Quality score above which designs are auto-approved", "category": "quality"},
]


async def seed_all():
    """Run all seed functions."""
    async with AsyncSessionLocal() as session:
        await seed_admin_user(session)
        await seed_agents(session)
        await seed_niches(session)
        await seed_settings(session)
        await session.commit()
    log.info("✅ Database seeding complete")


async def seed_admin_user(session: AsyncSession):
    result = await session.execute(select(User).where(User.email == settings.ADMIN_EMAIL))
    if result.scalar_one_or_none():
        return
    admin = User(
        id=uuid.uuid4(),
        email=settings.ADMIN_EMAIL,
        username=settings.ADMIN_USERNAME,
        hashed_password=hash_password(settings.ADMIN_PASSWORD),
        is_active=True,
        is_admin=True,
        full_name="Admin",
    )
    session.add(admin)
    log.info("🌱 Admin user seeded", email=settings.ADMIN_EMAIL)


async def seed_agents(session: AsyncSession):
    result = await session.execute(select(Agent))
    existing = result.scalars().all()
    if existing:
        return
    for data in AGENTS_DATA:
        agent = Agent(
            id=uuid.uuid4(),
            name=data["name"],
            role=data["role"],
            description=data["description"],
            avatar_config=data.get("avatar_config"),
            last_activity=datetime.now(timezone.utc),
        )
        session.add(agent)
    log.info("🌱 Agents seeded", count=len(AGENTS_DATA))


async def seed_niches(session: AsyncSession):
    result = await session.execute(select(Niche))
    existing = result.scalars().all()
    if existing:
        return
    for data in NICHES_DATA:
        niche = Niche(id=uuid.uuid4(), **data)
        session.add(niche)
    log.info("🌱 Niches seeded", count=len(NICHES_DATA))


async def seed_settings(session: AsyncSession):
    result = await session.execute(select(SystemSettings))
    existing = result.scalars().all()
    if existing:
        return
    for data in SETTINGS_DATA:
        setting = SystemSettings(id=uuid.uuid4(), **data)
        session.add(setting)
    log.info("🌱 System settings seeded", count=len(SETTINGS_DATA))


if __name__ == "__main__":
    asyncio.run(seed_all())
