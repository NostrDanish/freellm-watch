#!/usr/bin/env python3
"""Collect public provider-catalog observations without editing curated data.

This deliberately does NOT infer free entitlement from a public model listing,
HTTP 200, or an unauthenticated endpoint. It writes one atomic JSON snapshot.
Curated models.csv, chain.json and GUIDE.md remain human-reviewed sources.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

USER_AGENT = "freellm-watch/2.0 (+https://github.com/NostrDanish/freellm-watch)"
DEFAULT_SOURCES = {
    "vlm-run": "https://gateway.vlm.run/v1/openai/models",
    "deepai": "https://api.deepai.org/models",
    "keyless-llm-api-readme": "https://raw.githubusercontent.com/nafigamer0/Keyless-LLM-API/main/README.md",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def extract_model_ids(payload: Any) -> list[str]:
    """Extract only explicit model identifiers from common catalog JSON shapes."""
    rows = payload.get("data", []) if isinstance(payload, dict) else []
    if not isinstance(rows, list):
        return []
    found = set()
    for row in rows:
        if isinstance(row, dict):
            model_id = row.get("id") or row.get("name") or row.get("model")
            if isinstance(model_id, str) and model_id.strip():
                found.add(model_id.strip())
    return sorted(found)


def observe(name: str, url: str, timeout: float = 10.0) -> dict[str, Any]:
    checked_at = utc_now()
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json,text/plain,*/*"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read(2_000_001)
            truncated = len(body) > 2_000_000
            body = body[:2_000_000]
            content_type = response.headers.get("Content-Type", "")
            result: dict[str, Any] = {
                "source_id": name,
                "url": url,
                "checked_at": checked_at,
                "http_status": int(response.status),
                "content_type": content_type,
                "bytes": len(body),
                "truncated": truncated,
                "sha256": hashlib.sha256(body).hexdigest(),
                "status": "catalog_observed",
                "model_ids": [],
                "entitlement": "unknown",
                "note": "Catalog visibility is not proof of free entitlement or successful inference.",
            }
            if not truncated and ("json" in content_type.lower() or body.lstrip().startswith(b"{")):
                try:
                    result["model_ids"] = extract_model_ids(json.loads(body.decode("utf-8")))
                except (UnicodeDecodeError, json.JSONDecodeError):
                    result["status"] = "unparsed_response"
            return result
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return {
            "source_id": name,
            "url": url,
            "checked_at": checked_at,
            "status": "fetch_error",
            "error_type": type(exc).__name__,
            "entitlement": "unknown",
            "model_ids": [],
        }


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    except Exception:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default=os.environ.get("FREELLM_OBSERVATIONS_PATH", "data/provider_observations.json"))
    parser.add_argument("--timeout", type=float, default=10.0)
    args = parser.parse_args()
    if args.timeout <= 0 or args.timeout > 60:
        parser.error("--timeout must be greater than 0 and at most 60 seconds")

    observations = [observe(name, url, args.timeout) for name, url in DEFAULT_SOURCES.items()]
    payload = {
        "schema_version": 1,
        "generated_at": utc_now(),
        "policy": "Observations are not entitlement verification and are never auto-promoted into Hermes routing.",
        "observations": observations,
    }
    output = Path(args.output).expanduser()
    atomic_write_json(output, payload)
    print(json.dumps({"output": str(output), "sources": len(observations),
                      "catalog_observed": sum(x["status"] == "catalog_observed" for x in observations),
                      "fetch_errors": sum(x["status"] == "fetch_error" for x in observations)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
