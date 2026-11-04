# TeeDesign AI — Architecture & Multi-Agent Specifications

## 1. System Philosophy

TeeDesign AI is an autonomous merchandise illustration studio designed around four core design principles:
1. **Decoupled Autonomous Agents**: Every agent operates as an isolated unit with its own system prompt, structured input/output contract, error boundaries, and token expense tracker.
2. **Deterministic State Transitions via LangGraph**: Workflow states are recorded as typed dictionaries and passed through cyclical directed acyclic graphs (DAGs) with explicit approval, retry, and rejection nodes.
3. **Provider-Agnostic Execution**: Image generation and LLM reasoning run behind abstracted adapter interfaces (`BaseImageProvider`, `BaseAgent`), enabling effortless switching between OpenAI, Replicate, Anthropic, and local PIL stub engines.
4. **Data Integrity & Non-Fabrication**: Production metrics, image resolutions, blur metrics, and costs are derived directly from actual runtime records and database queries.

---

## 2. LangGraph Production Graph

The production workflow executes the following state transitions:

```
[START]
   │
   ▼
[research_node]  ──► Scout analyzes niche demand & competition
   │
   ▼
[creative_node]  ──► DaVinci develops concepts, prompts & palettes
   │
   ▼
[generate_node]  ──► Generator calls active provider (Flux / DALL-E / Stub)
   │
   ▼
[quality_node]   ──► Sentinel runs 5-factor weighted visual QA & blur test
   │
   ├────────► Score < Threshold (e.g. 70%) & retries < max: [generate_node] (RETRY)
   ├────────► Score < Threshold & retries >= max: [reject_node] ──► [END]
   │
   ▼ Score >= Threshold (APPROVED)
[compliance_node]──► Flags protected IP, characters, and trademarks
   │
   ▼
[seo_node]       ──► Keywordsmith generates 60-char title, tags & description
   │
   ▼
[portfolio_node] ──► Prepares transparent 5000x5500 PNG master & preview thumbnail
   │
   ▼
[complete_node]  ──► Telemetry recorded, CEO receives completion report
   │
   ▼
 [END]
```

---

## 3. Image Processing Engine Pipeline

Merchandise illustrations for TeePublic have strict technical requirements:
- Minimum resolution: 1000px, target print canvas: **5000x5500 pixels at 300 DPI**.
- **Transparent background**: True alpha channel without haloing or opaque white boxes.
- **Never stretch small images**: Centered on transparent canvas without upscaling artifacts.
- **Master file preservation**: Master outputs are saved with unique UUIDs and preserved immutably.

### Image Processing Steps:
1. `validate_dimensions()`: Verifies image size, aspect ratio, and file size.
2. `validate_transparency()`: Checks RGBA alpha channel array for transparency values.
3. `detect_blur()`: Uses OpenCV Laplacian variance ($threshold = 100$) or PIL edge variance fallback.
4. `create_preview()`: Generates optimized thumbnail previews with white backing for web display.
5. `prepare_export()`: Centers artwork on a $5000 \times 5500$ transparent canvas with aspect-ratio preservation.

---

## 4. Database Schema (17 Models)

The PostgreSQL database stores all aspects of the studio operation:
- **User**: Authentication, roles, password hashes.
- **Agent**: Agent identity, status, task counters, avatar configurations.
- **AgentLog**: Chronological execution logs with severity levels and metadata.
- **WorkflowExecution**: Multi-step LangGraph workflow progress and tracking.
- **Task**: Granular agent tasks, inputs, outputs, and token/cost tallies.
- **Niche**: Market niches, target audiences, opportunity scores.
- **ResearchReport**: Public market evidence, search trends, and competition levels.
- **DesignConcept**: Creative Director proposals, prompt blueprints, color palettes.
- **Design**: Generated artwork records, file paths, dimensions, and approval states.
- **QualityReview**: 5-point weighted scores, blur scores, and inspector critique.
- **ComplianceReview**: IP risk flags, copyright warnings, clearance determinations.
- **Listing**: TeePublic listing metadata (titles, descriptions, tags, categories).
- **Asset**: Previews, masters, transparent PNG exports.
- **CostRecord**: Itemized API bills, provider usage, and token expenses.
- **PerformanceMetric**: Latencies, acceptance rates, and daily burn rates.
- **SystemSettings**: Centralized key-value configurations and safety limits.
- **RevokedToken**: JWT token blacklisting.
