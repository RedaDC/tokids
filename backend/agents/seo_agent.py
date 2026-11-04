"""
TeeDesign AI — SEO Specialist Agent
"""
import time
from typing import Any
try:
    from .base_agent import AgentResult, BaseAgent, AgentStatus
except (ImportError, ValueError):
    from base_agent import AgentResult, BaseAgent, AgentStatus


class SEOAgent(BaseAgent):
    """SEO Agent: Generates optimized titles, descriptions, and high-converting search tags for TeePublic."""

    def __init__(self):
        super().__init__(
            name="SEO Specialist",
            role="Search Ranking & Apparel Copywriter",
            description="Crafts high-ranking, click-worthy metadata adhering to marketplace guidelines and search intent.",
        )

    async def execute(self, task_input: dict[str, Any]) -> AgentResult:
        start_time = time.time()
        self.status = AgentStatus.WORKING

        concept_title = task_input.get("concept_title") or task_input.get("title") or "Celestial Odyssey"
        niche = task_input.get("niche") or task_input.get("niche_name") or "Space Art"
        style = task_input.get("style", "vintage illustration")

        self.log(f"Generating optimized SEO listing for '{concept_title}' in '{niche}'")

        llm = self.get_llm_client()

        if hasattr(llm, "is_stub") and llm.is_stub:
            # Deterministic, compliant SEO metadata
            raw_title = f"{concept_title} {style}".strip()
            title = raw_title[:60] if len(raw_title) > 60 else raw_title

            primary_keyword = f"{niche.lower()} t-shirt"[:100]

            description = (
                f"Elevate your wardrobe with this handcrafted {concept_title} design. "
                f"Featuring intricate {style} artwork tailored for fans of {niche}. "
                "Printed on ultra-soft premium apparel with vibrant, fade-resistant inks. "
                "The perfect gift for passionate collectors and everyday casual wear."
            )
            # Ensure description is 150-300 chars
            if len(description) > 300:
                description = description[:297] + "..."

            tags = [
                niche.lower(),
                "vintage t-shirt",
                "graphic apparel",
                "screenprint art",
                "retro aesthetic",
                "illustrated tee",
                "gift idea",
                "outer space",
                "indie artist",
                "streetwear",
                "cool design",
                "minimalist tee",
                "aesthetic art",
                "trending apparel",
                "teepublic exclusive",
            ]
            tags = tags[:20]

            output = {
                "title": title,
                "description": description,
                "primary_keyword": primary_keyword,
                "tags": tags,
                "category": "Apparel",
                "platform": "TeePublic",
            }
            cost = 0.0
            tokens = 0
        else:
            prompt = (
                f"Generate optimized eCommerce listing metadata for a t-shirt design.\n"
                f"Concept: '{concept_title}'\nNiche: '{niche}'\nStyle: '{style}'\n\n"
                "Constraints:\n"
                "- Title: max 60 characters, compelling, no keyword stuffing\n"
                "- Description: between 150 and 300 characters, engaging apparel sales copy\n"
                "- Primary keyword: 1 high-intent keyphrase\n"
                "- Tags: array of 15 to 20 relevant, non-trademarked search tags\n"
                "- Category: 'Apparel'\n"
                "Output JSON format matching exact keys: title, description, primary_keyword, tags, category"
            )
            data = await llm.generate_json(
                prompt,
                system="You are an expert eCommerce SEO copywriter for print-on-demand marketplaces.",
            )
            # Ensure character limits
            title = str(data.get("title", concept_title))[:60]
            desc = str(data.get("description", ""))
            if len(desc) < 150:
                desc = desc + " Designed with premium attention to artistic detail and top-tier print fidelity."
            desc = desc[:300]
            tags = list(data.get("tags", []))[:20]

            output = {
                "title": title,
                "description": desc,
                "primary_keyword": str(data.get("primary_keyword", niche))[:100],
                "tags": tags,
                "category": data.get("category", "Apparel"),
                "platform": "TeePublic",
            }
            cost = 0.004
            tokens = 380

        self.track_cost(cost, tokens)
        self.status = AgentStatus.COMPLETED
        elapsed_ms = (time.time() - start_time) * 1000

        self.log(f"SEO metadata generated. Title: '{output.get('title')}' ({len(output.get('tags', []))} tags)")

        return AgentResult(
            success=True,
            output=output,
            cost_usd=cost,
            tokens_used=tokens,
            execution_time_ms=elapsed_ms,
        )
