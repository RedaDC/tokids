"""
TeeDesign AI — All Agents (complete implementations)
"""
from __future__ import annotations

import json
import uuid
from typing import Any

from .base_agent import BaseAgent, AgentResult


# ─── Research Agent ─────────────────────────────────────────────────────────

class ResearchAgent(BaseAgent):
    SYSTEM_PROMPT = """You are a Market Research Specialist for TeeDesign AI, an autonomous illustration studio.
Your job: Identify promising niches for merchandise illustrations on TeePublic.

Analyze:
- Customer interests and demographics
- Seasonal opportunities  
- Competition levels
- Creative gaps in the market

Always return valid JSON with this exact structure:
{
  "niches": [
    {
      "name": "string",
      "target_audience": "string",
      "evidence": "string (why this is a good opportunity)",
      "competition_level": "low|medium|high|saturated",
      "creative_opportunity": "string",
      "confidence_score": number (0-100),
      "keywords": ["string"],
      "is_seasonal": boolean,
      "season": "string or null"
    }
  ]
}"""

    STUB_NICHES = [
        {
            "name": "Cozy Cottagecore",
            "target_audience": "Young adults 18-35, home decor enthusiasts, cottagecore aesthetic fans",
            "evidence": "Cottagecore aesthetic has 2B+ TikTok views. High demand for pastoral, whimsical illustrations featuring mushrooms, wildflowers, and cottage life.",
            "competition_level": "medium",
            "creative_opportunity": "Focus on original forest creature characters in cozy settings — snails, hedgehogs, mice — that feel handcrafted and unique.",
            "confidence_score": 82.0,
            "keywords": ["cottagecore", "cozy", "mushroom", "wildflower", "forest", "whimsical"],
            "is_seasonal": False,
            "season": None,
        },
        {
            "name": "Space Cats",
            "target_audience": "Cat lovers, space enthusiasts, millennials, gift buyers",
            "evidence": "Cat-themed products consistently top seller charts. Space aesthetics combined with cute animals create unique crossover appeal with broad gifting potential.",
            "competition_level": "medium",
            "creative_opportunity": "Astronaut cats, cats on alien planets, cats piloting spaceships — retro sci-fi aesthetic with cute cat characters is underserved.",
            "confidence_score": 76.0,
            "keywords": ["space cat", "astronaut", "galaxy", "cute", "cosmic", "sci-fi"],
            "is_seasonal": False,
            "season": None,
        },
        {
            "name": "Vintage National Parks",
            "target_audience": "Outdoor enthusiasts, hikers, campers, nature lovers, environmentalists",
            "evidence": "National Parks merchandise sees 40% spike in spring/summer. Vintage poster style with original park illustrations avoids IP issues while tapping nostalgia.",
            "competition_level": "high",
            "creative_opportunity": "Create original vintage-style illustrations of lesser-known parks and trails — avoids direct competition with popular Yosemite/Grand Canyon designs.",
            "confidence_score": 71.0,
            "keywords": ["national park", "vintage", "hiking", "outdoor", "nature", "camping"],
            "is_seasonal": True,
            "season": "spring-summer",
        },
    ]

    def __init__(self, agent_id: uuid.UUID | None = None):
        super().__init__(
            name="Market Research Agent",
            role="Market Research Specialist",
            description="Identifies illustration niches and research opportunities",
            agent_id=agent_id,
        )

    async def execute(self, task_input: dict[str, Any]) -> AgentResult:
        query = task_input.get("query", "Find promising illustration niches for TeePublic merchandise")
        num_niches = task_input.get("num_niches", 3)

        if self._is_stub or not self._get_llm_client():
            # Return stub data
            return AgentResult(
                success=True,
                output={"niches": self.STUB_NICHES[:num_niches], "query": query},
                is_stub=True,
            )

        prompt = f"""Research request: {query}

Find {num_niches} promising niches for merchandise illustrations.
Consider: current trends, competition levels, customer demographics, seasonal factors.
Return valid JSON only."""

        llm_result = await self._call_llm(prompt, system_prompt=self.SYSTEM_PROMPT, response_format="json")

        try:
            data = json.loads(llm_result["content"])
            return AgentResult(success=True, output=data, is_stub=False)
        except (json.JSONDecodeError, KeyError) as e:
            return AgentResult(success=False, output={}, error=f"Failed to parse LLM response: {e}")


# ─── Creative Director Agent ─────────────────────────────────────────────────

