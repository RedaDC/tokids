"""
Unit tests for AI Agents in Stub Mode
"""
import pytest
from agents.agents import (
    ResearchAgent,
    CreativeDirectorAgent,
    QualityControlAgent,
    ComplianceAgent,
    SEOAgent,
)


@pytest.mark.asyncio
async def test_research_agent_stub():
    agent = ResearchAgent()
    result = await agent.execute_with_tracking({"query": "Space Cats", "num_niches": 2})
    assert result.success is True
    assert "niches" in result.output
    assert len(result.output["niches"]) > 0


@pytest.mark.asyncio
async def test_creative_agent_stub():
    agent = CreativeDirectorAgent()
    result = await agent.execute_with_tracking({"niche": "Vintage Nature", "style": "retro"})
    assert result.success is True
    assert "concepts" in result.output
    assert len(result.output["concepts"]) > 0


@pytest.mark.asyncio
async def test_compliance_agent_flags():
    agent = ComplianceAgent()
    # Test high risk trigger
    result = await agent.execute_with_tracking({
        "generation_prompt": "A cute Mickey mouse wearing a Disney cape",
    })
    assert result.success is True
    assert result.output["risk_level"] == "high"
    assert len(result.output["flags"]) > 0


@pytest.mark.asyncio
async def test_seo_agent_stub():
    agent = SEOAgent()
    result = await agent.execute_with_tracking({
        "title": "Cosmic Tabby Cat",
        "description": "An astronaut cat in a starry cosmos",
        "niche": "Space",
    })
    assert result.success is True
    assert "title" in result.output
    assert "tags" in result.output
    assert len(result.output["tags"]) > 0
