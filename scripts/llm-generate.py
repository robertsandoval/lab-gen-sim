#!/usr/bin/env python3
"""Call an OpenAI-compatible LLM API with a prompt template (Tekton build-time codegen)."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from string import Template
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def _load_template(path: Path, variables: dict[str, str]) -> str:
    raw = path.read_text(encoding="utf-8")
    # Support {{VAR}} placeholders
    for key, value in variables.items():
        raw = raw.replace(f"{{{{{key}}}}}", value)
    return raw


def _chat(base_url: str, api_key: str, model: str, prompt: str) -> str:
    url = base_url.rstrip("/") + "/chat/completions"
    body = json.dumps(
        {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a senior Python engineer extending general-simulation. "
                        "Follow domain extension rules strictly. Output only what is requested."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
        }
    ).encode("utf-8")
    req = Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    with urlopen(req, timeout=300) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"]


def main() -> int:
    parser = argparse.ArgumentParser(description="LLM codegen from prompt template")
    parser.add_argument("--prompt", required=True, type=Path, help="Prompt template file")
    parser.add_argument("--brief", type=Path, help="domain-brief.yaml")
    parser.add_argument("--spec", type=Path, help="domain-spec.json")
    parser.add_argument("--output", required=True, type=Path, help="Write LLM response here")
    parser.add_argument("--domain-id", default="", help="Override DOMAIN_ID")
    parser.add_argument("--adapter-id", default="", help="Override ADAPTER_ID")
    args = parser.parse_args()

    base_url = os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1")
    api_key = os.environ.get("LLM_API_KEY") or os.environ.get("OPENAI_API_KEY") or os.environ.get(
        "MAAS_API_TOKEN", ""
    )
    model = os.environ.get("LLM_MODEL", "gpt-4o-mini")

    if not api_key:
        print("ERROR: set LLM_API_KEY, OPENAI_API_KEY, or MAAS_API_TOKEN", file=sys.stderr)
        return 2

    brief_text = args.brief.read_text(encoding="utf-8") if args.brief else ""
    spec_text = args.spec.read_text(encoding="utf-8") if args.spec else ""

    domain_id = args.domain_id
    adapter_id = args.adapter_id
    if args.brief and not domain_id:
        try:
            import yaml

            brief = yaml.safe_load(brief_text)
            domain_id = brief.get("domain_id", "")
            adapter_id = brief.get("adapter_id", adapter_id)
        except Exception:
            pass

    variables = {
        "DOMAIN_BRIEF": brief_text,
        "DOMAIN_SPEC": spec_text,
        "DOMAIN_ID": domain_id,
        "ADAPTER_ID": adapter_id,
    }
    prompt = _load_template(args.prompt, variables)

    try:
        content = _chat(base_url, api_key, model, prompt)
    except (HTTPError, URLError, KeyError, TimeoutError) as exc:
        print(f"ERROR: LLM call failed: {exc}", file=sys.stderr)
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(content, encoding="utf-8")
    print(f"Wrote {args.output} ({len(content)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
