"""
TeeDesign AI — Autonomous Production Agents Package
"""
import sys
from pathlib import Path

# Ensure both backend root and agents directory are in sys.path
_current_dir = Path(__file__).resolve().parent
_backend_dir = _current_dir.parent
_repo_root = _backend_dir.parent

for p in [str(_current_dir), str(_backend_dir), str(_repo_root)]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
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
except (ImportError, ValueError):
    from base_agent import BaseAgent, AgentResult, StubLLMClient
    from ceo_agent import CEOAgent
    from research_agent import ResearchAgent
    from creative_agent import CreativeAgent, CreativeAgent as CreativeDirectorAgent
    from generator_agent import GeneratorAgent, GeneratorAgent as IllustrationGeneratorAgent
    from quality_agent import QualityAgent, QualityAgent as QualityControlAgent
    from compliance_agent import ComplianceAgent
    from seo_agent import SEOAgent
    from portfolio_agent import PortfolioAgent, ExportPackage
    from analytics_agent import AnalyticsAgent

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

# If Streamlit is running this file directly as the entry point:
if "streamlit" in sys.modules:
    try:
        app_file = _repo_root / "streamlit_app.py"
        if app_file.exists():
            with open(app_file, encoding="utf-8") as _f:
                _code = compile(_f.read(), str(app_file), "exec")
                exec(_code, globals())
    except Exception as _e:
        import streamlit as _st
        _st.error(f"Error loading dashboard: {_e}")
