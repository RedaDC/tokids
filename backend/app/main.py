"""
TeeDesign AI — FastAPI Application Entry Point
"""
import asyncio
import logging
from contextlib import asynccontextmanager
from pathlib import Path

import structlog
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import settings

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.dev.ConsoleRenderer() if settings.DEBUG else structlog.processors.JSONRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

log = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup + shutdown."""
    # ── Startup ──────────────────────────────────────────────
    log.info("🚀 TeeDesign AI starting up...", version=settings.APP_VERSION)

    # Ensure storage directories exist
    for path_str in [
        settings.MASTER_FILES_PATH,
        settings.APPROVED_FILES_PATH,
        settings.PREVIEWS_PATH,
        settings.EXPORTS_PATH,
    ]:
        Path(path_str).mkdir(parents=True, exist_ok=True)

    # Initialize DB and seed data
    try:
        from app.database.base import init_db
        from app.database.seed import seed_all
        await init_db()
        await seed_all()
        log.info("✅ Database initialized and seeded")
    except Exception as e:
        log.warning("⚠️  Database init failed (may need migrations)", error=str(e))

    log.info(
        "✅ TeeDesign AI ready",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        stub_mode=settings.is_stub_mode,
        image_provider=settings.IMAGE_PROVIDER,
    )

    yield

    # ── Shutdown ─────────────────────────────────────────────
    log.info("👋 TeeDesign AI shutting down...")


# ─── FastAPI App ──────────────────────────────────────────────────────────────
app = FastAPI(
    title="TeeDesign AI",
    description="Autonomous AI-powered illustration studio for TeePublic merchandise",
    version=settings.APP_VERSION,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)

# ─── Middleware ───────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)


# ─── Health Check ─────────────────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
async def health_check():
    """System health check endpoint."""
    from datetime import datetime, timezone

    health = {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "environment": settings.APP_ENV,
        "stub_mode": settings.is_stub_mode,
        "services": {},
    }

    # Check database
    try:
        from app.database.base import engine
        async with engine.connect() as conn:
            await conn.execute(__import__("sqlalchemy").text("SELECT 1"))
        health["services"]["database"] = "healthy"
    except Exception as e:
        health["services"]["database"] = f"unhealthy: {str(e)}"
        health["status"] = "degraded"

    # Check Redis
    try:
        import redis.asyncio as aioredis
        r = aioredis.from_url(settings.REDIS_URL)
        await r.ping()
        await r.aclose()
        health["services"]["redis"] = "healthy"
    except Exception as e:
        health["services"]["redis"] = f"unavailable: {str(e)}"

    health["services"]["image_provider"] = settings.IMAGE_PROVIDER
    health["services"]["llm_provider"] = settings.LLM_PROVIDER

    return health


# ─── API Routers ──────────────────────────────────────────────────────────────
try:
    from app.api.auth import router as auth_router
    from app.api.agents import router as agents_router
    from app.api.workflows import router as workflows_router
    from app.api.research import router as research_router
    from app.api.designs import router as designs_router
    from app.api.quality import router as quality_router
    from app.api.seo import router as seo_router
    from app.api.analytics import router as analytics_router
    from app.api.settings import router as settings_router

    app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
    app.include_router(agents_router, prefix="/api/agents", tags=["Agents"])
    app.include_router(workflows_router, prefix="/api/workflows", tags=["Workflows"])
    app.include_router(research_router, prefix="/api/research", tags=["Research"])
    app.include_router(designs_router, prefix="/api/designs", tags=["Designs"])
    app.include_router(quality_router, prefix="/api/quality", tags=["Quality"])
    app.include_router(seo_router, prefix="/api/seo", tags=["SEO"])
    app.include_router(analytics_router, prefix="/api/analytics", tags=["Analytics"])
    app.include_router(settings_router, prefix="/api/settings", tags=["Settings"])
except ImportError as e:
    log.warning("Some routers could not be loaded", error=str(e))


# ─── Static Files (assets) ────────────────────────────────────────────────────
assets_path = Path(settings.STORAGE_PATH)
if assets_path.exists():
    app.mount("/assets", StaticFiles(directory=str(assets_path)), name="assets")


# ─── Global Exception Handler ─────────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    log.error("Unhandled exception", path=request.url.path, error=str(exc), exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error", "type": type(exc).__name__},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.DEBUG,
        log_level="debug" if settings.DEBUG else "info",
    )
