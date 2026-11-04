"""
TeeDesign AI — Replicate Image Provider (Flux / SDXL)
"""
import logging
from typing import Any, Optional
import httpx

from app.core.config import settings
from image_processing.providers.base_provider import BaseImageProvider, ImageResult
from image_processing.providers.stub_provider import StubProvider

logger = logging.getLogger(__name__)


class ReplicateProvider(BaseImageProvider):
    """Generates images using Replicate API (Flux / SDXL)."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        resolved_key = api_key or settings.REPLICATE_API_KEY
        resolved_model = model or settings.REPLICATE_MODEL or "black-forest-labs/flux-schnell"
        super().__init__(resolved_key, resolved_model)
        self.stub_fallback = StubProvider()

    async def generate(self, prompt: str, **kwargs: Any) -> ImageResult:
        if not self.api_key:
            logger.warning("Replicate API key missing. Falling back to StubProvider.")
            return await self.stub_fallback.generate(prompt, **kwargs)

        width = int(kwargs.get("width", 1024))
        height = int(kwargs.get("height", 1024))

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Prefer": "wait",
        }

        # Normalize model string for replicate deployments or models
        model_name = self.model or "black-forest-labs/flux-schnell"
        url = "https://api.replicate.com/v1/predictions"

        payload = {
            "input": {
                "prompt": prompt,
                "width": width,
                "height": height,
                "num_outputs": 1,
                "aspect_ratio": "1:1",
                "output_format": "png",
            }
        }
        # Model identifier handling
        if ":" in model_name:
            payload["version"] = model_name.split(":")[-1]
        else:
            url = f"https://api.replicate.com/v1/models/{model_name}/predictions"

        try:
            async with httpx.AsyncClient(timeout=60.0) as http_client:
                resp = await http_client.post(url, json=payload, headers=headers)
                resp.raise_for_status()
                data = resp.json()

                output = data.get("output")
                if not output:
                    # If still running, poll
                    poll_url = data.get("urls", {}).get("get")
                    if poll_url:
                        for _ in range(15):
                            import asyncio
                            await asyncio.sleep(2.0)
                            poll_resp = await http_client.get(poll_url, headers=headers)
                            poll_data = poll_resp.json()
                            if poll_data.get("status") == "succeeded":
                                output = poll_data.get("output")
                                break
                            elif poll_data.get("status") in ["failed", "canceled"]:
                                raise ValueError(f"Replicate generation {poll_data.get('status')}")

                if not output:
                    raise ValueError("No output image from Replicate")

                image_url = output[0] if isinstance(output, list) else output

                # Download the image
                img_resp = await http_client.get(image_url)
                img_resp.raise_for_status()
                image_bytes = img_resp.content

                cost = 0.003  # Estimated cost for flux-schnell

                return ImageResult(
                    image_bytes=image_bytes,
                    width=width,
                    height=height,
                    format="PNG",
                    cost_usd=cost,
                    provider="replicate",
                    model=model_name,
                    metadata={"raw_output": image_url},
                )
        except Exception as e:
            logger.error(f"Replicate Image Generation error: {e}. Falling back to StubProvider.")
            stub_result = await self.stub_fallback.generate(prompt, **kwargs)
            stub_result.metadata["replicate_error"] = str(e)
            return stub_result
