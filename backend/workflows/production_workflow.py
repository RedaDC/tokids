"""
TeeDesign AI — LangGraph Production Workflow
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, TypedDict

import structlog

log = structlog.get_logger(__name__)


class WorkflowState(TypedDict):
    """State passed through the LangGraph production workflow."""
    # Input
    task_id: str
    workflow_id: str
    concept: dict[str, Any]
    niche: str
    style: str
    custom_instructions: str

    # Agent results
    research_result: dict[str, Any]
    creative_result: dict[str, Any]
    generation_result: dict[str, Any]
    quality_result: dict[str, Any]
    compliance_result: dict[str, Any]
    seo_result: dict[str, Any]
    portfolio_result: dict[str, Any]

    # Control flow
    current_step: str
    retry_count: int
    max_retries: int
    total_cost_usd: float
    max_spend_usd: float
    errors: list[str]
    is_approved: bool
    is_complete: bool
    is_stub: bool


class ProductionWorkflow:
    """
    Full TeeDesign AI production workflow using LangGraph.
    
    Steps:
    1. Research → 2. Creative → 3. Generate → 4. Quality Check
    → 5. Compliance → 6. SEO → 7. Portfolio → 8. Analytics
    """

    def __init__(self):
        from app.core.config import settings
        self.max_retries = settings.MAX_RETRIES_PER_DESIGN
        self.max_spend = settings.MAX_DAILY_SPEND_USD
        self._graph = None

    def _build_graph(self):
        """Build LangGraph StateGraph for the production workflow."""
        try:
            from langgraph.graph import StateGraph, END

            graph = StateGraph(WorkflowState)

            # Add all nodes
            graph.add_node("research", self._research_node)
            graph.add_node("creative", self._creative_node)
            graph.add_node("generate", self._generate_node)
            graph.add_node("quality_check", self._quality_node)
            graph.add_node("compliance", self._compliance_node)
            graph.add_node("seo", self._seo_node)
            graph.add_node("portfolio", self._portfolio_node)
            graph.add_node("complete", self._complete_node)
            graph.add_node("reject", self._reject_node)

            # Entry
            graph.set_entry_point("research")

            # Linear flow
            graph.add_edge("research", "creative")
            graph.add_edge("creative", "generate")

            # Conditional: quality check → approve or retry/reject
            graph.add_conditional_edges(
                "quality_check",
                self._quality_decision,
                {
                    "approved": "compliance",
                    "retry": "generate",
                    "reject": "reject",
                },
            )
            graph.add_edge("generate", "quality_check")
            graph.add_edge("compliance", "seo")
            graph.add_edge("seo", "portfolio")
            graph.add_edge("portfolio", "complete")
            graph.add_edge("complete", END)
            graph.add_edge("reject", END)

            return graph.compile()

        except ImportError:
            log.warning("LangGraph not available, using sequential fallback")
            return None

    async def _research_node(self, state: WorkflowState) -> WorkflowState:
        from agents.agents import ResearchAgent
        agent = ResearchAgent()
        result = await agent.execute_with_tracking({"query": state.get("niche", "")})
        state["research_result"] = result.output
        state["total_cost_usd"] += result.cost_usd
        state["current_step"] = "creative"
        await self._update_db_status(state["workflow_id"], "research_complete", result.cost_usd)
        return state

    async def _creative_node(self, state: WorkflowState) -> WorkflowState:
        from agents.agents import CreativeDirectorAgent
        agent = CreativeDirectorAgent()
        result = await agent.execute_with_tracking({
            "niche": state.get("niche", ""),
            "style": state.get("style", ""),
        })
        state["creative_result"] = result.output
        state["total_cost_usd"] += result.cost_usd
        state["current_step"] = "generate"
        # Use first concept for generation
        concepts = result.output.get("concepts", [])
        if concepts:
            state["concept"] = concepts[0]
        await self._update_db_status(state["workflow_id"], "creative_complete", result.cost_usd)
        return state

    async def _generate_node(self, state: WorkflowState) -> WorkflowState:
        from agents.agents import IllustrationGeneratorAgent
        agent = IllustrationGeneratorAgent()

        concept = state.get("concept", {})
        result = await agent.execute_with_tracking({
            "generation_prompt": concept.get("generation_prompt", state.get("custom_instructions", "")),
            "title": concept.get("title", ""),
        })
        state["generation_result"] = result.output
        state["total_cost_usd"] += result.cost_usd
        state["is_stub"] = result.is_stub
        state["current_step"] = "quality_check"
        await self._update_db_status(state["workflow_id"], "generation_complete", result.cost_usd)
        return state

    async def _quality_node(self, state: WorkflowState) -> WorkflowState:
        from agents.agents import QualityControlAgent
        agent = QualityControlAgent()

        generated = state.get("generation_result", {}).get("generated", [])
        if not generated or "file_path" not in generated[0]:
            state["quality_result"] = {"is_approved": False, "overall_score": 0.0, "rejection_reason": "No generated file"}
            state["is_approved"] = False
            return state

        result = await agent.execute_with_tracking({
            "file_path": generated[0]["file_path"],
            "niche": state.get("niche", ""),
            "description": state.get("concept", {}).get("description", ""),
        })
        state["quality_result"] = result.output
        state["is_approved"] = result.output.get("is_approved", False)
        state["total_cost_usd"] += result.cost_usd
        state["current_step"] = "compliance" if state["is_approved"] else "retry_or_reject"
        await self._update_db_status(state["workflow_id"], "quality_complete", result.cost_usd)
        return state

    def _quality_decision(self, state: WorkflowState) -> str:
        """Decide whether to approve, retry, or reject after quality check."""
        if state.get("is_approved"):
            return "approved"
        retry_count = state.get("retry_count", 0)
        if retry_count < state.get("max_retries", self.max_retries):
            state["retry_count"] = retry_count + 1
            return "retry"
        return "reject"

    async def _compliance_node(self, state: WorkflowState) -> WorkflowState:
        from agents.agents import ComplianceAgent
        agent = ComplianceAgent()
        concept = state.get("concept", {})
        result = await agent.execute_with_tracking({
            "generation_prompt": concept.get("generation_prompt", ""),
            "description": concept.get("description", ""),
        })
        state["compliance_result"] = result.output
        state["current_step"] = "seo"
        # If high risk, block from queue
        if result.output.get("risk_level") == "critical":
            state["is_approved"] = False
        return state

    async def _seo_node(self, state: WorkflowState) -> WorkflowState:
        from agents.agents import SEOAgent
        agent = SEOAgent()
        concept = state.get("concept", {})
        result = await agent.execute_with_tracking({
            "title": concept.get("title", ""),
            "description": concept.get("description", ""),
            "niche": state.get("niche", ""),
            "style": concept.get("style", ""),
        })
        state["seo_result"] = result.output
        state["total_cost_usd"] += result.cost_usd
        state["current_step"] = "portfolio"
        return state

    async def _portfolio_node(self, state: WorkflowState) -> WorkflowState:
        state["portfolio_result"] = {"organized": True}
        state["current_step"] = "complete"
        return state

    async def _complete_node(self, state: WorkflowState) -> WorkflowState:
        state["is_complete"] = True
        state["current_step"] = "complete"
        await self._update_db_status(state["workflow_id"], "completed", 0)
        log.info("✅ Workflow complete", workflow_id=state["workflow_id"], cost=state["total_cost_usd"])
        return state

    async def _reject_node(self, state: WorkflowState) -> WorkflowState:
        state["is_complete"] = True
        state["is_approved"] = False
        state["current_step"] = "rejected"
        await self._update_db_status(state["workflow_id"], "rejected", 0)
        log.warning("❌ Workflow rejected", workflow_id=state["workflow_id"])
        return state

    async def _update_db_status(self, workflow_id: str, step: str, cost: float):
        """Update workflow status in DB."""
        try:
            from app.database.base import AsyncSessionLocal
            from app.models.task import WorkflowExecution
            from sqlalchemy import select
            async with AsyncSessionLocal() as session:
                result = await session.execute(
                    select(WorkflowExecution).where(WorkflowExecution.id == uuid.UUID(workflow_id))
                )
                wf = result.scalar_one_or_none()
                if wf:
                    wf.current_step = step
                    wf.total_cost_usd = (wf.total_cost_usd or 0) + cost
                    wf.completed_steps = (wf.completed_steps or 0) + 1
                    if step in ("completed", "rejected"):
                        wf.status = step
                        wf.completed_at = datetime.now(timezone.utc)
                    await session.commit()
        except Exception as e:
            log.warning("Could not update workflow DB status", error=str(e))

    async def execute_step(self, task_input: dict[str, Any]) -> dict[str, Any]:
        """
        Execute the full production workflow.
        Uses LangGraph if available, otherwise sequential fallback.
        """
        workflow_id = str(task_input.get("workflow_id", uuid.uuid4()))
        from app.core.config import settings

        initial_state: WorkflowState = {
            "task_id": str(task_input.get("task_id", uuid.uuid4())),
            "workflow_id": workflow_id,
            "concept": task_input.get("concept", {}),
            "niche": task_input.get("niche", "general"),
            "style": task_input.get("style", "minimalist"),
            "custom_instructions": task_input.get("custom_instructions", ""),
            "research_result": {},
            "creative_result": {},
            "generation_result": {},
            "quality_result": {},
            "compliance_result": {},
            "seo_result": {},
            "portfolio_result": {},
            "current_step": "research",
            "retry_count": 0,
            "max_retries": settings.MAX_RETRIES_PER_DESIGN,
            "total_cost_usd": 0.0,
            "max_spend_usd": settings.MAX_DAILY_SPEND_USD,
            "errors": [],
            "is_approved": False,
            "is_complete": False,
            "is_stub": False,
        }

        # Try LangGraph first
        graph = self._build_graph()
        if graph:
            try:
                final_state = await graph.ainvoke(initial_state)
                return {"success": final_state.get("is_approved", False), **final_state}
            except Exception as e:
                log.warning("LangGraph execution failed, using sequential fallback", error=str(e))

        # Sequential fallback
        state = initial_state
        try:
            state = await self._research_node(state)
            state = await self._creative_node(state)
            state = await self._generate_node(state)
            state = await self._quality_node(state)
            if state.get("is_approved"):
                state = await self._compliance_node(state)
                state = await self._seo_node(state)
                state = await self._portfolio_node(state)
                state = await self._complete_node(state)
            else:
                state = await self._reject_node(state)
        except Exception as e:
            log.error("Workflow execution error", error=str(e))
            state["errors"].append(str(e))
            state["is_complete"] = True

        return {"success": state.get("is_approved", False), **state}

    async def start(self, task_input: dict[str, Any]) -> str:
        """Start workflow asynchronously via Celery."""
        workflow_id = str(uuid.uuid4())
        task_input["workflow_id"] = workflow_id

        try:
            from workers.tasks import run_production_workflow
            run_production_workflow.delay(task_input)
        except Exception:
            # Run directly if Celery unavailable
            import asyncio
            asyncio.create_task(self.execute_step(task_input))

        return workflow_id
