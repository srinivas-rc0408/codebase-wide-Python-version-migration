"""The provider contract and the key lookup every networked provider shares."""

from __future__ import annotations

import os
from typing import Protocol, TypedDict

Message = dict[str, str]  # {"role": "system" | "user" | "assistant", "content": ...}


class Completion(TypedDict):
    text: str
    tokens_in: int
    tokens_out: int
    provider: str
    model: str
    latency_s: float


class Provider(Protocol):
    name: str
    #: ``None`` only for a provider that does no network I/O at all.
    base_url: str | None

    @property
    def available(self) -> bool: ...

    def complete(self, messages: list[Message], model: str, temperature: float,
                 max_tokens: int) -> Completion: ...


class KeyedProvider:
    """Common state: where it lives, which env var holds its key, how long to wait.

    ``api_key_env`` is the *name* of an environment variable, never a key
    (golden rule 2). ``None`` means the runtime needs no key — a local server.
    """

    def __init__(self, *, name: str, base_url: str, api_key_env: str | None = None,
                 timeout_s: float = 120.0) -> None:
        self.name = name
        self.base_url = base_url
        self.api_key_env = api_key_env
        self.timeout_s = timeout_s
        self._client = None

    @property
    def api_key(self) -> str | None:
        return os.getenv(self.api_key_env) if self.api_key_env else None

    @property
    def available(self) -> bool:
        return self.api_key_env is None or bool(self.api_key)
