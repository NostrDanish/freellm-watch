# freellm-watch

Research and observation tooling for free/local LLM providers and Hermes routing.

## Data safety model

- `models.csv`, `chain.json`, and `GUIDE.md` are curated research artefacts. They are not silently rewritten by a network scrape.
- `fetch_and_update.py` fetches a small set of public catalogues and writes one atomic snapshot to `data/provider_observations.json` (or `FREELLM_OBSERVATIONS_PATH`).
- A listed model, HTTP 200, or public endpoint does **not** prove free entitlement, account access, a working completion, commercial-use rights, or sustainable quota.
- Observations are marked `entitlement: unknown`. Promote a provider into a Hermes fallback chain only after a separate authenticated test and human review of the provider's pricing/terms.
- The snapshot contains metadata and model IDs, not response bodies, API keys, prompts, or account data.

## Run

```bash
python3 fetch_and_update.py
python3 -m unittest discover -s tests -v
```

Set `FREELLM_OBSERVATIONS_PATH` to choose a writable output path. No machine-specific home directory is assumed.

## Watcher

`monitor.sh` fast-forwards configured clones using each clone's advertised `origin/HEAD`; set `FREELLMAPI_DIR`, `AWESOME_APIS_DIR`, and optionally `FREELLMAPI_SERVICE`. It fails closed if required paths/remotes/default branches are missing.
