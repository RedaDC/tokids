"""
TeeDesign AI — Portfolio Manager Agent
"""
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from .base_agent import AgentResult, BaseAgent
from app.models.agent import AgentStatus
from app.services.storage_service import storage_service
from image_processing.processor import processor


@dataclass
class ExportPackage:
    design_id: str
    collection_name: str
    master_path: str
    export_path: str
    preview_path: str
    dimensions: dict[str, int]
    file_size_bytes: int
    ready_for_upload: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)


class PortfolioAgent(BaseAgent):
    """Portfolio Agent: Organizes collections, manages versions, prevents duplication, and builds export archives."""

    def __init__(self):
        super().__init__(
            name="Portfolio Manager",
            role="Catalog Architect & Asset Packaging Specialist",
            description="Maintains design version integrity, tags collection categories, and builds master print bundles.",
        )

    def organize_design(self, design_id: str, niche: str) -> dict[str, Any]:
        """Categorize design into a curated niche collection."""
        collection_slug = niche.lower().replace(" ", "-")
        self.log(f"Assigned design {design_id} to collection '{collection_slug}'")
        return {
            "design_id": design_id,
            "collection_slug": collection_slug,
            "collection_name": niche.title(),
        }

    def check_for_duplicates(self, design_id: str, existing_ids: list[str]) -> bool:
        """Verify design uniqueness across current catalog."""
        return design_id in existing_ids

    def prepare_export_package(
        self,
        design_id: str,
        file_path: str,
        collection_name: str = "General",
    ) -> ExportPackage:
        """Render high-resolution print-ready 5000x5500 master package."""
        storage_service.ensure_directories()
        export_filename = f"design_{design_id}_print_5000x5500.png"
        export_full_path = storage_service.export_dir / export_filename

        # Render print canvas
        rendered_export_path = processor.prepare_export(
            image_path=file_path,
            output_path=export_full_path,
            width=5000,
            height=5500,
        )

        size_bytes = processor.check_file_size(rendered_export_path)

        return ExportPackage(
            design_id=str(design_id),
            collection_name=collection_name,
            master_path=str(file_path),
            export_path=str(rendered_export_path),
            preview_path=str(file_path),
            dimensions={"width": 5000, "height": 5500},
            file_size_bytes=size_bytes,
            ready_for_upload=True,
            metadata={"print_substrate": "Direct-to-Garment DTG", "dpi": 300},
        )

    async def execute(self, task_input: dict[str, Any]) -> AgentResult:
        start_time = time.time()
        self.status = AgentStatus.WORKING

        design_id = str(task_input.get("design_id") or uuid.uuid4().hex[:8])
        file_path = task_input.get("file_path") or ""
        niche = task_input.get("niche") or "Featured Collection"

        self.log(f"Assembling master export package for design: {design_id}")

        collection_info = self.organize_design(design_id, niche)

        export_pkg = None
        if file_path and Path(file_path).exists():
            pkg = self.prepare_export_package(
                design_id=design_id,
                file_path=file_path,
                collection_name=niche,
            )
            export_pkg = {
                "design_id": pkg.design_id,
                "collection_name": pkg.collection_name,
                "master_path": pkg.master_path,
                "export_path": pkg.export_path,
                "preview_path": pkg.preview_path,
                "dimensions": pkg.dimensions,
                "file_size_bytes": pkg.file_size_bytes,
                "ready_for_upload": pkg.ready_for_upload,
            }

        output = {
            "collection": collection_info,
            "export_package": export_pkg,
            "version_number": 1,
            "archive_status": "ready_for_distribution",
        }

        self.status = AgentStatus.COMPLETED
        elapsed_ms = (time.time() - start_time) * 1000

        self.log(f"Portfolio packaging completed for {design_id}.")

        return AgentResult(
            success=True,
            output=output,
            cost_usd=0.0,
            tokens_used=0,
            execution_time_ms=elapsed_ms,
        )
