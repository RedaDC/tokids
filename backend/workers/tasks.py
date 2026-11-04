"""
TeeDesign AI — Celery Tasks
"""
import asyncio
from typing import Any

from workers.celery_app import celery_app


def run_async(coro):
    """Run async coroutine in Celery task context."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


@celery_app.task(name="workers.tasks.run_production_workflow", bind=True, max_retries=3)
def run_production_workflow(self, task_input: dict[str, Any]):
    """Run the full production workflow."""
    from workflows.production_workflow import ProductionWorkflow
    workflow = ProductionWorkflow()
    return run_async(workflow.execute_step(task_input))


@celery_app.task(name="workers.tasks.run_research", bind=True, max_retries=2)
def run_research(self, niche_query: str):
    """Run market research for a niche."""
    from agents.agents import ResearchAgent
    agent = ResearchAgent()
    return run_async(agent.execute_with_tracking({"query": niche_query}))


@celery_app.task(name="workers.tasks.generate_design", bind=True, max_retries=3)
def generate_design(self, concept_id: str):
    """Generate artwork for a concept."""
    from agents.agents import IllustrationGeneratorAgent
    agent = IllustrationGeneratorAgent()
    return run_async(agent.execute_with_tracking({"concept_id": concept_id}))


@celery_app.task(name="workers.tasks.evaluate_quality", bind=True, max_retries=2)
def evaluate_quality(self, design_id: str):
    """Evaluate quality of a design."""
    from agents.agents import QualityControlAgent
    agent = QualityControlAgent()
    return run_async(agent.execute_with_tracking({"design_id": design_id}))


@celery_app.task(name="workers.tasks.generate_seo", bind=True, max_retries=2)
def generate_seo(self, design_id: str):
    """Generate SEO metadata for a design."""
    from agents.agents import SEOAgent
    agent = SEOAgent()
    return run_async(agent.execute_with_tracking({"design_id": design_id}))


@celery_app.task(name="workers.tasks.run_analytics")
def run_analytics():
    """Daily analytics aggregation."""
    from agents.agents import AnalyticsAgent
    agent = AnalyticsAgent()
    return run_async(agent.execute_with_tracking({}))
