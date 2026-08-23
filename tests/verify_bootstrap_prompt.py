#!/usr/bin/env python3
"""Contract checks for the public bootstrap prompt."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPT = ROOT / "plans" / "bootstrap-from-prompt.md"
README = ROOT / "README.md"

REQUIRED = (
    "https://open.larksuite.com/page/launcher?from=backend_oneclick",
    "https://open.larksuite.com",
    "cc-connect",
    "lark-cli",
    "BrowseForge",
    "https://github.com/nczz/BrowseForge/releases",
    "gpt-5.6-terra",
    "grok-4.6",
    "claude-opus-4-8",
    "deepseek-v4-flash-0731",
    "reasoning_effort = medium",
    "reasoning_effort = high",
)

# Words that must not appear in the copy-paste prompt body.
FORBIDDEN_IN_PROMPT = (
    "authentik",
    "vaultwarden",
    "netbird",
    "openclaw",
    "hermes",
    "odoo",
    "gitignore",
)


def extract_prompt(text: str) -> str:
    start = text.find("```text")
    end = text.rfind("```")
    if start < 0 or end <= start:
        raise SystemExit("bootstrap prompt fence ```text ... ``` is missing")
    return text[start + len("```text") : end]


def main() -> None:
    prompt_md = PROMPT.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")
    errors: list[str] = []

    if "plans/bootstrap-from-prompt.md" not in readme:
        errors.append("README.md does not link plans/bootstrap-from-prompt.md")

    body = extract_prompt(prompt_md)
    for needle in REQUIRED:
        if needle not in body:
            errors.append(f"prompt missing required text: {needle}")

    lowered = body.lower()
    for word in FORBIDDEN_IN_PROMPT:
        if word in lowered:
            errors.append(f"prompt contains forbidden term: {word}")

    if errors:
        raise SystemExit("\n".join(errors))
    print("verify_bootstrap_prompt: ok")


if __name__ == "__main__":
    main()
