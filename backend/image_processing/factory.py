"""
TeeDesign AI — Image Provider Factory
"""
from typing import Optional
from app.core.config import settings
from image_processing.providers.base_provider import BaseImageProvider
from image_processing.providers.openai_provider import OpenAIProvider
from image_processing.providers.replicate_provider import ReplicateProvider
from image_processing.providers.stub_provider import StubProvider


def get_image_provider(
    provider_name: Optional[str] = None,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
) -> BaseImageProvider:
    """Factory function returning the configured image generation provider."""
    target_provider = (provider_name or settings.IMAGE_PROVIDER or "stub").lower()

    if target_provider == "openai":
        return OpenAIProvider(api_key=api_key, model=model)
    elif target_provider == "replicate":
        return ReplicateProvider(api_key=api_key, model=model)
    else:
        return StubProvider(api_key=api_key, model=model)
