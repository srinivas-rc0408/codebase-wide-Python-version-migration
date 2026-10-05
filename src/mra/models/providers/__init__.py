"""LLM providers: one call shape over every backend the agent can use.

A provider knows *how* to reach a backend; it never chooses a model. Model
names, base URLs and key variable names all come from ``mra.toml`` (see
CONFIGURATION.md §3) and are passed in, so nothing here names a model.
"""

from __future__ import annotations

from typing import Any

from mra.models.providers.anthropic_sdk import AnthropicProvider
from mra.models.providers.base import Completion, Message, Provider
from mra.models.providers.fake import FakeProvider
from mra.models.providers.openai_compatible import OpenAICompatibleProvider

KINDS: dict[str, Any] = {
    "openai-compatible": OpenAICompatibleProvider,
    "anthropic": AnthropicProvider,
    "fake": FakeProvider,
}


def make_provider(name: str, entry: dict[str, Any]) -> Provider:
    """Build the provider for one ``[providers.<name>]`` table of ``mra.toml``."""
    kind = entry.get("provider")
    if kind not in KINDS:
        raise ValueError(f"providers.{name}: provider must be one of {sorted(KINDS)}, got {kind!r}")
    if kind == "fake":
        return FakeProvider(name=name)
    if not entry.get("base_url"):
        raise ValueError(f"providers.{name}: base_url is required")
    return KINDS[kind](
        name=name,
        base_url=entry["base_url"],
        api_key_env=entry.get("api_key_env"),
        api_key_envs=entry.get("api_key_envs"),
        timeout_s=float(entry.get("timeout_s", 120)),
        max_retries=int(entry.get("max_retries", 2)),
    )


__all__ = [
    "KINDS",
    "AnthropicProvider",
    "Completion",
    "FakeProvider",
    "Message",
    "OpenAICompatibleProvider",
    "Provider",
    "make_provider",
]
