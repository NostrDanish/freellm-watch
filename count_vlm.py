#!/usr/bin/env python3
"""Count total models on VLM Run keyless endpoint for accurate reporting."""
import urllib.request, json

url = "https://gateway.vlm.run/v1/openai/models"
try:
    req = urllib.request.Request(url, headers={"User-Agent": "freellm-scout/1.0"})
    data = json.loads(urllib.request.urlopen(req, timeout=10).read().decode())
    models = data.get("data", [])
    print(f"Total VLM Run models: {len(models)}")
    for m in models:
        print(f"  - {m.get('id', '?')}: {m.get('name', '?')}")
except Exception as e:
    print(f"Error: {e}")
