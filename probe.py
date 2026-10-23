#!/usr/bin/env python3
"""Probe for new/dead/changed free LLM endpoints not in tracked files."""
import urllib.request, json, sys, csv, re

BASE = "/home/masterofsouls/freellm-watch"
SCRATCH = "/home/masterofsouls/.hermes/profiles/freellm-scout/cache/scratch"

# --- Load tracked models.csv ---
tracked_csv = set()
try:
    with open(f"{BASE}/models.csv", newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tracked_csv.add(row.get('provider','').strip() + ':' + row.get('model','').strip())
    print(f"models.csv: {len(tracked_csv)} tracked provider:model entries")
except Exception as e:
    print(f"Error reading models.csv: {e}")

# --- Load tracked GUIDE.md ---
guide_text = ""
try:
    with open(f"{BASE}/GUIDE.md", encoding='utf-8') as f:
        guide_text = f.read()
    print(f"GUIDE.md: {len(guide_text)} chars")
except Exception as e:
    print(f"Error reading GUIDE.md: {e}")

# --- Load chain.json ---
chain_text = ""
try:
    with open(f"{SCRATCH}/chain.json", encoding='utf-8') as f:
        chain_text = f.read()
    print(f"chain.json: {len(chain_text)} chars (scratch)")
except:
    try:
        with open(f"{BASE}/chain.json", encoding='utf-8') as f:
            chain_text = f.read()
        print(f"chain.json: {len(chain_text)} chars (repo)")
    except Exception as e:
        print(f"Error reading chain.json: {e}")

def fetch(url, timeout=20, raw=False):
    """Fetch JSON or text from a URL."""
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Accept': 'application/json' if not raw else '*/*',
        })
        resp = urllib.request.urlopen(req, timeout=timeout)
        content = resp.read().decode('utf-8', errors='replace')
        if not raw:
            try:
                return json.loads(content), content
            except:
                return None, content
        return None, content
    except Exception as e:
        return None, str(e)

def is_tracked(provider, model):
    """Check if a provider:model is in any tracked file."""
    key = f"{provider}:{model}"
    if key.lower() in tracked_csv:
        return True
    if key.lower() in chain_text.lower():
        return True
    if provider.lower() in guide_text.lower() and model.lower() in guide_text.lower():
        return True
    return False

# --- Probe FreeRide ---
print("\n=== FreeRide ===")
data, raw = fetch('https://api.free-ride.xyz/v1/models')
if data:
    models_list = data.get('data', data.get('models', data if isinstance(data, list) else []))
    print(f"FreeRide models: {len(models_list)}")
    for m in models_list[:10]:
        mid = m.get('id','?') if isinstance(m, dict) else str(m)
        print(f"  {mid}")
else:
    print(f"  Error: {raw[:200]}")

# --- Probe FreeAI ---
print("\n=== FreeAI ===")
data, raw = fetch('https://api.free.ai/v1/models')
if data:
    models_list = data.get('data', data.get('models', data if isinstance(data, list) else []))
    print(f"FreeAI models: {len(models_list)}")
    for m in models_list[:10]:
        mid = m.get('id','?') if isinstance(m, dict) else str(m)
        print(f"  {mid}")
else:
    print(f"  Error: {raw[:200]}")

# --- Probe FreeTheAI ---
print("\n=== FreeTheAI ===")
data, raw = fetch('https://api.freetheai.com/v1/models')
if data:
    models_list = data.get('data', data.get('models', data if isinstance(data, list) else []))
    print(f"FreeTheAI models: {len(models_list)}")
    for m in models_list[:10]:
        mid = m.get('id','?') if isinstance(m, dict) else str(m)
        print(f"  {mid}")
else:
    print(f"  Error: {raw[:200]}")

# --- Probe LLM Tech ---
print("\n=== LLM Tech ===")
data, raw = fetch('https://api.llmtech.ai/v1/models')
if data:
    models_list = data.get('data', data.get('models', data if isinstance(data, list) else []))
    print(f"LLM Tech models: {len(models_list)}")
    for m in models_list[:5]:
        mid = m.get('id','?') if isinstance(m, dict) else str(m)
        print(f"  {mid}")
else:
    print(f"  Error: {raw[:200]}")

# --- Probe OpenRouter new free models ---
print("\n=== OpenRouter :free models (last 30) ===")
data, raw = fetch('https://openrouter.ai/api/v8/models')
if data:
    models_list = data.get('data', data.get('models', data if isinstance(data, list) else []))
    free_models = [m for m in models_list if isinstance(m, dict) and (':free' in m.get('id','') or 'free' in m.get('id','').lower())]
    print(f"Total: {len(models_list)}, :free: {len(free_models)}")
    for m in sorted(free_models, key=lambda x: x.get('id',''))[-30:]:
        mid = m.get('id','?')
        ctx = m.get('context_length','?')
        print(f"  {mid} | ctx={ctx}")
else:
    print(f"  Error: {raw[:200]}")

# --- Probe Groq ---
print("\n=== Groq ===")
data, raw = fetch('https://api.groq.com/openai/v1/models')
if data:
    models_list = data.get('data', [])
    print(f"Groq models: {len(models_list)}")
    for m in models_list:
        mid = m.get('id','?') if isinstance(m, dict) else str(m)
        print(f"  {mid}")
else:
    print(f"  Error: {raw[:200]}")

# --- Probe Cerebras ---
print("\n=== Cerebras ===")
data, raw = fetch('https://api.cerebras.ai/v1/models')
if data:
    print(f"  Models data: {str(data)[:500]}")
else:
    print(f"  Error: {raw[:200]}")

# --- Probe Mistral ---
print("\n=== Mistral AI ===")
data, raw = fetch('https://api.mistral.ai/v1/models')
if data:
    models_list = data.get('data', [])
    print(f"Mistral models: {len(models_list)}")
    for m in models_list:
        mid = m.get('id','?') if isinstance(m, dict) else str(m)
        print(f"  {mid}")
else:
    print(f"  Error: {raw[:200]}")

# --- Check GitHub Models (free tier) ---
print("\n=== GitHub Models ===")
data, raw = fetch('https://api.github.com/repos/github/models/contents?ref=main')
if data:
    # Try to list model directories
    if isinstance(data, list):
        dirs = [d.get('name','?') for d in data if d.get('type') == 'dir']
        print(f"GitHub Models dirs: {dirs[:20]}")
    else:
        print(f"  Unexpected: {str(data)[:200]}")
else:
    print(f"  Error: {raw[:200]}")

# --- Check BlockRun.ai ---
print("\n=== BlockRun.ai ===")
data, raw = fetch('https://api.blockrun.ai/v1/models')
if data:
    models_list = data.get('data', data.get('models', data if isinstance(data, list) else []))
    print(f"BlockRun models: {len(models_list)}")
    for m in models_list[:10]:
        mid = m.get('id','?') if isinstance(m, dict) else str(m)
        print(f"  {mid}")
else:
    print(f"  Error: {raw[:200]}")

# --- Check OVHcloud ---
print("\n=== OVHcloud AI ===")
data, raw = fetch('https://www.OVHcloud-AI.com/v1/models')
if data:
    print(f"  Models: {str(data)[:300]}")
else:
    print(f"  Error: {raw[:200]}")
    # Try alternative URL
    data2, raw2 = fetch('https://api.ai.cloud.ovh.net/v1/models')
    if data2:
        models_list = data2.get('data', data2.get('models', data2 if isinstance(data2, list) else []))
        print(f"OVHcloud models: {len(models_list)}")
        for m in models_list[:10]:
            mid = m.get('id','?') if isinstance(m, dict) else str(m)
            print(f"  {mid}")
    else:
        print(f"  Alt Error: {raw2[:200]}")

# --- Check freelm ---
print("\n=== FreeLLM pool ===")
data, raw = fetch('https://api.freelm.io/v1/models')
if data:
    print(f"  Models: {str(data)[:300]}")
else:
    print(f"  Error: {raw[:200]}")

# --- Check uncloseai ---
print("\n=== UncloseAI ===")
data, raw = fetch('https://api.uncloseai.com/v1/models')
if data:
    print(f"  Models: {str(data)[:300]}")
else:
    print(f"  Error: {raw[:200]}")

# --- Check AnyAPI ---
print("\n=== AnyAPI ===")
data, raw = fetch('https://api.anyapi.io/v1/models')
if data:
    print(f"  Models: {str(data)[:300]}")
else:
    print(f"  Error: {raw[:200]}")

# --- Check onomeo ---
print("\n=== Onomeo ===")
data, raw = fetch('https://api.onomeo.com/v1/models')
if data:
    print(f"  Models: {str(data)[:300]}")
else:
    print(f"  Error: {raw[:200]}")

# --- Check SambaNova ---
print("\n=== SambaNova (free tier) ===")
data, raw = fetch('https://api.sambanova.ai/v1/models')
if data:
    print(f"  Models: {str(data)[:300]}")
else:
    print(f"  Error: {raw[:200]}")
    # Try alternative
    data2, raw2 = fetch('https://api.sambanova.ai/v1/models', timeout=10)
    if data2:
        print(f"  Alt: {str(data2)[:300]}")
    else:
        print(f"  Alt Error: {raw2[:200]}")

# -- Check NVIDIA NIM ---
print("\n=== NVIDIA NIM ===")
# Try the NIM inference API for free models
data, raw = fetch('https://integrate.api.nvidia.com/v1/models')
if data:
    models_list = data.get('data', data.get('models', data if isinstance(data, list) else []))
    print(f"NVIDIA NIM models: {len(models_list)}")
    free_nim = [m for m in models_list if isinstance(m, dict) and ('free' in m.get('id','').lower() or 'reasoning' in m.get('id','').lower())]
    for m in free_nim[:20]:
        mid = m.get('id','?')
        print(f"  {mid}")
else:
    print(f"  Error: {raw[:200]}")

print("\n=== DONE ===")
