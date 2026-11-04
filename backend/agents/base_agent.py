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

logger = logging.getLogger(__name__)

try:
    from app.core.config import settings as _settings
except Exception:
    _settings = None  # type: ignore

try:
    from app.models.agent import AgentStatus
except Exception:
    import enum
    class AgentStatus(str, enum.Enum):  # type: ignore
        IDLE = "idle"
        WORKING = "working"
        COMPLETED = "completed"
        FAILED = "failed"

__all__ = ["BaseAgent", "AgentResult", "StubLLMClient", "AgentStatus"]


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
        openai_key = _settings.OPENAI_API_KEY if _settings else ""
        anthropic_key = _settings.ANTHROPIC_API_KEY if _settings else ""
        self.openai_key = openai_key
        self.anthropic_key = anthropic_key

    async def complete(self, prompt: str, system: Optional[str] = None) -> str:
        if self.provider == "anthropic" and self.anthropic_key:
            from anthropic import AsyncAnthropic
            client = AsyncAnthropic(api_key=self.anthropic_key)
            messages = [{"role": "user", "content": prompt}]
            kwargs: dict[str, Any] = {
                "model": _settings.ANTHROPIC_MODEL if _settings else "claude-3-5-sonnet-20241022",
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
                model=_settings.OPENAI_MODEL if _settings else "gpt-4o",
                messages=messages,
                max_tokens=_settings.OPENAI_MAX_TOKENS if _settings else 4096,
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
        """Return configured LLM client or stub client (public method)."""
        is_stub = (not _settings) or getattr(_settings, "is_stub_mode", True)
        openai_key = _settings.OPENAI_API_KEY if _settings else ""
        anthropic_key = _settings.ANTHROPIC_API_KEY if _settings else ""
        if is_stub or (not openai_key and not anthropic_key):
            return StubLLMClient()
        provider = _settings.LLM_PROVIDER if _settings else "openai"
        return RealLLMClient(provider=provider)

    # Alias used by agents.py monolithic-style agents
    def _get_llm_client(self) -> Any:
        return self.get_llm_client()

    @property
    def _is_stub(self) -> bool:
        """True when running without real API keys configured."""
        client = self.get_llm_client()
        return isinstance(client, StubLLMClient)

    def _log_activity(self, message: str, level: str = "info", **kwargs: Any) -> None:
        """Log activity (wrapper used by agents.py agents)."""
        self.log(message, level=level)

    async def execute_with_tracking(self, task_input: dict[str, Any]) -> "AgentResult":
        """Execute with timing and cost tracking."""
        start = time.time()
        try:
            result = await self.execute(task_input)
            result.execution_time_ms = (time.time() - start) * 1000
            self.track_cost(result.cost_usd, result.tokens_used)
            return result
        except Exception as e:
            elapsed = (time.time() - start) * 1000
            self.log(f"Agent execution error: {e}", level="error")
            return AgentResult(
                success=False,
                output={},
                error=str(e),
                execution_time_ms=elapsed,
            )

    async def _call_llm(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        response_format: str = "text",
    ) -> dict[str, Any]:
        """Call LLM and return structured result dict."""
        client = self.get_llm_client()
        try:
            if response_format == "json":
                data = await client.generate_json(prompt, system=system_prompt)
                return {"content": json.dumps(data) if isinstance(data, dict) else data, "raw": data}
            else:
                text = await client.complete(prompt, system=system_prompt)
                return {"content": text}
        except Exception as e:
            return {"content": "{}", "error": str(e)}

    @abstractmethod
    async def execute(self, task_input: dict[str, Any]) -> AgentResult:
        """Execute agent task workflow."""
        pass
