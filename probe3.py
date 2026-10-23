#!/usr/bin/env python3
"""Check watched repos and local FreeRide for new free LLM models."""
import urllib.request, json, csv, subprocess, re

BASE = "/home/masterofsouls/freellm-watch"
CHAIN = "/home/masterofsouls/.hermes/scripts/freellm-watch/chain.json"

# --- Load tracked data ---
tracked_models = set()
chain_str = ""

# chain.json
try:
    with open(CHAIN, encoding='utf-8') as f:
        chain_str = f.read()
except:
    pass

# models.csv
try:
    with open(f"{BASE}/models.csv", newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tracked_models.add((row.get('provider','').strip(), row.get('model','').strip()))
except:
    pass

def fetch(url, timeout=15):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        resp = urllib.request.urlopen(req, timeout=timeout)
        return resp.read().decode('utf-8', errors='replace')
    except Exception as e:
        return None

def is_tracked(provider, model):
    """Check if in models.csv OR chain.json."""
    for p, m in tracked_models:
        if p.lower() == provider.lower() and (model.lower() in m.lower() or m.lower() in model.lower()):
            return True
    combined = f"{provider.lower()}:{model.lower()}"
    if combined in chain_str.lower():
        return True
    # Also check if just the model appears in chain.json
    if model.lower() in chain_str.lower():
        return True
    return False

# --- 1. Check FreeRide local proxy ---
print("=== FreeRide local proxy (localhost:11343) ===")
result = subprocess.run(['curl', '-s', '-m', '10', 'http://localhost:11343/v1/models'],
    capture_output=True, text=True, timeout=15)
if result.stdout:
    try:
        data = json.loads(result.stdout)
        models = data.get('data', data if isinstance(data, list) else [])
        print(f"FreeRide local: {len(models)} routes")
        # Sample some routes
        if isinstance(models, list):
            for m in models[:5]:
                print(f"  {m.get('id','?') if isinstance(m,dict) else str(m)}")
    except:
        print(f"Raw: {result.stdout[:500]}")
else:
    print(f"Not running: {result.stderr[:200]}")

# --- 2. Check mnfst/awesome-free-llm-apis ---
print("\n=== mnfst/awesome-free-llm-apis ===")
content = fetch('https://raw.githubusercontent.com/mnstlme/awesome-free-llm-apis/main/README.md')
if content:
    print(f"README: {len(content)} chars")
    # Extract table rows or list items with API providers
    import re
    # Find lines mentioning free/API providers
    lines = content.split('\n')
    free_items = [l for l in lines if re.search(r'\b(free|api|endpoint|provider)', l, re.IGNORECASE) and l.strip().startswith(('*', '-', '|'))]
    print(f"Lines mentioning free/api: {len(free_items)}")
    for l in free_items[:30]:
        print(f"  {l.strip()[:120]}")
else:
    # Try alternate repo name
    content = fetch('https://raw.githubusercontent.com/mnstlme/awesome-free-llm-apis/master/README.md')
    if content:
        print(f"README (master): {len(content)} chars")
    else:
        print("Could not fetch mnfst repo")

# Also try github API to get repo info
result = subprocess.run(['curl', '-s', '-m', '10',
    'https://api.github.com/repos/mnstlme/awesome-free-llm-apis'],
    capture_output=True, text=True, timeout=15)
if result.stdout:
    try:
        repo = json.loads(result.stdout)
        print(f"Repo: {repo.get('full_name','?')} | stars={repo.get('stargazers_count','?')} | updated={repo.get('updated_at','?')}")
    except:
        pass

# --- 3. Check tashfeenahmed/freellmapi ---
print("\n=== tashfeenahmed/freellmapi ===")
content = fetch('https://raw.githubusercontent.com/tashfeenahmed/freellmapi/main/README.md')
if content:
    print(f"README: {len(content)} chars")
    lines = content.split('\n')
    free_items = [l for l in lines if re.search(r'\b(free|api|endpoint|provider)', l, re.IGNORECASE) and l.strip().startswith(('*', '-', '|'))]
    print(f"Lines mentioning free/api: {len(free_items)}")
    for l in free_items[:30]:
        print(f"  {l.strip()[:120]}")
else:
    content = fetch('https://raw.githubusercontent.com/tashfeenahmed/freellmapi/master/README.md')
    if content:
        print(f"README (master): {len(content)} chars")
    else:
        # Try listing the repo contents
        result = subprocess.run(['curl', '-s', '-m', '10',
            'https://api.github.com/repos/tashfeenahmed/freellmapi/contents'],
            capture_output=True, text=True, timeout=15)
        if result.stdout:
            try:
                files = json.loads(result.stdout)
                if isinstance(files, list):
                    print(f"Repo files: {[f.get('name','?') for f in files[:20]]}")
            except:
                print(f"Raw: {result.stdout[:300]}")
        else:
            print(f"Error: {result.stderr[:200]}")

# --- 4. Check for new model additions in the watched repos ---
print("\n=== Checking for NEW untracked entries ===")

# Check FreeRide README for new provider mentions
content = fetch('https://raw.githubusercontent.com/Shaivpidadi/FreeRideV3/main/README.md')
if content:
    # Look for provider names mentioned in README
    providers = re.findall(r'([A-Z][a-zA-Z]+\s*(?:AI|cloud|API|Models|Endpoint|Gateway))', content)
    print(f"Providers in FreeRide README: {list(set(providers))[:20]}")

# --- 5. Check OpenRouter for any brand-new :free models added today ---
print("\n=== OpenRouter new :free models ===")
result = subprocess.run(['curl', '-s', '-m', '15', 'https://openrouter.ai/api/v1/models'],
    capture_output=True, text=True, timeout=20)
if result.stdout:
    try:
        data = json.loads(result.stdout)
        models = data.get('data', [])
        free_models = [m for m in models if isinstance(m, dict) and ':free' in m.get('id','')]
        print(f"Total :free models: {len(free_models)}")
        # Find untracked ones
        new_models = []
        for m in free_models:
            mid = m.get('id','')
            if not is_tracked('openrouter', mid):
                new_models.append(mid)
        if new_models:
            print(f"NEW untracked :free models: {new_models}")
        else:
            print("All :free models tracked")
        # Show all with creation dates (epoch)
        import datetime
        for m in sorted(free_models, key=lambda x: x.get('created', 0)):
            mid = m.get('id','')
            created = m.get('created', 0)
            try:
                dt = datetime.datetime.fromtimestamp(created).strftime('%Y-%m-%d')
            except:
                dt = '?'
            ctx = m.get('context_length','?')
            tracked = "TRACKED" if is_tracked('openrouter', mid) else "NEW!!!"
            print(f"  {mid} | created={dt} | ctx={ctx} | {tracked}")
    except Exception as e:
        print(f"Error: {e}")
else:
    print(f"Error: {result.stderr[:200]}")

# --- 6. Check for new free LLM news ---
print("\n=== Recent news / announcements ===")
# Check if there are any new announcements on github trending
result = subprocess.run(['curl', '-s', '-m', '15',
    'https://api.github.com/search/repositories?q=free+llm+api+created:>2026-10-22&sort=stars&order=desc&per_page=10'],
    capture_output=True, text=True, timeout=20)
if result.stdout:
    try:
        data = json.loads(result.stdout)
        items = data.get('items', [])
        print(f"New free-LLM API repos (today+): {len(items)}")
        for item in items:
            name = item.get('full_name','?')
            stars = item.get('stargazers_count','?')
            created = item.get('created_at','?')
            desc = item.get('description','?')
            tracked = "check"
            if name.lower() in chain_str.lower():
                tracked = "TRACKED"
            print(f"  {name} | stars={stars} | created={created}")
            print(f"    desc: {(desc[:100] if desc else 'N/A')}")
    except:
        print(f"Error: {result.stdout[:300]}")
else:
    print(f"Error: {result.stderr[:200]}")

# --- 7. Check FreeTheAI ---
print("\n=== FreeTheAI check ===")
result = subprocess.run(['curl', '-s', '-m', '10', '-o', '/dev/null', '-w', '%{http_code}',
    'https://api.freetheai.com/v1/models'],
    capture_output=True, text=True, timeout=15)
print(f"FreeTheAI HTTP status: {result.stdout}")

# FreeTheAI alternative URL
result = subprocess.run(['curl', '-s', '-m', '10', '-o', '/dev/null', '-w', '%{http_code}',
    'https://freetheai.com/api/v1/models'],
    capture_output=True, text=True, timeout=15)
print(f"FreeTheAI alt HTTP status: {result.stdout}")

# --- 8. Check LLM Tech ---
print("\n=== LLM Tech check ===")
result = subprocess.run(['curl', '-s', '-m', '10', '-o', '/dev/null', '-w', '%{http_code}',
    'https://api.llmtech.ai/v1/models'],
    capture_output=True, text=True, timeout=15)
print(f"LLM Tech HTTP status: {result.stdout}")

print("\n=== DONE ===")
