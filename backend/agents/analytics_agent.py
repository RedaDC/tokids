"""
TeeDesign AI — Analytics & Performance Insights Agent
"""
import time
from typing import Any, Optional
from .base_agent import AgentResult, BaseAgent
from app.models.agent import AgentStatus


class AnalyticsAgent(BaseAgent):
    """Analytics Agent: Synthesizes performance data, unit economics, and operational suggestions."""

    def __init__(self):
        super().__init__(
            name="Analytics & Intelligence Specialist",
            role="Production Metrics & Unit Economics Analyst",
            description="Aggregates generation costs, approval yields, and marketplace conversion signals.",
        )

    def generate_recommendations(self, stats: dict[str, Any]) -> list[str]:
        """Produce actionable operational suggestions based on factual production signals."""
        recommendations = []
        total_spent = stats.get("total_spent_usd", 0.0)
        approval_rate = stats.get("approval_rate", 100.0)
        avg_quality = stats.get("avg_quality_score", 85.0)

        if approval_rate < 75.0:
            recommendations.append("Approval rate is below 75%; refine creative negative prompts for better edge definition.")
        else:
            recommendations.append("High approval yield (>85%); consider expanding daily batch volume.")

        if avg_quality >= 85.0:
            recommendations.append("Visual quality scores are exceptional. Safe to deploy onto multiple product substrates.")

        if total_spent > 40.0:
            recommendations.append("Daily budget approaching safety threshold ($50.00). Keep monitoring generation cost per image.")
        else:
            recommendations.append(f"Unit economics healthy. Total spend is ${total_spent:.2f}.")

        return recommendations

    async def execute(self, task_input: dict[str, Any]) -> AgentResult:
        start_time = time.time()
        self.status = AgentStatus.WORKING

        # Aggregate inputs from workflow or database summary
        total_designs = task_input.get("total_designs", 1)
        total_cost = task_input.get("total_cost_usd", task_input.get("generation_cost", 0.0))
        quality_score = task_input.get("quality_score", 85.0)
        is_approved = task_input.get("is_approved", True)

        stats = {
            "total_designs": total_designs,
            "total_spent_usd": float(total_cost),
            "approval_rate": 100.0 if is_approved else 0.0,
            "avg_quality_score": float(quality_score),
        }

        recommendations = self.generate_recommendations(stats)

        output = {
            "production_stats": stats,
            "cost_per_design_usd": round(float(total_cost) / max(1, total_designs), 4),
            "recommendations": recommendations,
            "health_status": "optimal",
        }

        self.status = AgentStatus.COMPLETED
        elapsed_ms = (time.time() - start_time) * 1000

        self.log(f"Analytics report generated. Cost per design: ${output['cost_per_design_usd']:.4f}")

        return AgentResult(
            success=True,
            output=output,
            cost_usd=0.0,
            tokens_used=0,
            execution_time_ms=elapsed_ms,
        )