class CreativeDirectorAgent(BaseAgent):
    SYSTEM_PROMPT = """You are the Creative Director for TeeDesign AI.
Create original design concepts for merchandise illustrations.

Always return valid JSON:
{
  "concepts": [
    {
      "title": "string",
      "description": "string",
      "style": "string",
      "color_palette": ["#hex1", "#hex2", "#hex3", "#hex4"],
      "composition_notes": "string",
      "generation_prompt": "string (detailed prompt for image generation)",
      "negative_prompt": "string"
    }
  ]
}

For generation_prompt: be specific, descriptive, and avoid any copyrighted characters or brands."""

    STUB_CONCEPTS = [
        {
            "title": "Moonlit Cottage Cat",
            "description": "A cozy tabby cat reading a book by candlelight in a magical cottage window, surrounded by hanging herbs and enchanted mason jars.",
            "style": "whimsical",
            "color_palette": ["#2D1B69", "#7B4FA6", "#E8A87C", "#F9E4B7", "#4A90D9"],
            "composition_notes": "Circular vignette composition. Cat centered in warm window light against cool moonlit exterior.",
            "generation_prompt": "A cozy tabby cat reading a small book by warm candlelight, sitting in a magical cottage window, dried herbs and wildflowers hanging from wooden beams, enchanted glowing mason jars, soft moonlight outside, whimsical illustration style, warm amber tones, transparent background, digital art, sticker-ready design",
            "negative_prompt": "text, watermark, logo, blurry, deformed, realistic photo, photography",
        },
        {
            "title": "Cosmic Adventurer Cat",
            "description": "An astronaut cat floating in a colorful galaxy surrounded by tiny planets and shooting stars with a retro sci-fi aesthetic.",
            "style": "retro",
            "color_palette": ["#0B1026", "#3D1A78", "#00D4FF", "#FF6B6B", "#FFD700"],
            "composition_notes": "Cat centered with planets and stars orbiting around it. Badge-like circular border.",
            "generation_prompt": "Cute cartoon astronaut cat floating in space, colorful galaxy background with planets and stars, retro 1960s space poster aesthetic, vibrant colors, circular badge composition, isolated on transparent background, vector illustration style, clean lines",
            "negative_prompt": "realistic, photo, blurry, text, watermark, copyrighted characters",
        },
        {
            "title": "Botanical Mushroom Kingdom",
            "description": "A detailed botanical illustration of enchanted mushrooms with tiny fairy doors, moss, and dewdrops in a forest setting.",
            "style": "botanical",
            "color_palette": ["#2D5016", "#7FB069", "#E76F51", "#F4A261", "#E8D5B7"],
            "composition_notes": "Tall vertical composition. Large mushrooms frame smaller details below.",
            "generation_prompt": "Detailed botanical illustration of magical mushrooms with tiny fairy doors carved in stems, fresh green moss, morning dewdrops, fern fronds, woodland flowers, cottagecore aesthetic, earthy color palette, fine line art with watercolor texture, transparent background, art nouveau borders",
            "negative_prompt": "photography, realistic photo, text, logo, watermark, blurry",
        },
    ]

    def __init__(self, agent_id: uuid.UUID | None = None):
        super().__init__(
            name="Creative Director",
            role="Creative Director AI",
            description="Develops original illustration concepts, styles, and generation prompts",
            agent_id=agent_id,
        )

    async def execute(self, task_input: dict[str, Any]) -> AgentResult:
        niche = task_input.get("niche", "general merchandise")
        style = task_input.get("style", "")
        num_concepts = task_input.get("num_concepts", 3)

        client = self._get_llm_client()
        if self._is_stub:
            return AgentResult(
                success=True,
                output={"concepts": self.STUB_CONCEPTS[:num_concepts], "niche": niche},
                is_stub=True,
            )

        prompt = f"""Create {num_concepts} original illustration concepts for the "{niche}" niche.
Style preference: {style or 'any appropriate style'}

Requirements:
- Original characters and scenes (no copyrighted elements)
- Suitable for merchandise (clear, impactful, print-ready)
- Generation prompts must be detailed and specific
- Include transparent background instruction in all prompts"""

        llm_result = await self._call_llm(prompt, system_prompt=self.SYSTEM_PROMPT, response_format="json")
        try:
            data = json.loads(llm_result["content"])
            return AgentResult(success=True, output=data, is_stub=False)
        except Exception as e:
            return AgentResult(success=False, output={}, error=str(e))


# ─── Illustration Generator Agent ───────────────────────────────────────────

