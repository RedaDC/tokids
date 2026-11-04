"""
TeeDesign AI — Image Processor (Pillow & OpenCV utilities)
"""
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional
from PIL import Image

from app.core.config import settings


@dataclass
class ProcessingResult:
    is_valid: bool
    has_transparency: bool
    dimensions: dict[str, Any]
    file_size_bytes: int
    preview_path: Optional[str] = None
    export_path: Optional[str] = None
    errors: list[str] = field(default_factory=list)


class ImageProcessor:
    """Utilities for preparing, validating, and optimizing print-ready t-shirt graphics."""

    @staticmethod
    def validate_transparency(image_path: str | Path) -> bool:
        """Check if image has an alpha channel with at least some transparent or semi-transparent pixels."""
        try:
            with Image.open(image_path) as img:
                if img.mode not in ("RGBA", "LA") and "transparency" not in img.info:
                    return False
                alpha = img.convert("RGBA").split()[-1]
                # If minimum alpha is less than 255, image has transparent areas
                min_alpha, max_alpha = alpha.getextrema()
                return min_alpha < 250
        except Exception:
            return False

    @staticmethod
    def validate_dimensions(image_path: str | Path) -> dict[str, Any]:
        """Extract dimension, format, and aspect ratio metadata."""
        try:
            with Image.open(image_path) as img:
                w, h = img.size
                return {
                    "width": w,
                    "height": h,
                    "aspect_ratio": round(w / h, 3) if h > 0 else 1.0,
                    "format": img.format or "PNG",
                    "mode": img.mode,
                }
        except Exception as e:
            return {"error": str(e), "width": 0, "height": 0}

    @staticmethod
    def create_preview(
        image_path: str | Path,
        output_path: str | Path,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> str:
        """Generate web-optimized preview thumbnail preserving aspect ratio."""
        target_w = width or settings.PREVIEW_WIDTH or 600
        target_h = height or settings.PREVIEW_HEIGHT or 600

        out_path = Path(output_path).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)

        with Image.open(image_path) as img:
            preview_img = img.copy()
            preview_img.thumbnail((target_w, target_h), Image.Resampling.LANCZOS)
            preview_img.save(out_path, format="PNG", optimize=True)

        return str(out_path)

    @staticmethod
    def prepare_export(
        image_path: str | Path,
        output_path: str | Path,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> str:
        """
        Produce master print export canvas (default 5000x5500) preserving design aspect ratio
        and centering it on a transparent canvas.
        """
        canvas_w = width or settings.EXPORT_WIDTH or 5000
        canvas_h = height or settings.EXPORT_HEIGHT or 5500

        out_path = Path(output_path).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)

        with Image.open(image_path) as img:
            src = img.convert("RGBA")
            src_w, src_h = src.size

            # Compute scale ratio to fit nicely inside canvas with a small margin (92% of canvas)
            max_design_w = int(canvas_w * 0.92)
            max_design_h = int(canvas_h * 0.92)

            scale = min(max_design_w / src_w, max_design_h / src_h)
            new_w = max(1, int(src_w * scale))
            new_h = max(1, int(src_h * scale))

            resized = src.resize((new_w, new_h), Image.Resampling.LANCZOS)

            # Create transparent canvas
            canvas = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))

            # Paste centered
            offset_x = (canvas_w - new_w) // 2
            offset_y = (canvas_h - new_h) // 2
            canvas.paste(resized, (offset_x, offset_y), mask=resized)

            canvas.save(out_path, format="PNG")

        return str(out_path)

    @staticmethod
    def check_file_size(image_path: str | Path) -> int:
        """Return file size in bytes."""
        try:
            return os.path.getsize(image_path)
        except Exception:
            return 0

    @classmethod
    def process_for_library(
        cls,
        image_path: str | Path,
        preview_output_path: Optional[str | Path] = None,
        export_output_path: Optional[str | Path] = None,
    ) -> ProcessingResult:
        """Full pipeline verification, preview generation, and export packaging."""
        errors: list[str] = []
        path = Path(image_path)

        if not path.exists():
            return ProcessingResult(
                is_valid=False,
                has_transparency=False,
                dimensions={"width": 0, "height": 0},
                file_size_bytes=0,
                errors=[f"File does not exist: {image_path}"],
            )

        dims = cls.validate_dimensions(path)
        has_transparency = cls.validate_transparency(path)
        file_size = cls.check_file_size(path)

        preview_saved_path = None
        if preview_output_path:
            try:
                preview_saved_path = cls.create_preview(path, preview_output_path)
            except Exception as e:
                errors.append(f"Preview generation failed: {e}")

        export_saved_path = None
        if export_output_path:
            try:
                export_saved_path = cls.prepare_export(path, export_output_path)
            except Exception as e:
                errors.append(f"Export preparation failed: {e}")

        is_valid = len(errors) == 0 and dims.get("width", 0) > 0

        return ProcessingResult(
            is_valid=is_valid,
            has_transparency=has_transparency,
            dimensions=dims,
            file_size_bytes=file_size,
            preview_path=preview_saved_path,
            export_path=export_saved_path,
            errors=errors,
        )


processor = ImageProcessor()
