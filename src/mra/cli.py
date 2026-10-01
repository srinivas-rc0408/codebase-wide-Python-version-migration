"""The ``mra`` command. ``mra providers check`` pings every configured provider.

An unreachable provider is a warning, not a failure: the deterministic path
never needs one, so the command always exits 0 once the config parses.
"""

from __future__ import annotations

import argparse

from mra import __version__
from mra.models.privacy import host_of, privacy_mode
from mra.models.router import config_path, endpoints, load_config


def providers_check(path: str | None) -> int:
    path = path or str(config_path())
    built = endpoints(load_config(path))
    if not built:
        print(f"no [providers.*] entries in {path}; copy mra.example.toml to start")
        return 0
    local_only = privacy_mode() == "local-only"
    for name, endpoint in built.items():
        where = f"{name:<16} {endpoint.model:<22} {host_of(endpoint.provider.base_url)}"
        if local_only and not endpoint.local:
            print(f"BLOCKED      {where}  (MRA_PRIVACY=local-only)")
            continue
        if not endpoint.provider.available:
            print(f"WARN no key  {where}  (${endpoint.provider.api_key_env} unset)")
            continue
        try:
            result = endpoint.provider.complete(
                [{"role": "user", "content": "Reply with: ok"}], endpoint.model, 0.0, 5)
        except Exception as exc:  # any failure here is the answer, not a crash
            reason = str(exc).splitlines()[0][:80] if str(exc) else type(exc).__name__
            print(f"WARN unreach {where}  ({reason})")
        else:
            print(f"reachable    {where}  {result['latency_s']:.2f}s")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="mra")
    parser.add_argument("--version", action="version", version=f"mra {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)
    providers = commands.add_parser("providers", help="LLM provider tools")
    actions = providers.add_subparsers(dest="action", required=True)
    check = actions.add_parser("check", help="ping each configured provider")
    check.add_argument("--config", help="path to mra.toml (default: $MRA_CONFIG or ./mra.toml)")
    args = parser.parse_args(argv)
    return providers_check(args.config)


if __name__ == "__main__":
    raise SystemExit(main())
