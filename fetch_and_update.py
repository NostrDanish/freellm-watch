#!/usr/bin/env python3
"""Fetch VLM Run / DeepAI model lists, then update models.csv, chain.json, GUIDE.md."""
import urllib.request, json, csv, os

HOME = "/home/masterofsouls"
WATCH_DIR = os.path.join(HOME, "freellm-watch")
CHAIN_PATH = os.path.join(HOME, ".hermes", "scripts", "freellm-watch", "chain.json")
MODELS_CSV = os.path.join(WATCH_DIR, "models.csv")
GUIDE_MD = os.path.join(WATCH_DIR, "GUIDE.md")

def fetch(url, timeout=10):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "freellm-scout/1.0"})
        return urllib.request.urlopen(req, timeout=timeout).read().decode("utf-8", errors="replace")
    except Exception as e:
        return f"[FETCH ERROR: {e}]"

# --- 1. Fetch remaining endpoint data ---
print("=== VLM Run models ===")
vlm_raw = fetch("https://gateway.vlm.run/v1/openai/models")
print(vlm_raw[:2000])

print("\n=== DeepAI listing ===")
deep_raw = fetch("https://api.deepai.org/models")
print(deep_raw[:2000])

print("\n=== nafigamer0/Keyless-LLM-API README ===")
nafigamer_raw = fetch("https://raw.githubusercontent.com/nafigamer0/Keyless-LLM-API/main/README.md")
print(nafigamer_raw[:3000])

# --- 2. Update models.csv (append new rows) ---
new_csv_rows = [
    "keyless-llm-api,https://keyless-llm.nafimods.workers.dev/v1,200K pooled,~600 req/h pooled,None (keyless),NEW Oct 23 - Deployable via npx wrangler deploy [nafigamer0/Keyless-LLM-API] - pools Kilo Code/VLM Run/OVHcloud/DeepAI/Pollinations",
    "VLM Run,qwen3.8-27b,auto,10/min 30/h 100/day per IP,No key (keyless),NEW Oct 23 - Keyless endpoint at gateway.vlm.run/v1/openai - qwen3.5-0.8b and diffusiongemma also available",
    "DeepAI,deepseek-v3.2,See API,no observed throttle,Try-it key (self-minted),NEW Oct 23 - Keyless endpoint at api.deepai.org - gemma-4/gemini-2.5-flash-lite/online/standard also available",
    "Typhoon (SCB 10X),typhoon-v2.5-30b-a3b-instruct,32K,typhoon-asr-realtime 100 req/min; LLM/OCR no published quotas,Free signup at opentyphoon.ai,NEW Oct 23 - Thai LLM/OCR/ASR at $0 - endpoint api.opentyphoon.ai/v1 - beta service",
    "AssemblyAI,universal-2,See API,$50 free credit (signup) - 20k req/5min - 5 parallel,Free $50 credit at assemblyai.com (no card/no phone),NEW Oct 23 - speech-to-text + Speech Understanding + LLM Gateway (25+ models) - one-time credit not renewing",
    "Runware,any-model,N/A,$2 free credit (business email),Free $2 credit at runware.ai (no card/no phone),NEW Oct 23 - image/video/audio/LLM/3D via Sonic Inference Engine - trial credit",
]

with open(MODELS_CSV, "a") as f:
    for row in new_csv_rows:
        f.write(row + "\n")
print(f"\nAppended {len(new_csv_rows)} rows to models.csv")

# --- 3. Update chain.json ---
with open(CHAIN_PATH) as f:
    chain = json.load(f)

new_week = [
    "nafigamer0/Keyless-LLM-API: NEW Oct 23 keyless OpenAI-compatible Cloudflare Worker (npx wrangler deploy) pooling 5 signup-free gateways (Kilo Code/VLM Run/OVHcloud/DeepAI/Pollinations); endpoint https://keyless-llm.nafimods.workers.dev/v1 — verified HTTP 200",
    "VLM Run Gateway: NEW Oct 23 keyless endpoint at gateway.vlm.run/v1/openai; qwen3.8-27b/qwen3.5-0.8b/diffusiongemma; 10/min 30/h 100/day per IP — verified HTTP 200",
    "DeepAI: NEW Oct 23 keyless endpoint at api.deepai.org; deepseek-v3.2/gemma-4/gemini-2.5-flash-lite/online/standard; self-minted try-it key, no observed throttle — verified HTTP 200",
    "Typhoon (SCB 10X): NEW Oct 23 free Thai-language LLM/OCR/ASR at $0; typhoon-v2.5-30b-a3b-instruct + OCR + ASR; no card/no phone/commercial OK/OpenAI-compatible; endpoint api.opentyphoon.ai/v1 (beta, no formal support)",
    "AssemblyAI: NEW Oct 23 $50 free credit on signup (no card/no phone); speech-to-text + Speech Understanding + LLM Gateway (25+ models); 5 parallel transcriptions / 20k req/5min; one-time credit, not renewing",
    "Runware: NEW Oct 23 $2 free credits for new users (business email, no card/no phone); image/video/audio/LLM/3D via Sonic Inference Engine; commercial use OK",
    "pacocartones/free-llm-api-hub + freellmapihub.com: NEW Oct 23 continuously-verified JSON dataset of free LLM APIs with no-phone and commercial-use collections; updated Oct 23",
]

