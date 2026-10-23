#!/usr/bin/env python3
"""Probe for new/dead/changed free LLM endpoints not in tracked files."""
import urllib.request, json, csv, re

BASE = "/home/masterofsouls/freellm-watch"
CHAIN = "/home/masterofsouls/.hermes/scripts/freellm-watch/chain.json"

# --- Load tracked files ---
tracked_keys = set()
tracked_text = ""

# Load chain.json
try:
    with open(CHAIN, encoding='utf-8') as f:
        chain_data = json.load(f)
    chain_str = json.dumps(chain_data)
    # Extract all provider:model combos
    for item in chain_data.get('ordered_fallback_chain', []):
        tracked_keys.add((item.get('provider',''), item.get('model','')))
    tracked_text = chain_str
    print(f"chain.json: {len(chain_str)} chars, {len(chain_data.get('ordered_fallback_chain',[]))} chain entries")
    # Check new_this_week
    new_week = chain_data.get('new_this_week', [])
    print(f"new_this_week entries: {len(new_week)}")
    for item in new_week:
        print(f"  {item.get('provider','')}:{item.get('model','')} — {item.get('notes','')[:80]}")
except Exception as e:
    print(f"Error reading chain.json: {e}")

# Load models.csv
try:
    with open(f"{BASE}/models.csv", newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tracked_keys.add((row.get('provider','').strip(), row.get('model','').strip()))
    print(f"models.csv: {len(tracked_keys)} tracked entries")
except Exception as e:
    print(f"Error reading models.csv: {e}")

# Load GUIDE.md
try:
    with open(f"{BASE}/GUIDE.md", encoding='utf-8') as f:
        guide_text = f.read()
    print(f"GUIDE.md: {len(guide_text)} chars")
except Exception as e:
    print(f"Error reading GUIDE.md: {e}")
    guide_text = ""

def fetch_json(url, timeout=20):
    """Fetch JSON from a URL."""
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Accept': 'application/json',
        })
        resp = urllib.request.urlopen(req, timeout=timeout)
        content = resp.read().decode('utf-8', errors='replace')
        return json.loads(content), None
    except Exception as e:
        return None, str(e)

def is_tracked(provider, model):
    """Check if a provider:model is in any tracked file."""
    # Check chain.json
    for p, m in tracked_keys:
        if p.lower() == provider.lower() and m.lower() == model.lower():
            return True
    # Check by text search in chain_str
    combined = f"{provider}:{model}".lower()
    if combined in chain_str.lower():
        return True
    return False

print("\n=== === PROBING ENDPOINTS === ===\n")

# --- OpenRouter free models ---
print("--- OpenRouter ---")
data, err = fetch_json('https://openrouter.ai/api/v1/models')
if data:
    models = data.get('data', data if isinstance(data, list) else [])
    print(f"Total OpenRouter models: {len(models)}")
    free_models = [m for m in models if isinstance(m, dict) and ':free' in m.get('id','')]
    print(f":free models: {len(free_models)}")
    new_free = []
    for m in free_models:
        mid = m.get('id','')
        if not is_tracked('openrouter', mid):
            new_free.append(mid)
    if new_free:
        print(f"NEW UNTRACKED :free models ({len(new_free)}):")
        for mid in sorted(new_free):
            ctx = m.get('context_length','?') if isinstance(m, dict) else '?'
            print(f"  {mid}")
    else:
        print("All :free models already tracked")
    # Show last 10 free models with dates
    for m in free_models[-10:]:
        mid = m.get('id','')
        ctx = m.get('context_length','?')
        created = m.get('created', '?')
        print(f"  {mid} | ctx={ctx} | created={created}")
else:
    print(f"Error: {err[:200]}")

# --- FreeRide ---
print("\n--- FreeRide ---")
# Try the GitHub repo to find the API URL
data, err = fetch_json('https://api.github.com/repos/Shaivpidadi/FreeRideV3/readme')
if data:
    import base64
    content = base64.b64decode(data.get('content','')).decode('utf-8', errors='replace')
    # Look for API URL patterns
    urls = re.findall(r'https?://[a-zA-Z0-9.-]+free-?ride[a-zA-Z0-9.-]*(?:/[^\s<>"\']*)?', content, re.IGNORECASE)
    api_urls = re.findall(r'https?://api[a-zA-Z0-9.-]*(?:/[^\s<>"\']*)?', content)
    print(f"FreeRide README: {len(content)} chars")
    print(f"free-ride URLs found: {urls[:10]}")
    print(f"API URLs found: {api_urls[:10]}")
