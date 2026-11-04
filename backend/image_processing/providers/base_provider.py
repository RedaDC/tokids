"""
TeeDesign AI — Base Image Provider Interface
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class ImageResult:
    image_bytes: bytes
    width: int
    height: int
    format: str = "PNG"
    cost_usd: float = 0.0
    provider: str = "stub"
    model: str = "stub-model"
    metadata: dict[str, Any] = field(default_factory=dict)


class BaseImageProvider(ABC):
    """Abstract base class for all image generation providers."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key
        self.model = model

    @abstractmethod
    async def generate(self, prompt: str, **kwargs: Any) -> ImageResult:
        """Generate an image from prompt and return ImageResult."""
        pass
