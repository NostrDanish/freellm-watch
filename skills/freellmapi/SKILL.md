---
name: freellmapi
description: Use for local FreeLLMAPI (localhost:3001) auth and tuning.
---

# FreeLLMAPI ops

Repo `~/Work/freellmapi` (upstream tashfeenahmed/freellmapi, v0.16.5). Service `freellmapi.service` (user). DB `server/data/freeapi.db` — sqlite, holds unified key, user, usage history; **back it up before any reinstall** (`.backup` into `~/Work/freellmapi/backups/`). Reinstall is almost never the fix.

## Two credentials, two audiences
- `/v1/*` (chat, models): unified key from `settings.unified_api_key` in DB; mirrored in env `HERMES_CUSTOM_FREELLMAPI_API_KEY` (Hermes provider `key_env` must point there — direct config.yaml edits are write-guarded, use `hermes config set`).
- `/api/*` (dashboard ops): session token from `POST /api/auth/login` — the unified key is rejected here.

## Dashboard password recovery (no UI needed)
Hash is Node scrypt defaults (N=16384 r=8 p=1, keylen 64), format `scrypt$<saltHex>$<hashHex>` in `users.password_hash` — Python `hashlib.scrypt` is compatible. Rotate at DB level: generate pw, hash, `UPDATE users SET password_hash`, then `POST /api/auth/login {"email","password"}` → session token. Back up DB first. Hand the new pw to the user once (no programmatic vault on this box: `hermes vault add` is interactive-only, `vaultknox` module absent).

## Keyless-platform unlock
Platforms whose providers allow anonymous use (llm7: any bearer e.g. "anonymous"; aihorde: built-in ANON_KEY 0000000000) are router-dead until a key ROW exists — add via `POST /api/keys {"platform","key","label"}` (server encrypts; hand-crafted DB rows impossible). Key status 'unknown' is routable (counts as healthy everywhere). Served model IDs are BARE (no platform prefix): llm7's model is `default`, not `llm7/default` — 'llm7/default' returns model_not_found. Verified live 2026-10-21: llm7 works through the gateway; aihorde's 32 models stayed unserved despite key+enabled (worker-availability gating) — skip it, not worth the rabbit hole.

## Login reset trap
Every "Send reset code" click mints a NEW code and silently kills the previous one. Out-of-band codes are dead the moment the user clicks that button. Correct order: click in UI first → `journalctl --user -u freellmapi.service -q --since "1 min ago" | grep -oP 'Password-reset code: \K\w+'` → paste into the already-open form → touch nothing else. Codes: 15-min TTL, single-use. 5 wrong passwords → 15-min 429 lockout.

## Quota savers (monthly free-tier budget)
- Cache: `PUT /api/cache/config {"enabled":true}` — off by default; verify with repeat request, header `X-FreeLLM-Cache: HIT`. Truncated replies (finish_reason=length) are never cached — intentional.
- Compression: `PUT /api/settings/compression {"mode":"lossless"}` — modes off/lossless/standard/aggressive.
- Keep explore mode OFF (burns quota probing).
- Guardrails: `PUT /api/settings/guardrails {"maxConsecutiveUpstreamFails":4}` bounds serial retries (worst case 38.8s). Leave `requestMaxTokensBudget` at 0 — any nonzero value injects max_tokens≤4096 when the client sends none (TOKEN_BUDGET_OUTPUT_CAP), truncating long agent replies.
- Reliability floor: `PUT /api/settings/min-reliability-floor {"floor":0.5}` drops well-sampled flaky models; under-sampled ones stay, chain never empties.
- Cache TTL is env-only: `RESPONSE_CACHE_TTL_SECONDS` drop-in at `~/.config/systemd/user/freellmapi.service.d/cache-ttl.conf` (86400), then daemon-reload + restart freellmapi.service (safe; cache entries + settings persist in sqlite).

## Catalog reality
Enabled-model counts lie: check `keyCount`/`keyless` in `/api/fallback/` — most platforms (groq, google, mistral, cloudflare, nvidia, electronhub…) ship enabled but keyless-dead. Live pool = only platforms with keys. Adding free keys (Groq, AI Studio, Mistral, Cloudflare, NIM) needs no restart.

## Hermes wiring
Provider block: base_url `http://localhost:3001/v1`, model `auto`, `discover_models: true`. Changes need a natural gateway restart — never restart mid-session.