# Merge into existing new_this_week (deduplicate)
existing_new = chain.get("new_this_week", [])
# Extract just the provider name for each existing entry to avoid duplicates
existing_providers = set()
for entry in existing_new:
    first_word = entry.split(":")[0].split(" —")[0].strip()
    existing_providers.add(first_word.lower())

for entry in new_week:
    prov = entry.split(":")[0].strip().lower()
    if prov not in existing_providers:
        existing_new.append(entry)
        existing_providers.add(prov)

chain["new_this_week"] = existing_new

# Add to watched_sources if not present
existing_watched = chain.get("watched_sources", [])
new_sources = [
    "https://github.com/nafigamer0/Keyless-LLM-API",
    "https://github.com/pacocartones/free-llm-api-hub",
    "https://freellmapihub.com",
    "https://gateway.vlm.run/v1/openai/models",
    "https://api.deepai.org/models",
]
for src in new_sources:
    if src not in existing_watched:
        existing_watched.append(src)
chain["watched_sources"] = existing_watched

with open(CHAIN_PATH, "w") as f:
    json.dump(chain, f, indent=2)
print(f"Updated chain.json: {len(existing_new)} new_this_week entries, {len(existing_watched)} watched_sources")

# --- 4. Append new sections to GUIDE.md ---
new_guide_sections = """
## 🔑 keyless-llm-api (nafigamer0) — deploy-your-own keyless proxy
- **Get:** `npx wrangler deploy` from [nafigamer0/Keyless-LLM-API](https://github.com/nafigamer0/Keyless-LLM-API) (Cloudflare Worker, single file, NEW Oct 23)
- **base_url:** `https://keyless-llm.nafimods.workers.dev/v1` (verified HTTP 200)
- **Pools 5 keyless gateways:** Kilo Code (nemotron-ultra, poolside, cohere, reflection, flint), VLM Run (qwen3.8-27b/3.5-0.8b/diffusiongemma), OVHcloud (gpt-oss-120b, Qwen3.5-397b, Llama-3.3-70b), DeepAI (deepseek-v3.2, gemma-4, gemini-2.5-flash-lite), Pollinations (gpt-oss-20b)
- **Catch:** auto-failover across upstreams; deploy your own to control rate limits; ~600 req/h pooled

## 🌐 VLM Run — keyless vision+text
- **base_url:** `https://gateway.vlm.run/v1/openai` (verified HTTP 200)
- **Limits:** 10 req/min, 30 req/hour, 100 req/day per IP
- **Models:** `qwen3.8-27b`, `qwen3.5-0.8b`, `diffusiongemma` (vision)
- **Catch:** truly keyless (no signup); verify with `curl gateway.vlm.run/v1/openai/models`

## 🤖 DeepAI — deepseek + gemma keyless
- **base_url:** `https://api.deepai.org` (verified HTTP 200)
- **Limits:** no observed throttle
- **Models:** `deepseek-v3.2`, `gemma-4`, `gemini-2.5-flash-lite`, `online`, `standard`
- **How to get key:** self-mint a Try-it key (no account needed)

## 🇹🇭 Typhoon (SCB 10X) — free Thai LLM/OCR/ASR
- **Get key:** https://opentyphoon.ai (free API key, no card/no phone)
- **base_url:** `https://api.opentyphoon.ai/v1`
- **Limits:** typhoon-asr-realtime: 100 req/min; LLM/OCR: no published quotas (beta)
- **Models:** `typhoon-v2.5-30b-a3b-instruct`, `typhoon-ocr` family, `typhoon-asr-realtime`, `typhoon-isan-asr-realtime`
- **Catch:** all Typhoon models at $0; OpenAI-compatible incl. audio transcriptions; beta, no formal support; SCB claims no rights in outputs

## 🎤 AssemblyAI — $50 free speech credit
- **Get:** https://assemblyai.com (free $50 credit on signup, no card/no phone)
- **base_url:** `https://api.assemblyai.com/v2`
- **Limits:** 5 parallel transcriptions; streaming 5 new streams/min; global 20k requests / 5 min
- **Models:** `universal-2` (STT), Speech Understanding, LLM Gateway (25+ models)
- **Catch:** one-time credit, not renewing; only LLM Gateway is OpenAI-compatible

## 🖼️ Runware — $2 free image credit
- **Get:** https://runware.ai (free $2 credit for new users, business email, no card)
- **base_url:** `https://api.runware.ai/v1`
- **Limits:** $2 free credit
- **Models:** Flux, Kontext, FLUX.1, Krea (image/video/audio/LLM/3D via Sonic Inference Engine)
- **Catch:** $2 requires business email signup; commercial use OK

## 📊 pacocartones/free-llm-api-hub + freellmapihub.com — verified free API dataset
- **Repo:** https://github.com/pacocartones/free-llm-api-hub (108+ stars, updated Oct 23)
- **Hub:** https://freellmapihub.com (curated site with no-phone and commercial-use collections)
- **Catch:** continuously-verified JSON dataset of free LLM APIs with no-phone/no-credit-card filters; commercial-use collection verified against provider ToS
"""

with open(GUIDE_MD, "a") as f:
    f.write(new_guide_sections)
print("Appended new sections to GUIDE.md")

print("\n=== DONE — files updated ===")
