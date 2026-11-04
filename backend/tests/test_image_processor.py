"""
Unit tests for Image Processing Engine
"""
import pytest
import os
from PIL import Image
from image_processing.processor import ImageProcessor


def test_image_dimension_validation(tmp_path):
    # Create test PNG image
    test_img_path = str(tmp_path / "test_artwork.png")
    img = Image.new("RGBA", (1024, 1024), (255, 0, 0, 255))
    img.save(test_img_path, "PNG")

    processor = ImageProcessor()
    dims = processor.validate_dimensions(test_img_path)
    assert dims["is_valid"] is True
    assert dims["width"] == 1024
    assert dims["height"] == 1024


def test_image_transparency_validation(tmp_path):
    # Image with transparent alpha
    transparent_path = str(tmp_path / "transparent.png")
    img = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
    img.save(transparent_path, "PNG")

    processor = ImageProcessor()
    has_trans = processor.validate_transparency(transparent_path)
    assert has_trans is True

    # Opaque image
    opaque_path = str(tmp_path / "opaque.png")
    img_op = Image.new("RGB", (200, 200), (255, 255, 255))
    img_op.save(opaque_path, "PNG")
    has_trans_op = processor.validate_transparency(opaque_path)
    assert has_trans_op is False
