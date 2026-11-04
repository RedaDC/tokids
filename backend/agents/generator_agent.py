"""
TeeDesign AI — Illustration Generator Agent
"""
import time
import uuid
from pathlib import Path
from typing import Any
from .base_agent import AgentResult, BaseAgent
from app.core.config import settings
from app.models.agent import AgentStatus
from image_processing.factory import get_image_provider
from image_processing.processor import processor
from app.services.storage_service import storage_service


class GeneratorAgent(BaseAgent):
    """Illustration Generator Agent: Coordinates image generation and asset rendering."""

    def __init__(self):
        super().__init__(
            name="Illustration Generator",
            role="AI Art Generation Engineer",
            description="Executes image synthesis pipelines (OpenAI / Replicate / Stub) and renders assets to disk.",
        )

    async def execute(self, task_input: dict[str, Any]) -> AgentResult:
        start_time = time.time()
        self.status = AgentStatus.WORKING

        prompt = task_input.get("generation_prompt") or task_input.get("prompt")
        if not prompt:
            title = task_input.get("concept_title", "Epic Graphic")
            style = task_input.get("style", "vintage t-shirt illustration")
            prompt = f"Striking t-shirt illustration of {title}, {style}, isolated on transparent background, vector design"

        provider_name = task_input.get("provider") or settings.IMAGE_PROVIDER
        model_name = task_input.get("model")
        width = int(task_input.get("width", 1024))
        height = int(task_input.get("height", 1024))

        self.log(f"Synthesizing image via provider '{provider_name}'...")

        provider = get_image_provider(provider_name=provider_name, model=model_name)
        img_result = await provider.generate(prompt=prompt, width=width, height=height)

        # Ensure directories exist
        storage_service.ensure_directories()

        # Save master file
        asset_id = uuid.uuid4().hex[:12]
        master_filename = f"design_{asset_id}_master.png"
        preview_filename = f"design_{asset_id}_preview.png"

        master_path = await storage_service.save_file(
            content=img_result.image_bytes,
            directory=storage_service.master_dir,
            filename=master_filename,
        )

        # Generate preview thumbnail
        preview_full_path = storage_service.preview_dir / preview_filename
        preview_path = processor.create_preview(
            image_path=master_path,
            output_path=preview_full_path,
            width=600,
            height=600,
        )

        self.track_cost(img_result.cost_usd)
        self.status = AgentStatus.COMPLETED
        elapsed_ms = (time.time() - start_time) * 1000

        self.log(f"Image generation completed. Saved master to '{master_filename}' (Cost: ${img_result.cost_usd:.4f})")

        output = {
            "file_path": master_path,
            "preview_path": preview_path,
            "master_path": master_path,
            "width": img_result.width,
            "height": img_result.height,
            "file_size_bytes": len(img_result.image_bytes),
            "generation_cost": img_result.cost_usd,
            "generation_provider": img_result.provider,
            "generation_model": img_result.model,
            "metadata": img_result.metadata,
        }

        return AgentResult(
            success=True,
            output=output,
            cost_usd=img_result.cost_usd,
            tokens_used=0,
            execution_time_ms=elapsed_ms,
        )