else:
    print(f"GitHub Error: {err[:200]}")

# Try pip
import subprocess
result = subprocess.run(['pip3', 'index', 'versions', 'freeride-gateway'], capture_output=True, text=True, timeout=30)
print(f"pip freeride-gateway: {result.stdout[:300]}")
if result.stderr:
    print(f"pip stderr: {result.stderr[:200]}")

# --- Check HuggingFace Inference Endpoints ---
print("\n--- HuggingFace Inference ---")
# Check if there are new free inference endpoints
result = subprocess.run(['curl', '-s', '-m', '15', 
    'https://huggingface.co/api/models?library=transformers&sort=modified&direction=-1&limit=30'],
    capture_output=True, text=True, timeout=20)
if result.stdout:
    try:
        hf_models = json.loads(result.stdout)
        print(f"Recent HF models: {len(hf_models)}")
        for m in hf_models[:10]:
            mid = m.get('id','?')
            task = m.get('pipeline_tag','?')
            downloads = m.get('downloads',0)
            print(f"  {mid} | task={task} | downloads={downloads}")
    except:
        print(f"HF parse error: {result.stdout[:200]}")
else:
    print(f"HF error: {result.stderr[:200]}")

# --- Check Pollinations ---
print("\n--- Pollinations ---")
result = subprocess.run(['curl', '-s', '-m', '15', 'https://pollinations.ai/models'],
    capture_output=True, text=True, timeout=20)
if result.stdout:
    try:
        models = json.loads(result.stdout)
        if isinstance(models, list):
            print(f"Pollinations models: {len(models)}")
            for m in models[:20]:
                print(f"  {m}")
    except:
        print(f"Pollinations raw: {result.stdout[:500]}")
else:
    print(f"Pollinations error: {result.stderr[:200]}")

# --- Check Kiro ---
print("\n--- Kiro ---")
result = subprocess.run(['curl', '-s', '-m', '15', 'https://api.kiro.ai/v1/models'],
    capture_output=True, text=True, timeout=20)
if result.stdout:
    try:
        data = json.loads(result.stdout)
        models = data.get('data', data if isinstance(data, list) else [])
        print(f"Kiro models: {len(models)}")
        for m in models[:10]:
            mid = m.get('id','?') if isinstance(m, dict) else str(m)
            print(f"  {mid}")
    except:
        print(f"Kiro raw: {result.stdout[:500]}")
else:
    print(f"Kiro error: {result.stderr[:200]}")

# --- Check Ollama Cloud ---
print("\n--- Ollama Cloud ---")
result = subprocess.run(['curl', '-s', '-m', '15', 'https://api.ollama.ai/v1/models'],
    capture_output=True, text=True, timeout=20)
if result.stdout:
    try:
        data = json.loads(result.stdout)
        print(f"Ollama Cloud: {str(data)[:500]}")
    except:
        print(f"Ollama raw: {result.stdout[:500]}")
else:
    print(f"Ollama error: {result.stderr[:200]}")

# --- Check xKiro / Z.ai ---
print("\n--- Z.ai / xKiro ---")
result = subprocess.run(['curl', '-s', '-m', '15', 'https://api.z.ai/v1/models'],
    capture_output=True, text=True, timeout=20)
if result.stdout:
    try:
        data = json.loads(result.stdout)
        models = data.get('data', data if isinstance(data, list) else [])
        print(f"Z.ai models: {len(models)}")
        for m in models[:10]:
            mid = m.get('id','?') if isinstance(m, dict) else str(m)
            print(f"  {mid}")
    except:
        print(f"Z.ai raw: {result.stdout[:500]}")
else:
    print(f"Z.ai error: {result.stderr[:200]}")

# --- Check OVHcloud ---
print("\n--- OVHcloud AI ---")
result = subprocess.run(['curl', '-s', '-m', '15', '-H', 'Accept: application/json', 
    'https://api.ai.cloud.ovh.net/1.0/lib/v1/models'],
    capture_output=True, text=True, timeout=20)
if result.stdout:
    print(f"OVHcloud raw: {result.stdout[:500]}")
else:
    print(f"OVHcloud error: {result.stderr[:200]}")

