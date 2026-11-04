"""
TeeDesign AI — Base Agent Architecture and LLM Client
"""
import json
import logging
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional

from app.core.config import settings
from app.models.agent import AgentStatus

logger = logging.getLogger(__name__)


@dataclass
class AgentResult:
    success: bool
    output: dict[str, Any]
    error: Optional[str] = None
    cost_usd: float = 0.0
    tokens_used: int = 0
    execution_time_ms: float = 0.0


class StubLLMClient:
    """Stub LLM Client producing realistic mock structured outputs."""

    def __init__(self):
        self.is_stub = True

    async def complete(self, prompt: str, system: Optional[str] = None) -> str:
        logger.info(f"[STUB LLM] Generating completion for prompt: {prompt[:80]}...")
        return f"[STUB MODE response for: {prompt[:40]}]"

    async def generate_json(self, prompt: str, system: Optional[str] = None) -> dict[str, Any]:
        logger.info(f"[STUB LLM] Generating structured JSON for prompt: {prompt[:80]}...")
        return {
            "mode": "stub",
            "message": "Realistic stub structured output",
            "prompt_received": prompt[:100],
        }


class RealLLMClient:
    """OpenAI / Anthropic async LLM wrapper."""

    def __init__(self, provider: str = "openai"):
        self.provider = provider
        self.openai_key = settings.OPENAI_API_KEY
        self.anthropic_key = settings.ANTHROPIC_API_KEY

    async def complete(self, prompt: str, system: Optional[str] = None) -> str:
        if self.provider == "anthropic" and self.anthropic_key:
            from anthropic import AsyncAnthropic
            client = AsyncAnthropic(api_key=self.anthropic_key)
            messages = [{"role": "user", "content": prompt}]
            kwargs: dict[str, Any] = {
                "model": settings.ANTHROPIC_MODEL,
                "max_tokens": 2048,
                "messages": messages,
            }
            if system:
                kwargs["system"] = system
            resp = await client.messages.create(**kwargs)
            return resp.content[0].text

        elif self.openai_key:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=self.openai_key)
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})
            resp = await client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=messages,
                max_tokens=settings.OPENAI_MAX_TOKENS,
            )
            return resp.choices[0].message.content or ""

        # Fallback to stub if keys missing
        stub = StubLLMClient()
        return await stub.complete(prompt, system)

    async def generate_json(self, prompt: str, system: Optional[str] = None) -> dict[str, Any]:
        raw_text = await self.complete(prompt, system)
        try:
            # Strip markdown code blocks if wrapped
            clean = raw_text.strip()
            if clean.startswith("```json"):
                clean = clean[7:]
            elif clean.startswith("```"):
                clean = clean[3:]
            if clean.endswith("```"):
                clean = clean[:-3]
            return json.loads(clean.strip())
        except Exception:
            return {"raw_text": raw_text}


class BaseAgent(ABC):
    """Abstract base class for all autonomous production agents."""

    def __init__(
        self,
        name: str,
        role: str,
        description: str = "",
        agent_id: Optional[uuid.UUID] = None,
    ):
        self.id = agent_id or uuid.uuid4()
        self.name = name
        self.role = role
        self.description = description
        self.status = AgentStatus.IDLE
        self.cost_usd: float = 0.0
        self.tokens_used: int = 0
        self.logs: list[dict[str, Any]] = []

    def log(self, message: str, level: str = "info", task_id: Optional[str] = None) -> None:
        """Record agent log event."""
        log_entry = {
            "timestamp": time.time(),
            "level": level,
            "agent": self.name,
            "message": message,
            "task_id": task_id,
        }
        self.logs.append(log_entry)
        log_func = getattr(logger, level.lower(), logger.info)
        log_func(f"[{self.name}] {message}")

    def track_cost(self, usd: float, tokens: int = 0) -> None:
        """Increment cost and token counters."""
        self.cost_usd += usd
        self.tokens_used += tokens

    def get_llm_client(self) -> Any:
        """Return configured LLM client or stub client."""
        if settings.is_stub_mode or (not settings.OPENAI_API_KEY and not settings.ANTHROPIC_API_KEY):
            return StubLLMClient()
        return RealLLMClient(provider=settings.LLM_PROVIDER)

    @abstractmethod
    async def execute(self, task_input: dict[str, Any]) -> AgentResult:
        """Execute agent task workflow."""
        pass
