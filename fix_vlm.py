#!/usr/bin/env python3
"""Fix VLM Run entries to reflect actual model list from gateway.vlm.run."""
import json, os, re

HOME = "/home/masterofsouls"
WATCH_DIR = os.path.join(HOME, "freellm-watch")
CHAIN_PATH = os.path.join(HOME, ".hermes", "scripts", "freellm-watch", "chain.json")
MODELS_CSV = os.path.join(WATCH_DIR, "models.csv")
GUIDE_MD = os.path.join(WATCH_DIR, "GUIDE.md")

# --- 1. Fix models.csv VLM Run row ---
with open(MODELS_CSV) as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if line.startswith("VLM Run,"):
        # Replace with accurate model names from actual gateway.vlm.run endpoint
        lines[i] = 'VLM Run,"google/gemini-3.5-flash-lite + google/gemini-3.7-flash + meta/muse-spark-1.2 + qwen/qwen3.8-27b + diffusiongemma",auto,10/min 30/h 100/day per IP,No key (keyless),NEW Oct 23 - Keyless endpoint at gateway.vlm.run/v1/openai - google-vertex provider models available keyless\n'
        print(f"Fixed models.csv line {i+1}: VLM Run")
        break

with open(MODELS_CSV, "w") as f:
    f.writelines(lines)

# --- 2. Fix chain.json VLM Run entry ---
with open(CHAIN_PATH) as f:
    chain = json.load(f)

for i, entry in enumerate(chain.get("new_this_week", [])):
    if entry.startswith("VLM Run Gateway:"):
        chain["new_this_week"][i] = (
            "VLM Run Gateway: NEW Oct 23 keyless endpoint at gateway.vlm.run/v1/openai; "
            "google/gemini-3.5-flash-lite + google/gemini-3.7-flash + meta/muse-spark-1.2 "
            "+ qwen/qwen3.8-27b + diffusiongemma; 10/min 30/h 100/day per IP — verified HTTP 200"
        )
        print(f"Fixed chain.json new_this_week[{i}]: VLM Run")
        break

with open(CHAIN_PATH, "w") as f:
    json.dump(chain, f, indent=2)

# --- 3. Fix GUIDE.md VLM Run section ---
with open(GUIDE_MD) as f:
    guide = f.read()

old_vlm = """## 🌐 VLM Run — keyless vision+text
- **base_url:** `https://gateway.vlm.run/v1/openai` (verified HTTP 200)
- **Limits:** 10 req/min, 30 req/hour, 100 req/day per IP
- **Models:** `qwen3.8-27b`, `qwen3.5-0.8b`, `diffusiongemma` (vision)
- **Catch:** truly keyless (no signup); verify with `curl gateway.vlm.run/v1/openai/models`"""

new_vlm = """## 🌐 VLM Run — keyless vision+text
- **base_url:** `https://gateway.vlm.run/v1/openai` (verified HTTP 200)
- **Limits:** 10 req/min, 30 req/hour, 100 req/day per IP
- **Models (live list):** `google/gemini-3.5-flash-lite`, `google/gemini-3.7-flash`, `meta/muse-spark-1.2`, `qwen/qwen3.8-27b`, `diffusiongemma`
- **Catch:** truly keyless (no signup); Google-Vertex Gemini models served keyless; verify with `curl gateway.vlm.run/v1/openai/models`"""

guide = guide.replace(old_vlm, new_vlm)
print("Fixed GUIDE.md VLM Run section")

with open(GUIDE_MD, "w") as f:
    f.write(guide)

print("\n=== All VLM Run entries fixed ===")
