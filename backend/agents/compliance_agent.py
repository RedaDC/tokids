"""
TeeDesign AI — Copyright & Trademark Compliance Agent
"""
import re
import time
from typing import Any
from agents.base_agent import AgentResult, BaseAgent
from app.models.agent import AgentStatus
from app.models.quality import ComplianceRiskLevel

# High-risk IP terms frequently subject to takedown notices on POD marketplaces
FLAGGED_IP_PATTERNS = [
    r"\b(disney|marvel|star wars|pokemon|pikachu|mickey mouse|nintendo|mario|zelda)\b",
    r"\b(harry potter|hogwarts|batman|superman|dc comics|avengers|iron man)\b",
    r"\b(nike|adidas|gucci|chanel|louis vuitton|supreme|apple|coca cola)\b",
    r"\b(anime studio ghibli|totoro|dragon ball|goku|naruto|one piece)\b",
]


class ComplianceAgent(BaseAgent):
    """Compliance Agent: Scans prompts, metadata, and concepts for trademark & copyright infringement risks."""

    def __init__(self):
        super().__init__(
            name="Copyright Compliance Specialist",
            role="IP Risk & Trademark Clearance Screener",
            description="Protects against IP infringement, brand dilution, and marketplace takedown violations.",
        )

    async def execute(self, task_input: dict[str, Any]) -> AgentResult:
        start_time = time.time()
        self.status = AgentStatus.WORKING

        text_to_scan = " ".join([
            str(task_input.get("prompt", "")),
            str(task_input.get("generation_prompt", "")),
            str(task_input.get("concept_title", "")),
            str(task_input.get("title", "")),
            str(task_input.get("description", "")),
            str(task_input.get("niche", "")),
        ]).lower()

        self.log(f"Screening design assets and text for trademark infringement risks...")

        flags: list[str] = []
        for pattern in FLAGGED_IP_PATTERNS:
            matches = re.findall(pattern, text_to_scan)
            if matches:
                flags.extend([f"Potential registered trademark matched: '{m}'" for m in set(matches)])

        if len(flags) == 0:
            risk_level = ComplianceRiskLevel.LOW.value
            is_cleared = True
            notes = "No registered trademark or high-risk protected franchise keywords detected in assets."
        elif len(flags) == 1:
            risk_level = ComplianceRiskLevel.MEDIUM.value
            is_cleared = True  # Flagged for advisory human review without hard blocking
            notes = "Advisory notice: Potential trademark reference detected. Recommended for human review."
        else:
            risk_level = ComplianceRiskLevel.HIGH.value
            is_cleared = False
            notes = "Multiple high-risk trademark flags detected. Halting auto-publishing pending legal verification."

        disclaimer = "Automated screening does not guarantee legal clearance. Always perform manual trademark checks with USPTO / WIPO."

        output = {
            "risk_level": risk_level,
            "flags": flags,
            "is_cleared": is_cleared,
            "review_notes": f"{notes} | {disclaimer}",
            "disclaimer": disclaimer,
        }

        self.status = AgentStatus.COMPLETED
        elapsed_ms = (time.time() - start_time) * 1000

        self.log(f"Compliance screening complete: Risk={risk_level.upper()}, Cleared={is_cleared}")

        return AgentResult(
            success=True,
            output=output,
            cost_usd=0.0005,
            tokens_used=50,
            execution_time_ms=elapsed_ms,
        )
