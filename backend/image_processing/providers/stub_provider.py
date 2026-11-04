"""
TeeDesign AI — Stub Image Provider (Mock mode using Pillow)
"""
import io
import math
from typing import Any
from PIL import Image, ImageDraw, ImageFont

from image_processing.providers.base_provider import BaseImageProvider, ImageResult


class StubProvider(BaseImageProvider):
    """Generates synthetic test illustration images using Pillow without external API calls."""

    def __init__(self, api_key: str | None = None, model: str | None = None):
        super().__init__(api_key, model or "pillow-stub")

    async def generate(self, prompt: str, **kwargs: Any) -> ImageResult:
        width = int(kwargs.get("width", 1024))
        height = int(kwargs.get("height", 1024))

        # Create RGBA image with transparent background
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Draw decorative circular badges and geometric tee illustration elements
        center_x, center_y = width // 2, height // 2
        radius = min(width, height) // 3

        # Outer glowing circles
        colors = [
            (255, 107, 107, 180),  # Coral
            (78, 205, 196, 180),   # Teal
            (255, 190, 11, 200),   # Yellow
            (131, 56, 236, 220),   # Purple
        ]

        for i, color in enumerate(colors):
            r = radius - (i * 25)
            if r > 0:
                draw.ellipse(
                    [center_x - r, center_y - r, center_x + r, center_y + r],
                    outline=color,
                    width=6,
                )

        # Draw decorative stars / sparkles around
        for angle_deg in range(0, 360, 45):
            rad = math.radians(angle_deg)
            dist = radius + 40
            sx = int(center_x + dist * math.cos(rad))
            sy = int(center_y + dist * math.sin(rad))
            draw.regular_polygon((sx, sy, 16), 5, fill=(255, 215, 0, 220))

        # Banner box for label
        box_top = center_y - 60
        box_bottom = center_y + 60
        box_left = max(20, center_x - 380)
        box_right = min(width - 20, center_x + 380)

        draw.rounded_rectangle(
            [box_left, box_top, box_right, box_bottom],
            radius=16,
            fill=(24, 24, 27, 230),
            outline=(255, 107, 107, 255),
            width=3,
        )

        # Text labels
        try:
            # Try default or standard PIL font
            font = ImageFont.load_default()
        except Exception:
            font = None

        text_title = "STUB MODE - Configure API Key"
        truncated_prompt = prompt[:60] + "..." if len(prompt) > 60 else prompt
        text_sub = f"Prompt: {truncated_prompt}"
        text_dim = f"TeeDesign AI Mock Canvas: {width}x{height}"

        # Center texts
        draw.text(
            (center_x, center_y - 30),
            text_title,
            fill=(255, 220, 100, 255),
            anchor="mm",
            font=font,
        )
        draw.text(
            (center_x, center_y),
            text_sub,
            fill=(240, 240, 240, 230),
            anchor="mm",
            font=font,
        )
        draw.text(
            (center_x, center_y + 30),
            text_dim,
            fill=(180, 180, 180, 200),
            anchor="mm",
            font=font,
        )

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        image_bytes = buffer.getvalue()

        return ImageResult(
            image_bytes=image_bytes,
            width=width,
            height=height,
            format="PNG",
            cost_usd=0.0,
            provider="stub",
            model="pillow-stub",
            metadata={
                "is_stub": True,
                "prompt": prompt,
                "note": "Mock illustration generated locally via Pillow",
            },
        )