class IllustrationGeneratorAgent(BaseAgent):
    def __init__(self, agent_id: uuid.UUID | None = None):
        super().__init__(
            name="Illustration Generator",
            role="AI Illustration Engine",
            description="Generates original illustrations using configured image APIs",
            agent_id=agent_id,
        )

    async def execute(self, task_input: dict[str, Any]) -> AgentResult:
        from image_processing.factory import get_image_provider
        from image_processing.processor import ImageProcessor

        prompt = task_input.get("generation_prompt", "")
        num_variations = task_input.get("num_variations", 1)
        concept_title = task_input.get("title", "Untitled")

        if not prompt:
            return AgentResult(success=False, output={}, error="No generation_prompt provided")

        provider = get_image_provider()
        processor = ImageProcessor()

        if num_variations == 1:
            result = await provider.generate(prompt)
            results = [result]
        else:
            results = await provider.generate_variations(prompt, num_variations=num_variations)

        generated = []
        for img_result in results:
            if img_result.success and img_result.file_path:
                # Process image
                processing = await processor.process_for_library(img_result.file_path)
                self.track_cost(img_result.cost_usd)
                generated.append({
                    "file_path": img_result.file_path,
                    "preview_path": processing.preview_path,
                    "export_path": processing.export_path,
                    "width": img_result.width,
                    "height": img_result.height,
                    "cost_usd": img_result.cost_usd,
                    "provider": img_result.provider,
                    "model": img_result.model,
                    "is_stub": img_result.is_stub,
                    "has_transparency": processing.has_transparency,
                    "is_blurry": processing.is_blurry,
                    "metadata": img_result.metadata,
                })
            else:
                generated.append({"error": img_result.error, "is_stub": img_result.is_stub})

        success_count = sum(1 for g in generated if "file_path" in g)
        return AgentResult(
            success=success_count > 0,
            output={
                "generated": generated,
                "total_generated": success_count,
                "total_cost_usd": sum(g.get("cost_usd", 0) for g in generated),
                "concept_title": concept_title,
                "is_stub": results[0].is_stub if results else False,
            },
            is_stub=results[0].is_stub if results else False,
        )


# ─── Quality Control Agent ───────────────────────────────────────────────────

class QualityControlAgent(BaseAgent):
    SYSTEM_PROMPT = """You are a Quality Control Inspector for merchandise illustrations.
Evaluate artwork on 5 criteria (each 0-100):
1. Visual Quality (25%): Sharpness, resolution, clarity
2. Originality (25%): Uniqueness, creative expression
3. Composition (20%): Balance, focal point, layout
4. Print Suitability (20%): Contrast, colors for printing, clean edges
5. Niche Relevance (10%): How well it fits the target niche

Return JSON:
{
  "visual_quality_score": number,
  "originality_score": number,
  "composition_score": number,
  "print_suitability_score": number,
  "niche_relevance_score": number,
  "overall_score": number,
  "is_approved": boolean,
  "rejection_reason": "string or null",
  "notes": "string"
}"""

    def __init__(self, agent_id: uuid.UUID | None = None):
        super().__init__(
            name="Quality Control Agent",
            role="Quality Inspector AI",
            description="Evaluates artwork quality across 5 weighted categories",
            agent_id=agent_id,
        )

    def _basic_quality_check(self, image_path: str) -> dict[str, Any]:
        """Basic PIL-based quality scoring when LLM is unavailable."""
        try:
            from image_processing.processor import ImageProcessor
            processor = ImageProcessor()

            dims = processor.validate_dimensions(image_path)
            blur = processor.detect_blur(image_path)
            has_transparency = processor.validate_transparency(image_path)

            width = dims.get("width", 0)
            height = dims.get("height", 0)

            # Dimension score
            dim_score = min(100, (width / 500) * 50 + (height / 500) * 50) if width and height else 20

            # Blur score (higher blur score = less blurry = better)
            blur_val = blur.get("blur_score", 0)
            visual_quality = min(100, max(0, (blur_val / 500) * 100)) if not blur.get("is_blurry") else 30

            # Assign heuristic scores
            scores = {
                "visual_quality_score": min(100, visual_quality * 0.7 + dim_score * 0.3),
                "originality_score": 72.0,  # Can't assess without LLM
                "composition_score": 68.0,
                "print_suitability_score": 75.0 if has_transparency else 65.0,
                "niche_relevance_score": 70.0,
            }

            # Weighted overall
            overall = (
                scores["visual_quality_score"] * 0.25
                + scores["originality_score"] * 0.25
                + scores["composition_score"] * 0.20
                + scores["print_suitability_score"] * 0.20
                + scores["niche_relevance_score"] * 0.10
            )

            from app.core.config import settings
            is_approved = overall >= settings.MIN_QUALITY_SCORE
            return {
                **scores,
                "overall_score": round(overall, 1),
                "is_approved": is_approved,
                "rejection_reason": f"Quality score {overall:.1f} below threshold {settings.MIN_QUALITY_SCORE}" if not is_approved else None,
                "notes": "Automated heuristic scoring (stub mode). Configure LLM for AI-powered evaluation.",
                "has_transparency": has_transparency,
                "dimensions_valid": dims.get("is_valid", False),
                "is_blurry": blur.get("is_blurry", False),
            }
        except Exception as e:
            return {
                "visual_quality_score": 65.0, "originality_score": 65.0,
                "composition_score": 65.0, "print_suitability_score": 65.0,
                "niche_relevance_score": 65.0, "overall_score": 65.0,
                "is_approved": False, "rejection_reason": f"Could not evaluate: {e}",
                "notes": str(e), "has_transparency": False, "dimensions_valid": False, "is_blurry": False,
            }

    async def execute(self, task_input: dict[str, Any]) -> AgentResult:
        image_path = task_input.get("file_path", "")
        niche = task_input.get("niche", "general")
        concept_description = task_input.get("description", "")

        if not image_path:
            return AgentResult(success=False, output={}, error="No file_path provided")

        client = self._get_llm_client()
        if self._is_stub:
            scores = self._basic_quality_check(image_path)
            return AgentResult(success=True, output=scores, is_stub=True)

        prompt = f"""Evaluate this merchandise illustration for TeePublic:
Niche: {niche}
Concept: {concept_description}
File: {image_path}

Score each criterion 0-100 and determine approval status."""

        llm_result = await self._call_llm(prompt, system_prompt=self.SYSTEM_PROMPT, response_format="json")
        try:
            data = json.loads(llm_result["content"])
            return AgentResult(success=True, output=data, is_stub=False)
        except Exception as e:
            # Fallback to basic scoring
            scores = self._basic_quality_check(image_path)
            return AgentResult(success=True, output=scores, is_stub=True)


