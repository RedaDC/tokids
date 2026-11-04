"""
TeeDesign AI — Storage Service
"""
import os
import shutil
from pathlib import Path
from typing import Optional
import aiofiles

from app.core.config import settings


class StorageService:
    def __init__(self):
        self.base_dir = Path(settings.STORAGE_PATH).resolve()
        self.master_dir = Path(settings.MASTER_FILES_PATH).resolve()
        self.approved_dir = Path(settings.APPROVED_FILES_PATH).resolve()
        self.preview_dir = Path(settings.PREVIEWS_PATH).resolve()
        self.export_dir = Path(settings.EXPORTS_PATH).resolve()

    def ensure_directories(self) -> None:
        """Create storage directories if they don't exist."""
        for directory in [
            self.base_dir,
            self.master_dir,
            self.approved_dir,
            self.preview_dir,
            self.export_dir,
        ]:
            directory.mkdir(parents=True, exist_ok=True)

    async def save_file(
        self,
        content: bytes,
        directory: str | Path,
        filename: str,
    ) -> str:
        """Asynchronously save bytes content to disk and return absolute path."""
        target_dir = Path(directory).resolve()
        target_dir.mkdir(parents=True, exist_ok=True)
        file_path = target_dir / filename

        async with aiofiles.open(file_path, "wb") as f:
            await f.write(content)

        return str(file_path)

    def delete_file(self, file_path: str | Path) -> bool:
        """Delete a file from disk if it exists."""
        try:
            path = Path(file_path).resolve()
            if path.exists() and path.is_file():
                path.unlink()
                return True
        except Exception:
            return False
        return False

    def get_file_url(self, file_path: str | Path) -> str:
        """Generate static file relative URL for serving via API."""
        try:
            path = Path(file_path).resolve()
            rel_path = path.relative_to(self.base_dir)
            return f"/assets/{rel_path.as_posix()}"
        except Exception:
            return str(file_path)

    def get_file_bytes(self, file_path: str | Path) -> Optional[bytes]:
        """Read bytes from file."""
        try:
            path = Path(file_path).resolve()
            if path.exists():
                return path.read_bytes()
        except Exception:
            pass
        return None


storage_service = StorageService()
