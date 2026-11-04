"""
TeeDesign AI — All Agents Module Re-export
Provides backward-compatible access for `from agents.agents import ...`
"""
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
