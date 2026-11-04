"""
TeeDesign AI — Autonomous Production Agents Package
"""
import sys
from pathlib import Path

# Ensure backend directory is in sys.path for robust imports across all environments
_backend_dir = str(Path(__file__).resolve().parent.parent)
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

from .base_agent import BaseAgent, AgentResult, StubLLMClient
from .ceo_agent import CEOAgent
from .research_agent import ResearchAgent
from .creative_agent import CreativeAgent, CreativeAgent as CreativeDirectorAgent
from .generator_agent import GeneratorAgent, GeneratorAgent as IllustrationGeneratorAgent
from .quality_agent import QualityAgent, QualityAgent as QualityControlAgent
from .compliance_agent import ComplianceAgent
from .seo_agent import SEOAgent
from .portfolio_agent import PortfolioAgent, ExportPackage
from .analytics_agent import AnalyticsAgent

__all__ = [
    "BaseAgent",
    "AgentResult",
    "StubLLMClient",
    "CEOAgent",
    "ResearchAgent",
    "CreativeAgent",
    "CreativeDirectorAgent",
    "GeneratorAgent",
    "IllustrationGeneratorAgent",
    "QualityAgent",
    "QualityControlAgent",
    "ComplianceAgent",
    "SEOAgent",
    "PortfolioAgent",
    "ExportPackage",
    "AnalyticsAgent",
]
