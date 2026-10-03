"""Any endpoint speaking the OpenAI ``/v1/chat/completions`` protocol.

That covers DeepSeek, OpenAI, GLM and the local runtimes (Ollama, vLLM,
llama.cpp server, LM Studio) — they differ only in ``base_url``, model name
and whether a key is needed, all of which come from config.
"""

from __future__ import annotations

import time

from mra.models.providers.base import Completion, KeyedProvider, Message


class OpenAICompatibleProvider(KeyedProvider):
    @property
    def client(self):
        if self._client is None:
            from openai import OpenAI  # lazy: the deterministic path never imports it

            # The SDK refuses an empty key; a keyless local server ignores this one.
            self._client = OpenAI(
                api_key=self.api_key or "not-needed", base_url=self.base_url, timeout=self.timeout_s
            )
        return self._client

    def complete(
        self, messages: list[Message], model: str, temperature: float, max_tokens: int
    ) -> Completion:
        started = time.perf_counter()
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        usage = getattr(response, "usage", None)
        return Completion(
            text=response.choices[0].message.content or "",
            tokens_in=int(getattr(usage, "prompt_tokens", 0) or 0),
            tokens_out=int(getattr(usage, "completion_tokens", 0) or 0),
            provider=self.name,
            model=model,
            latency_s=time.perf_counter() - started,
        )
