# TeeDesign AI — Autonomous AI Merchandise Illustration Studio

> **Production-grade multi-agent AI business platform engineered for autonomous merchandise artwork creation, quality inspection, IP compliance screening, and marketplace listing generation on TeePublic.**

---

## 🚀 Key Highlights & Capabilities

- **Autonomous Multi-Agent Workforce**: 9 specialized AI agents (CEO Orchestrator, Market Research, Creative Director, Illustration Generator, Quality Control, Copyright Compliance, SEO Specialist, Portfolio Manager, Analytics).
- **LangGraph State Graph Workflow**: Stateful, cyclical graph with automated retry policies, quality gates, conditional review branching, and non-blocking recovery.
- **Provider-Independent Image Architecture**: Pluggable interface supporting **Flux 1.1 Pro (Replicate)**, **OpenAI DALL-E 3**, and **Pillow Stub Engine** with dynamic runtime fallback when API keys are not supplied.
- **5-Point Weighted Quality Evaluation**:
  - Visual Quality: 25% (edge sharpness, resolution, 300 DPI compliance)
  - Originality: 25% (creative uniqueness, character design)
  - Composition: 20% (garment center placement, focal balance)
  - Print Suitability: 20% (alpha channel transparency, contrast)
  - Niche Relevance: 10% (consumer demographic alignment)
- **Copyright & Trademark Guardrails**: Automated prompt and concept inspection for trademarked characters, living artist imitation, and intellectual property flags.
- **Automated Merchandise SEO**: 60-character natural titles, consumer descriptions, high-volume apparel tags, and direct TeePublic JSON metadata export.
- **3D Workforce Command Center**: Interactive Three.js / React Three Fiber visual workplace rendered in Next.js 14, dark-navy glassmorphic UI, real-time telemetry, and Recharts analytics.
- **Full-Stack Containerization**: One-command launch via `docker-compose.yml` orchestrating PostgreSQL, Redis, Celery workers/beat, FastAPI, and Next.js.

---

## 🏛️ System Architecture

```
                               ┌────────────────────────────────┐
                               │       COMMAND CENTER           │
                               │   Next.js 14 + Three.js UI     │
                               └──────────────┬─────────────────┘
                                              │ REST / JSON
                                              ▼
                               ┌────────────────────────────────┐
                               │       FastAPI BACKEND          │
                               │  Async SQLAlchemy + Pydantic   │
                               └──────────────┬─────────────────┘
                                              │
                      ┌───────────────────────┴───────────────────────┐
                      ▼                                               ▼
         ┌──────────────────────────┐                    ┌─────────────────────────┐
         │     LANGGRAPH ENGINE     │                    │     CELERY + REDIS      │
         │  StateGraph Orchestration│                    │ Background Distribution │
         └────────────┬─────────────┘                    └────────────┬────────────┘
                      │                                               │
    ┌─────────────────┴─────────────────┐                             │
    │  AGENT 1: CEO Orchestrator        │                             │
    │  AGENT 2: Market Research         │                             │
    │  AGENT 3: Creative Director       │                             │
    │  AGENT 4: Illustration Generator  │◄────────────────────────────┘
    │  AGENT 5: Quality Control         │
    │  AGENT 6: Copyright Compliance    │
    │  AGENT 7: SEO Specialist          │
    │  AGENT 8: Portfolio Manager       │
    │  AGENT 9: Analytics               │
    └─────────────────┬─────────────────┘
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
┌───────────────┐           ┌───────────────┐
│  POSTGRESQL   │           │ ASSETS ENGINE │
│   DATABASE    │           │ (5000x5500 PNG│
│ (17 Tables)   │           │  Pillow/CV2)  │
└───────────────┘           └───────────────┘
```

---

## 📂 Project Structure

