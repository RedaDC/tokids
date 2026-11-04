"""
TeeDesign AI — OpenAI DALL-E 3 Image Provider
"""
import base64
import logging
from typing import Any, Optional
import httpx
from openai import AsyncOpenAI

from app.core.config import settings
from image_processing.providers.base_provider import BaseImageProvider, ImageResult
from image_processing.providers.stub_provider import StubProvider

logger = logging.getLogger(__name__)


class OpenAIProvider(BaseImageProvider):
    """Generates images using OpenAI DALL-E 3 API."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        resolved_key = api_key or settings.OPENAI_API_KEY
        resolved_model = model or settings.DALLE_MODEL or "dall-e-3"
        super().__init__(resolved_key, resolved_model)
        self.stub_fallback = StubProvider()

    async def generate(self, prompt: str, **kwargs: Any) -> ImageResult:
        if not self.api_key:
            logger.warning("OpenAI API key missing. Falling back to StubProvider.")
            return await self.stub_fallback.generate(prompt, **kwargs)

        size = kwargs.get("size", settings.DALLE_SIZE or "1024x1024")
        quality = kwargs.get("quality", settings.DALLE_QUALITY or "standard")

        # Parse width/height from size string
        try:
            parts = size.split("x")
            width, height = int(parts[0]), int(parts[1])
        except Exception:
            width, height = 1024, 1024

        client = AsyncOpenAI(api_key=self.api_key)

        try:
            response = await client.images.generate(
                model=self.model or "dall-e-3",
                prompt=prompt,
                n=1,
                size=size,  # type: ignore
                quality=quality,  # type: ignore
                response_format="b64_json",
            )

            img_data = response.data[0]
            if img_data.b64_json:
                image_bytes = base64.b64decode(img_data.b64_json)
            elif img_data.url:
                async with httpx.AsyncClient() as http_client:
                    r = await http_client.get(img_data.url, timeout=30.0)
                    r.raise_for_status()
                    image_bytes = r.content
            else:
                raise ValueError("No image content returned from OpenAI API.")

            # DALL-E 3 standard is $0.040, HD is $0.080 for 1024x1024
            cost = 0.080 if quality == "hd" else 0.040

            return ImageResult(
                image_bytes=image_bytes,
                width=width,
                height=height,
                format="PNG",
                cost_usd=cost,
                provider="openai",
                model=self.model or "dall-e-3",
                metadata={
                    "revised_prompt": getattr(img_data, "revised_prompt", prompt),
                    "quality": quality,
                    "size": size,
                },
            )
        except Exception as e:
            logger.error(f"OpenAI Image Generation error: {e}. Falling back to StubProvider.")
            stub_result = await self.stub_fallback.generate(prompt, **kwargs)
            stub_result.metadata["openai_error"] = str(e)
            return stub_result
