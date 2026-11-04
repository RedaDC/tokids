"""
TeeDesign AI — Market Research Specialist Agent
"""
import time
from typing import Any
from .base_agent import AgentResult, BaseAgent
from app.models.agent import AgentStatus


class ResearchAgent(BaseAgent):
    """Market Research Agent: Analyzes POD market trends, keyword volume, and niche opportunities."""

    def __init__(self):
        super().__init__(
            name="Market Research Specialist",
            role="Trend Analyst & Market Opportunity Researcher",
            description="Identifies profitable, underserved apparel niches with strong viral potential.",
        )

    async def execute(self, task_input: dict[str, Any]) -> AgentResult:
        start_time = time.time()
        self.status = AgentStatus.WORKING
        niche_query = task_input.get("niche_query") or task_input.get("niche") or "Space Cats"

        self.log(f"Conducting deep niche research for query: '{niche_query}'")

        llm = self.get_llm_client()

        if hasattr(llm, "is_stub") and llm.is_stub:
            # Deterministic, realistic rich stub niche analysis
            sample_niches = {
                "Space Cats": {
                    "niche_name": "Cosmic Space Cats",
                    "target_audience": "Cat lovers, sci-fi enthusiasts, millennials, quirky humor apparel buyers",
                    "evidence": "High TeePublic search volume for 'cat in space' (+34% YoY); low saturation of retro linocut styles.",
                    "competition_assessment": "Moderate generic designs, but distinct lack of stylized vintage botanical & cosmic fusion.",
                    "creative_opportunity": "Feline astronaut with celestial starlight halo, ornate helmet detailing, vibrant vector linework.",
                    "confidence_score": 88.5,
                },
                "Retro Gaming": {
                    "niche_name": "16-Bit Retro Arcade Nostalgia",
                    "target_audience": "Gamers (25-45), pixel art lovers, 80s/90s nostalgia collectors",
                    "evidence": "Consistent evergreen seller on TeePublic and Redbubble; vintage neon gaming quotes trend upwards during holidays.",
                    "competition_assessment": "High volume of low-res pixel dumps; massive demand for premium illustrated reinterpretations.",
                    "creative_opportunity": "Isometric synthwave arcade machine overflowing with mythical dreamscape creatures.",
                    "confidence_score": 84.0,
                },
                "Botanical Illustrations": {
                    "niche_name": "Dark Vintage Botanical & Fungi",
                    "target_audience": "Nature lovers, dark academia, gardeners, cottagecore & gothic aesthetic fans",
                    "evidence": "Wild mushroom and nocturnal floral motifs showing 45% engagement spike on Pinterest and Etsy.",
                    "competition_assessment": "Medium competition; public domain scans are common but original vector artwork is scarce.",
                    "creative_opportunity": "Luminescent nocturnal fungi with moth wings and celestial astrological chart border.",
                    "confidence_score": 91.0,
                },
            }

            matched = sample_niches.get(niche_query)
            if not matched:
                matched = {
                    "niche_name": niche_query.title(),
                    "target_audience": f"Enthusiasts and subculture fans passionate about {niche_query}",
                    "evidence": f"Steady recurring consumer interest across print-on-demand marketplaces for {niche_query}.",
                    "competition_assessment": "Scattered amateur designs, primed for cohesive high-end illustrated concepts.",
                    "creative_opportunity": f"Striking iconic visual emblematic of {niche_query} with vintage screenprint styling.",
                    "confidence_score": 85.0,
                }

            report = matched
            cost = 0.0
            tokens = 0
        else:
            prompt = (
                f"Analyze the market opportunity for print-on-demand apparel in the niche: '{niche_query}'. "
                "Respond in JSON format with exact keys:\n"
                "{\n"
                '  "niche_name": "string",\n'
                '  "target_audience": "string",\n'
                '  "evidence": "string",\n'
                '  "competition_assessment": "string",\n'
                '  "creative_opportunity": "string",\n'
                '  "confidence_score": float (0-100)\n'
                "}"
            )
            report = await llm.generate_json(
                prompt,
                system="You are a senior eCommerce apparel trend analyst specializing in TeePublic and Redbubble markets.",
            )
            cost = 0.005
            tokens = 450

        self.track_cost(cost, tokens)
        self.status = AgentStatus.COMPLETED
        elapsed_ms = (time.time() - start_time) * 1000

        self.log(f"Research complete: {report.get('niche_name')} (Score: {report.get('confidence_score')})")

        return AgentResult(
            success=True,
            output=report,
            cost_usd=cost,
            tokens_used=tokens,
            execution_time_ms=elapsed_ms,
        )
