"""
TeeDesign AI — Creative Director Agent
"""
import time
from typing import Any
from agents.base_agent import AgentResult, BaseAgent
from app.models.agent import AgentStatus


class CreativeAgent(BaseAgent):
    """Creative Director Agent: Conceptualizes artistic themes, palettes, and prompt engineering."""

    def __init__(self):
        super().__init__(
            name="Creative Director",
            role="Art Director & Visual Concept Designer",
            description="Transforms niche insights into vivid apparel illustration prompts tailored for t-shirt graphics.",
        )

    async def execute(self, task_input: dict[str, Any]) -> AgentResult:
        start_time = time.time()
        self.status = AgentStatus.WORKING

        niche_name = task_input.get("niche_name") or task_input.get("niche") or "Space Exploration"
        preferred_style = task_input.get("style", "vintage screenprint illustration")

        self.log(f"Developing creative concepts for '{niche_name}' with style '{preferred_style}'")

        llm = self.get_llm_client()

        if hasattr(llm, "is_stub") and llm.is_stub:
            # Deterministic, high-aesthetic mock concepts
            primary_concept = {
                "concept_title": f"The Astral Odyssey of {niche_name}",
                "description": f"A nostalgic 1970s sci-fi linework illustration highlighting {niche_name} in deep space.",
                "style": preferred_style,
                "color_palette": ["#FFBE0B", "#FB5607", "#FF006E", "#8338EC", "#3A86FF"],
                "composition_notes": "Centered circular badge composition, bold vector silhouettes, distressed halftone textures, isolated on transparent background.",
                "generation_prompt": (
                    f"A masterwork t-shirt graphic illustration of {niche_name}, {preferred_style}, "
                    "bold outlines, vibrant screenprint colors, distressed vintage halftone dots, "
                    "isolated on clean transparent background, vector apparel graphic, no background, high detail"
                ),
            }

            concept_variations = [
                primary_concept,
                {
                    "concept_title": f"Minimalist Celestial {niche_name}",
                    "description": f"Clean Japanese woodblock inspired monochrome rendition of {niche_name}.",
                    "style": "ukiyo-e woodblock print",
                    "color_palette": ["#1A1A1A", "#E63946", "#F1FAEE", "#A8DADC"],
                    "composition_notes": "Asymmetrical balanced arrangement, dramatic sweeping ink strokes, clean negative space.",
                    "generation_prompt": f"Ukiyo-e woodblock t-shirt design of {niche_name}, bold sumi-e ink linework, crimson red sun accent, pure transparent background.",
                },
                {
                    "concept_title": f"Cyberpunk Neon {niche_name}",
                    "description": f"Vivid 80s outrun synthwave emblem featuring {niche_name}.",
                    "style": "synthwave neon vector",
                    "color_palette": ["#00F5D4", "#7B2CBF", "#F72585", "#4CC9F0"],
                    "composition_notes": "Diamond badge framing, geometric grid accents, radiant glowing contour outlines.",
                    "generation_prompt": f"Vibrant synthwave neon vector emblem of {niche_name}, retro 80s aesthetic, glowing cyan and magenta accents, transparent background.",
                },
            ]

            output = {
                "selected_concept": primary_concept,
                "concept_title": primary_concept["concept_title"],
                "description": primary_concept["description"],
                "style": primary_concept["style"],
                "color_palette": primary_concept["color_palette"],
                "composition_notes": primary_concept["composition_notes"],
                "generation_prompt": primary_concept["generation_prompt"],
                "variations": concept_variations,
            }
            cost = 0.0
            tokens = 0
        else:
            prompt = (
                f"Create a high-impact t-shirt design concept for the niche: '{niche_name}' with style '{preferred_style}'. "
                "Output JSON with exact fields:\n"
                "{\n"
                '  "concept_title": "string",\n'
                '  "description": "string",\n'
                '  "style": "string",\n'
                '  "color_palette": ["#hex1", "#hex2", "#hex3"],\n'
                '  "composition_notes": "string",\n'
                '  "generation_prompt": "string tailored for image models like Flux/DALL-E with transparent background requirement",\n'
                '  "variations": [list of 3 concepts with the above structure]\n'
                "}"
            )
            output = await llm.generate_json(
                prompt,
                system="You are an award-winning creative art director designing best-selling graphic apparel.",
            )
            cost = 0.006
            tokens = 600

        self.track_cost(cost, tokens)
        self.status = AgentStatus.COMPLETED
        elapsed_ms = (time.time() - start_time) * 1000

        self.log(f"Creative concepts generated. Selected: '{output.get('concept_title')}'")

        return AgentResult(
            success=True,
            output=output,
            cost_usd=cost,
            tokens_used=tokens,
            execution_time_ms=elapsed_ms,
        )