# ─── Copyright Compliance Agent ───────────────────────────────────────────────

class ComplianceAgent(BaseAgent):
    DISCLAIMER = "⚠️ Automated screening does not guarantee legal clearance. Human review is recommended before publication."

    def __init__(self, agent_id: uuid.UUID | None = None):
        super().__init__(
            name="Copyright Compliance Agent",
            role="IP Compliance Specialist",
            description="Screens designs for IP risks and trademark issues",
            agent_id=agent_id,
        )

    # Keywords that trigger medium/high risk flags
    HIGH_RISK_TERMS = [
        "mickey", "pokemon", "disney", "marvel", "dc comics", "superman", "batman",
        "star wars", "harry potter", "hello kitty", "spongebob", "peppa pig",
        "minions", "paw patrol", "nike", "adidas", "apple logo", "google",
    ]
    MEDIUM_RISK_TERMS = [
        "inspired by", "in the style of", "tribute to", "fan art",
        "based on", "replica", "copy of",
    ]

    def _check_prompt(self, prompt: str) -> dict[str, Any]:
        prompt_lower = prompt.lower()
        flags = []
        risk_level = "low"

        for term in self.HIGH_RISK_TERMS:
            if term in prompt_lower:
                flags.append(f"High-risk term detected: '{term}' — may reference protected IP")
                risk_level = "high"

        for term in self.MEDIUM_RISK_TERMS:
            if term in prompt_lower:
                flags.append(f"Medium-risk phrase: '{term}'")
                if risk_level == "low":
                    risk_level = "medium"

        is_cleared = risk_level in ("low", "medium")
        return {
            "risk_level": risk_level,
            "flags": flags,
            "is_cleared": is_cleared,
            "review_notes": self.DISCLAIMER,
            "prompt_checked": prompt,
        }

    async def execute(self, task_input: dict[str, Any]) -> AgentResult:
        prompt = task_input.get("generation_prompt", "")
        concept_description = task_input.get("description", "")

        result = self._check_prompt(f"{prompt} {concept_description}")

        if result["risk_level"] == "high":
            self._log_activity(
                "⚠️ High IP risk detected",
                risk_level=result["risk_level"],
                flags=result["flags"],
                level="warning",
            )

        return AgentResult(
            success=True,
            output=result,
            is_stub=self._is_stub,
        )


# ─── SEO Agent ───────────────────────────────────────────────────────────────