# --- Check new free LLM APIs via web ---
print("\n--- Recent GitHub repos (free LLM) ---")
result = subprocess.run(['curl', '-s', '-m', '15', 
    'https://api.github.com/search/repositories?q=free+llm+api+openai+compatible+created:>2026-09-1&sort=updated&per_page=10'],
    capture_output=True, text=True, timeout=20)
if result.stdout:
    try:
        data = json.loads(result.stdout)
        items = data.get('items', [])
        print(f"GitHub repos found: {len(items)}")
        for item in items:
            name = item.get('full_name','?')
            desc = item.get('description','?')
            stars = item.get('stargazers_count','?')
            created = item.get('created_at','?')
            updated = item.get('updated_at','?')
            print(f"  {name} | stars={stars} | created={created} | updated={updated}")
            print(f"    desc: {desc[:100] if desc else 'N/A'}")
    except:
        print(f"GitHub search error: {result.stdout[:300]}")
else:
    print(f"GitHub search error: {result.stderr[:200]}")

# --- Check BlockRun.ai ---
print("\n--- BlockRun.ai ---")
result = subprocess.run(['curl', '-s', '-m', '15', 'https://api.blockrun.ai/v1/models'],
    capture_output=True, text=True, timeout=20)
if result.stdout:
    try:
        data = json.loads(result.stdout)
        models = data.get('data', data if isinstance(data, list) else [])
        print(f"BlockRun models: {len(models)}")
        for m in models[:10]:
            mid = m.get('id','?') if isinstance(m, dict) else str(m)
            print(f"  {mid}")
    except:
        print(f"BlockRun raw: {result.stdout[:500]}")
else:
    print(f"BlockRun error: {result.stderr[:200]}")

# --- Check Mistral free tier ---
print("\n--- Mistral AI ---")
data, err = fetch_json('https://api.mistral.ai/v1/models')
if data:
    models = data.get('data', [])
    print(f"Mistral models: {len(models)}")
    for m in models:
        mid = m.get('id','?')
        print(f"  {mid}")
else:
    print(f"Error: {err[:200]}")

# --- Check Cerebras ---
print("\n--- Cerebras ---")
data, err = fetch_json('https://api.cerebras.ai/v1/models')
if data:
    print(f"Cerebras: {str(data)[:500]}")
else:
    print(f"Error: {err[:200]}")

# --- Check Together.ai ---
print("\n--- Together.ai ---")
data, err = fetch_json('https://api.together.xyz/v1/models')
if data:
    models = data.get('data',[])
    print(f"Together models: {len(models)}")
    free_or_cheap = [m for m in models if isinstance(m, dict) and m.get('pricing',{}).get('prompt','') in ('0','0.0')]
    print(f"Free/0-prompt models: {len(free_or_cheap)}")
    for m in free_or_cheap[:10]:
        print(f"  {m.get('id','?')}")
else:
    print(f"Error: {err[:200]}")

# --- Check Cloudflare AI ---
print("\n--- Cloudflare AI ---")
result = subprocess.run(['curl', '-s', '-m', '15', 'https://api.cloudflare.com/client/v4/accounts/-/ai/models'],
    capture_output=True, text=True, timeout=20)
if result.stdout:
    try:
        data = json.loads(result.stdout)
        models = data.get('result', {}).get('models', [])
        print(f"Cloudflare models: {len(models)}")
        for m in models[-15:]:
            print(f"  {m}")
    except:
        print(f"Cloudflare raw: {result.stdout[:500]}")
else:
    print(f"Cloudflare error: {result.stderr[:200]}")

# --- Check for new models on GitHub trending ---
print("\n--- GitHub Trending (AI free) ---")
result = subprocess.run(['curl', '-s', '-m', '15', 'https://api.github.com/search/repositories?q=free-llm-api+OR+free-llm-models+OR+freeride+OR+freeai+created:>2026-09-15&sort=updated&per_page=10'],
    capture_output=True, text=True, timeout=20)
if result.stdout:
    try:
        data = json.loads(result.stdout)
        items = data.get('items', [])
        print(f"Repos found: {len(items)}")
        for item in items:
            name = item.get('full_name','?')
            updated = item.get('updated_at','?')
            stars = item.get('stargazers_count','?')
            print(f"  {name} | stars={stars} | updated={updated}")
    except:
        print(f"Error: {result.stdout[:300]}")
else:
    print(f"Error: {result.stderr[:200]}")

print("\n=== DONE ===")