```
teedesign-ai/
├── docker-compose.yml            # Complete container stack
├── .env.example                  # Environment configuration template
├── README.md                     # System documentation
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── alembic.ini
│   ├── alembic/                  # Database migration versions
│   ├── app/
│   │   ├── main.py               # FastAPI application & router mounting
│   │   ├── core/                 # Config (pydantic-settings), JWT auth
│   │   ├── database/             # SQLAlchemy async engine & seeds
│   │   ├── models/               # 17 models (User, Agent, Design, etc.)
│   │   └── api/                  # 10 modular REST API endpoints
│   ├── agents/                   # All 9 multi-agent implementations
│   ├── workflows/                # LangGraph state graph production workflow
│   ├── image_processing/         # Pillow/OpenCV engine & providers (Flux, DALL-E, Stub)
│   ├── workers/                  # Celery worker & beat schedules
│   └── tests/                    # Pytest asynchronous test suite
│
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── tailwind.config.ts
│   ├── app/
│   │   ├── page.tsx              # 1. Command Center Dashboard
│   │   ├── workforce/page.tsx    # 2. AI Workforce (3D Office & Agent detail)
│   │   ├── studio/page.tsx       # 3. Creative Studio (Artwork generation)
│   │   ├── research/page.tsx     # 4. Market Research & Niche Discovery
│   │   ├── library/page.tsx      # 5. Design Library & Version History
│   │   ├── quality/page.tsx      # 6. Quality Control & IP Screening
│   │   ├── seo/page.tsx          # 7. SEO & Listing Manager
│   │   ├── analytics/page.tsx    # 8. Analytics & Telemetry
│   │   ├── costs/page.tsx        # 9. Cost Management & Budget Guardrails
│   │   └── settings/page.tsx     # 10. Settings & Policies
│   ├── components/               # 3D Office, GlassPanel, StatsCard, Modals
│   └── lib/                      # Typed Axios API client & mock fallbacks
│
└── assets/                       # File system storage (master, previews, exports)
```

---

## ⚡ Quickstart Guide

### 1. Prerequisites
- [Docker](https://www.docker.com/) & Docker Compose
- *Optional for local dev without Docker*: Node.js 18+, Python 3.11+

### 2. Configuration
Copy the sample environment file:
```bash
cp .env.example .env
```
Configure your API keys in `.env` (or run in `stub` mode for 100% zero-cost local testing):
```env
OPENAI_API_KEY=sk-...
REPLICATE_API_KEY=r8_...
IMAGE_PROVIDER=stub      # Change to 'replicate' or 'openai' when keys are added
LLM_PROVIDER=stub        # Change to 'openai' or 'anthropic' when keys are added
```

### 3. Launch via Docker Compose
```bash
docker-compose up --build
```

The stack will start:
- **Frontend Dashboard**: `http://localhost:3000`
- **FastAPI Backend**: `http://localhost:8000`
- **Interactive API Documentation (Swagger)**: `http://localhost:8000/docs`
- **PostgreSQL Database**: `localhost:5432`
- **Redis Broker**: `localhost:6379`
- **Celery Worker & Beat**: Concurrent asynchronous job processing

---

## 🧑‍💻 AI Workforce Roster

| Agent Name | Role | Responsibilities | Default Avatar |
| :--- | :--- | :--- | :--- |
| **CEO Orchestrator** | Chief Executive AI | Decomposes business goals, schedules batches, enforces daily spending caps. | Holographic Golden Core |
| **Market Research** | Market Research | Identifies high-velocity niches, analyzes buyer demographics & search trends. | Blue Knowledge Prism |
| **Creative Director** | Art Director | Synthesizes apparel prompts, colorways, and art direction (13+ supported styles). | Purple Crystal Sphere |
| **Illustration Generator** | Image Engine | Directs provider pipelines (Flux / DALL-E / Stub), manages master PNG retention. | Cyan Turbine |
| **Quality Control** | QA Inspector | 5-point weighted scoring (300 DPI, transparency, edge contrast, balance). | Emerald Guard Shield |
| **Copyright Compliance**| IP Specialist | Screens for trademarked characters, logo patterns, and copyright infringements. | Amber Padlock |
| **SEO Specialist** | Listing Optimizer | Crafts natural 60-char titles, descriptions, and 20 optimal tags for TeePublic. | Magenta Scanner |
| **Portfolio Manager** | Asset Custodian | Organizes catalog collections, versions, and transparent export archives. | Violet Workspace |
| **Analytics** | Data Scientist | Analyzes design throughput, pass rates, compute costs, and unit economics. | Coral Telemetry Beacon |

---

## 🛡️ Production & Legal Safeguards

1. **Master File Preservation**: Master generated files are stored immutably in `/assets/master/` and never overwritten.
2. **Transparent PNG Standards**: Artwork is processed through Pillow alpha channel isolation and centered on a 5000x5500 px canvas for direct-to-garment printing.
3. **Budget Hard-Cutoff**: Execution is monitored against the configured `MAX_DAILY_SPEND_USD` ceiling to prevent unintended API billing.
4. **Legal Disclaimer**: Automated copyright screening identifies known protected terms and artist styles, with explicit logging that automated reviews do not constitute final legal clearance.