class SEOAgent(BaseAgent):
    SYSTEM_PROMPT = """You are an SEO Specialist for TeePublic merchandise listings.
Create optimized listing metadata that:
- Uses natural, non-stuffed keywords
- Writes compelling, accurate descriptions
- Selects relevant tags (max 20)
- Avoids trademarked terms unless factually applicable

Return JSON:
{
  "title": "string (max 60 chars)",
  "description": "string (150-300 chars)",
  "primary_keyword": "string",
  "tags": ["string", ...],
  "category": "string"
}"""

    STUB_METADATA = {
        "title": "Whimsical Forest Creature Illustration",
        "description": "Original whimsical illustration featuring an enchanting forest creature surrounded by magical botanicals. Perfect for nature lovers and fantasy art fans. Great for t-shirts, mugs, and stickers.",
        "primary_keyword": "whimsical forest illustration",
        "tags": ["whimsical", "forest", "illustration", "fantasy", "nature", "magical", "botanical", "original art", "cute", "sticker"],
        "category": "Art & Illustration",
    }

    def __init__(self, agent_id: uuid.UUID | None = None):
        super().__init__(
            name="SEO Specialist",
            role="SEO & Listing Optimizer",
            description="Generates optimized SEO metadata for merchandise listings",
            agent_id=agent_id,
        )

    async def execute(self, task_input: dict[str, Any]) -> AgentResult:
        concept_title = task_input.get("title", "Illustration")
        concept_description = task_input.get("description", "")
        niche = task_input.get("niche", "general")
        style = task_input.get("style", "")

        client = self._get_llm_client()
        if self._is_stub:
            stub = {**self.STUB_METADATA, "title": concept_title[:60]}
            return AgentResult(success=True, output=stub, is_stub=True)

        prompt = f"""Create TeePublic listing metadata for:
Title: {concept_title}
Description: {concept_description}
Niche: {niche}
Style: {style}

Requirements:
- Title max 60 chars, keyword-rich but natural
- Description 150-300 chars, engaging, no keyword stuffing
- 10-20 relevant tags
- Appropriate category for TeePublic"""

        llm_result = await self._call_llm(prompt, system_prompt=self.SYSTEM_PROMPT, response_format="json")
        try:
            data = json.loads(llm_result["content"])
            return AgentResult(success=True, output=data, is_stub=False)
        except Exception as e:
            return AgentResult(success=True, output=self.STUB_METADATA, is_stub=True)


# ─── CEO Agent ───────────────────────────────────────────────────────────────

class CEOAgent(BaseAgent):
    def __init__(self, agent_id: uuid.UUID | None = None):
        super().__init__(
            name="CEO Orchestrator",
            role="Chief Executive AI",
            description="Coordinates all agents, assigns tasks, monitors workflows",
            agent_id=agent_id,
        )

    async def execute(self, task_input: dict[str, Any]) -> AgentResult:
        """CEO delegates to the production workflow."""
        from workflows.production_workflow import ProductionWorkflow
        workflow = ProductionWorkflow()
        result = await workflow.execute_step(task_input)
        return AgentResult(
            success=result.get("success", False),
            output=result,
            is_stub=task_input.get("is_stub", True),
        )


# ─── Portfolio Agent ──────────────────────────────────────────────────────────

class PortfolioAgent(BaseAgent):
    def __init__(self, agent_id: uuid.UUID | None = None):
        super().__init__(
            name="Portfolio Manager",
            role="Portfolio & Asset Manager",
            description="Organizes artwork, manages collections, prepares exports",
            agent_id=agent_id,
        )

    async def execute(self, task_input: dict[str, Any]) -> AgentResult:
        design_id = task_input.get("design_id")
        action = task_input.get("action", "organize")
        return AgentResult(
            success=True,
            output={"design_id": str(design_id), "action": action, "status": "organized"},
            is_stub=True,
        )


# ─── Analytics Agent ─────────────────────────────────────────────────────────

class AnalyticsAgent(BaseAgent):
    def __init__(self, agent_id: uuid.UUID | None = None):
        super().__init__(
            name="Analytics Agent",
            role="Data Analytics Specialist",
            description="Monitors production stats and provides data-driven insights",
            agent_id=agent_id,
        )

    async def execute(self, task_input: dict[str, Any]) -> AgentResult:
        # Fetch real metrics from DB
        try:
            from app.services.analytics_service import get_production_stats
            stats = await get_production_stats()
            return AgentResult(success=True, output=stats, is_stub=False)
        except Exception as e:
            return AgentResult(success=False, output={}, error=str(e))
