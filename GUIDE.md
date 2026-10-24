# Free LLM API Guide — updated 2026-10-23

Every provider below is OpenAI-SDK-compatible. Point any tool at `base_url` + key and go.
Full model table: `models.csv` (same folder). Auto-maintained by the `freellm-watch` cron agent.

---

## ⭐ OpenRouter — the one key to rule them all
- **Get key:** https://openrouter.ai/keys (Google login, 30 sec)
- **Limits:** 20 RPM, **50 req/day per free model** → jumps to **1,000/day** after a one-time $10 credit buy
- **base_url:** `https://openrouter.ai/api/v1`
- **Best free models:** `nvidia/nemotron-3-ultra-550b-a55b:free` (1M ctx), `nvidia/nemotron-3-super-120b-a12b:free`, `nvidia/nemotron-3.5-lightning:free`, `poolside/laguna-s-2.1:free` (code), `google/gemma-4-31b-it:free`, `thinkingmachines/inkling:free` (reasoning), `google/lyria-3-pro-preview` (audio, $0), `recursive/flint-v1.0:free` (262K ctx), `apodex/apodex-1.1-mini:free` (262K ctx, reasoning)
- **Trick:** model = `openrouter/free` auto-routes across all 23 free models. Or pass a `models: [...]` array for built-in fallback.

## 🚪 No-key options (zero signup)
| Provider | base_url | Limit | Catch |
|---|---|---|---|
| **Kilo Code** | `https://api.kilo.ai/api/gateway` | 200 req/hr per IP | Logs prompts; has nemotron-ultra 1M free |
| **OVHcloud** | `https://oai.endpoints.kepler.ai.cloud.ovh.net/v1` | 2 RPM per IP/model | EU-hosted, slow trickle |
| **BlockRun.ai** | `https://blockrun.ai/api/v1` | 429 per IP; keyless | Verified Oct 21; 7 NVIDIA-hosted OS free models: nemotron-3-ultra-550b (1M), nano-omni-30b-a3b-reasoning (256K), llama-3.2-11b-vision (128K), nemotron-3.5-lightning (1M), cohere/north-mini-code (256K), poolside/laguna-xs-2.1 (262K), muse-glimmer-30b (1M) |
| **uncloseai** | `https://hermes.ai.unturf.com/v1` | 429 per IP; keyless | Verified Oct 21; single Qwen3.8-27B-exl3 (64K) vllm endpoint |
| **LLM Tech** | `https://api.llmtech.eu/v1` | 2M tok/day; shared trial key | EU; no signup, no card; qwen3.8-27b (probe-verified) |
|| **LLMTR** | `https://llmtr.com/v1` | Free on zero balance | Turkish keyless gateway; 27 free models Oct 23 across agnes-evren-heabsy-ifm-internlm-liquid-minimax-nace-nvidia-openai-poolside-qwen-voltropy; motif DEAD (absent probe); ling-3.1-flash DEAD Oct 13 |
|| **KeylessAI** | `https://keylessai.thryx.workers.dev/v1` | ☠️ DEAD Oct 22 2026 | ~~NEW Oct 21 v0.4.0;~~ DNS NXDOMAIN (Cloudflare DoH Status:3) + GitHub repo 404; aggregates Pollinations + ApiAirforce; `npm keylessai` / `npx keylessai serve`; works with Aider/Cline/Continue/Codex/Claude Code |

## 🗺️ stillworks (Dobby) — live keyless endpoint selector (NEW Oct 23)

- **Get:** `curl https://stillworks.supercapybara.com/api/llm/up` — no key, no signup
- **Returns:** ranked OpenAI-compatible no-auth endpoints (`auth_mode: none`, `last_ok`, `latency_ms`, `capabilities`) — currently FreeAI `qwen-coder`, OVHcloud `Qwen3Guard`, etc.
- **One-liner:** `curl https://stillworks.supercapybara.com/api/llm/up?format=env` → outputs `OPENAI_BASE_URL` / `OPENAI_API_KEY=not-needed` / `OPENAI_MODEL` for the current top pick
- **Catch (important):** this is a **discovery/routing head**, not a distinct model provider — it walks the keyless backends already tracked in this guide (Kilo Code / OVHcloud / LLM7 / FreeAI / VLM Run). Try it first for zero-signup calls, then fall through to a concrete provider if you need a specific model. Source: `github.com/bon5co/stillworks`

## 🧠 Google AI Studio (Gemini)
- **Get key:** https://aistudio.google.com/app/apikey
- **Limits:** Per-model limits no longer published (moved to per-project, console-gated in AI Studio since ~Oct 18). Flash / Pro / Flash-Lite all free; 1M context each.
- **base_url:** `https://generativelanguage.googleapis.com/v1beta`
- **Best:** `gemini-3.8-flash` (new), `gemini-2.5-pro` (best free reasoning)
- **Catch:** prompts may be used for training (not in EU/UK/CH).

## ⚡ Groq — fastest inference alive
- **Get key:** https://console.groq.com/keys
- **Limits:** 30 RPM / **1,000 RPD** (8K TPM); `gpt-oss-safeguard-20b` cut to **3 RPM / 2K TPM** Oct 6 2026 (console.groq.com/docs/rate-limits); 11 free no-card models incl. whisper + prompt-guard + orpheus TTS
- **base_url:** `https://api.groq.com/openai/v1`
- **Best:** `openai/gpt-oss-120b`, `qwen/qwen3.8-27b`
- **Free models (no card, 11 total):** `openai/gpt-oss-120b`, `openai/gpt-oss-20b`, `openai/gpt-oss-safeguard-20b` (safety), `qwen/qwen3.8-27b`, `whisper-large-v3` (STT), `whisper-large-v3-turbo` (STT), `meta-llama/llama-prompt-guard-2-22m` (safety), `canopylabs/orpheus-v1-english` (TTS), `canopylabs/orpheus-v1-arabic-saudi` (TTS)

## 🟠 Mistral
- **Get key:** https://console.mistral.ai/api-keys (free mode on by default)
- **Limits:** ~1 RPS; Free mode — allowance **unpublished/console-gated** (`$10/month free credits` removed Oct 7 2026; docs still promise included usage); no card — SMS/verify required
- **base_url:** `https://api.mistral.ai/v1`
- **Best:** `mistral-large-3`, `codestral` (code), `mistral-small-4` (vision)
- **Catch:** trains on your prompts unless you opt out; Moderation 2 + Shieldstral 1.0 free outright; Large 4 (preview) not surfaced in Free mode (Oct 2026 tests)

## 🟢 NVIDIA NIM — highest free daily volume
- **Get key:** https://build.nvidia.com (free dev program: sign up, verify phone, no card needed)
- **Limits:** 40 RPM, **no daily cap** per model; 91 models online (free dev program)
- **base_url:** `https://integrate.api.nvidia.com/v1`
- **Best:** `minimaxai/minimax-m3.1-flash` (NEW Oct 23; MiniMax M3.1 Flash, 265B dense, 1M ctx), `nvidia/nemotron-3-ultra-550b-a55b` (1M ctx), `deepseek-ai/deepseek-v4.1-flash` (NEW Oct 17; 552B MoE, 1M ctx), `z-ai/glm-5.3-flash` (NEW Oct 21; first natively multimodal GLM-5, 320B params, 1M ctx), `nvidia/nemotron-3.5-super-vl-120b-a12b` (NEW Oct 22; vision, 1M ctx), `stepfun-ai/step-5-preview` (NEW Oct 22; multimodal reasoning, 1M ctx), `meta/llama-4-maverick-17b-128e-instruct` (NEW Oct 22; 128-expert MoE), `qwen/qwen3-coder-480b-a35b-instruct` (NEW Oct 22; 480B coding MoE), `moonshotai/kimi-k2.6` (NEW Oct 22; 262K ctx, ⚠️ Unavailable on free-model.com), `01-ai/yi-large` (NEW Oct 22; ctx unknown), `openai/gpt-oss-20b` (NEW Oct 22; 128K ctx)
- **Free embedding/reranking:** `nvidia/nemotron-3.5-embed-1b` (1B, 32K ctx), `nvidia/nemotron-3.5-embed-8b` (8B, 32K ctx), `nvidia/nemotron-3.5-rerank-8b` (8B, 32K ctx) — NEW Oct 20; free on build.nvidia.com
- ⚠️ Oct 3: they killed nemotron-3-nano, llama-3.3-70b, gpt-oss-120b… free list rotates — check build.nvidia.com/models.

## Others worth a key (details in models.csv)
- **Cerebras** https://cerebras.ai — $5/30-day trial credit (card required; FAQ "no permanent free tier"); 5 RPM / 30K uncached tok/min / 1M tok/day per model; free trial models: gpt-oss-120b, Qwen3-235B, Qwen3.8-27B
- **Cohere** — 1,000 calls/month, non-commercial only
- **Cloudflare Workers AI** — 10K neurons/day, 60+ models
- **Ollama Cloud** — session (5h) + weekly caps, `https://ollama.com/v1`
- **APInex** (apinex.bond) — NEW Oct 2026 gateway; ~18 `:free` models at $0, ~10M tokens/day shared allowance, Google sign-in + daily sign-in; OpenAI-compatible base `https://api.apinex.bond/v1`
- **xKiro** (xkiro.com) — NEW Oct 2026; free-forever plan (no card), **21 free models** at $0, 500K tokens/day; OpenAI + Anthropic SDK compatible. base_url `https://api.xkiro.com/v1`; key `sk-xt-…` from [dashboard](https://xkiro.com/dashboard/api/keys). Top free: `longcat-2.5-preview:free` (262K), `qwen/qwen3.7-flash:free` (262K), `qwen/qwen3-max:free` (262K), `qwen/qwen3.8-max:free` (262K), `qwen/qwen3.7-max:free`. ⚠️ 5 Oct-21 top-free dropped from live listing (qwen3.8-27b, stealth/llama-3.1-70b, nemotron-3.5-super-vl, qwen3-32b, qwen2.5-72b). High-volume no-card alternative to OpenRouter
- **freelm** — installable free-only LLM gateway (LiteLLM alternative), pip/npm, auto-failover across OpenRouter/Groq/Gemini/Ollama free tiers (no card); github shihabshahrier/freelm (June 2026 tool, newly tracked Oct 21)
- **UnoRouter** — 🆕 NEW Oct 22; free-aggregator aggregating 18 provider APIs (OpenRouter/NVIDIA/Gemini/etc.); **190+ free models** at $0; key = free registration (unorouter.com/en/register, no card); ~1 req/min per model; OpenAI-compatible; models include `mistral-large-4:free`, `deepseek-v4.1-flash-1017:free`; base `https://api.unorouter.com/v1`
- **freellmpool** — installable free-only LLM gateway, pip/npm, auto-failover across 22 provider free tiers (Groq/NVIDIA/OpenRouter/Gemini/Cloudflare/Mistral/Cohere/.../LLM7); keyless start via Pollinations/OVH/Kilo/LLM7 (no card); local OpenAI-compatible proxy/CLI/library/MCP with per-day quota tracking; github 0xzr/freellmpool (NEW Oct 2026 v0.13.0)
- **omniroute** — 🆕 NEW Oct 2026 installable free AI gateway (MIT, GitHub `dbegineer/omniroute`, default branch `release/v3.8.49`): `npm install -g omniroute` then point any tool at `http://localhost:20128/v1`; **one endpoint routes across 290 providers / 90+ free tiers (40+ free forever, $0 no card)** — keyless out-of-box via wired-in OpenCode Free + Felo (a fresh install answers with no signup/config); pooled **~1.53B free tokens/mo** (up to ~2.15B first month w/ signup credits); auto-fallback circuit breakers, 19 routing strategies, RTK+Caveman compression, MCP+A2A+CLI, OpenAI↔Claude↔Gemini compat; built-in free-forever providers include Qoder (unlimited), Pollinations (no key), Kiro (~50 credits/mo), NVIDIA NIM, Z.AI GLM-Flash, SiliconFlow, Kilo, OpenCode Zen, Baidu; **15 ToS-flagged providers require explicit opt-in**; live budget at `/dashboard/free-tiers`
- **FreeTheAI** — 🆕 NEW Oct 2026 free OpenAI-compatible API (`https://api.freetheai.org/v1`; the old `api.freetheai.xyz` is dead): 50+ models, IDs `fta/<provider>/<model>` (e.g. `fta/zai/glm-5.3`); **no card** — free account (email/Discord confirm) + [daily check-in](https://freetheai.org/checkin) unlocks free models until 00:00 UTC; **50 requests/day** on free models (resets 00:00 UTC, failed requests don't count); streaming, tool calling, web search, image/video gen; MIT, GitHub `Free-The-Ai/free-ai` (35★); model list at `freetheai.org/models`
- **AnyAPI** — NEW Oct 2026 gateway (`https://api.anyapi.ai/v1`), 400+ models, OpenAI-compatible, permanent free tier (100K tokens/day free, no credit card); added to freellmapi as provider; key at dash.anyapi.ai
|- **IteraCompute** — 🆕 NEW Oct 22; OpenAI-compatible (`https://api.iteracompute.com/v1`); **1 model truly free** — `qwen/qwen3.8-27b` (262K ctx, 128K free tier); **30M tok/month** (signup key, no card); 160K TPM; key validation OFF; 120s timeout (queues at peak); ⚠️ `moonshotai/kimi-k3-free` ($0 pricing) requires $10 recharge — excluded from chain; 30 of 32 catalog models paid; key via iteracompute.com/signup
- **onomeo** — NEW Oct 21; OpenAI-compatible gateway (`https://onomeo.com/v1`), Bearer API-key; free models share 30 calls/5h per account (1,500 site-wide shared window); long requests count as 1 call per 50K chars; models delivered via signed catalog (Premium now, Free after 30-day gate); free answers branded "— via onomeo.com" (freellmapi adapter strips this); 403/429 = quota/throttle on valid key, not auth failure
| - **Z AI** (GLM-4.7-Flash, 200K ctx; GLM-4.6V-Flash NEW Oct 23, free vision; GLM-4.5-Flash DEAD Oct 22) — https://api.z.ai/api/paas/v1 intl endpoint
| - **BazaarLink** (bazaarlink.ai) — NEW Oct 21; free no-card API key (`bazaarlink.ai/keys`); OpenAI-compatible `https://api.bazaarlink.ai/v1`; shared free pool: 10 RPM / 60 wu-day (no card) or 20 RPM / 120 wu-day (credit); 20 RPM site cap, 2 concurrent, resets 00:00 UTC; 6 free models: qwen/qwen3.7-flash, reflection/beam (501B MoE agentic coder), reflection/beam-free, nvidia/nemotron-3.5-lightning-free, stealth/glyph-cluster, deepseek/deepseek-v4-flash-0731free; hourly probes Oct 21 ~96-100% success
| - **Hugging Face router** — $0.10/mo credit: `https://router.huggingface.co/v1`
- ❌ **GitHub Models — RETIRED July 2026.** Don't bother.
- **OpenCode Zen** (opencode.ai/zen/v1) — NEW Oct 2026; free account key (no card), OpenAI-compatible; **11 free `-free` models confirmed** (beam-free, mimo-v2.6-flash-free, jev-1.13-free, longcat-2.5-preview-free, deepseek-v4.1-flash-free, glm-5.3-flash-free, nemotron-3.5-lightning-free, nemotron-3.5-super-vl-free, flint-40b-free, **big-pickle**, **nemotron-3-ultra-free**). ⚠️ promo/limited-time, data may be logged, direct API fingerprint-gated.
|- **FreeLLMAPI** (tashfeenahmed/freellmapi) — 🆕 NEW Oct 2026 v0.16.8 installable free-only LLM gateway (pip/npm/Docker `ghcr.io/tashfeenahmed/freellmapi`, Node.js 24); **34 free LLM providers / 635 endpoints / 474 model families / 7.4B tok/mo** pooled; OpenAI + **Anthropic `/v1/messages`** compat (Claude Code + Anthropic SDKs run against free pool); MCP server at `/mcp`; image/video/speech gen; tool calling + structured outputs; self-updating signed catalog; setup CLI for Claude Code/Codex/Aider/Cline/Roo/Continue/Cursor; custom local provider support (Ollama/vLLM/llama.cpp); IteraCompute adapter; **Keenable keyless web search**; `npx freellmapi` → http://localhost:3001; 34 free providers incl. 10 not tracked individually: SEA-LION, NavyAI, NaraRouter, Aion, Requesty, AI Horde, Routeway, AINative, Keenable (BazaarLink + onomeo tracked separately)

||- **FreeRide** (api.free-ride.xyz) — installable free-only LLM gateway; local OpenAI-compatible proxy at `http://localhost:11343/v1`; 290+ providers/90+ free tiers (~1.53B tok/mo pooled, up to ~2.15B first month w/ signup credits); routes OpenRouter/Groq/Gemini/NVIDIA NIM/Cloudflare/HuggingFace/Z.ai/xKiro/Ollama Cloud/Kilo/OpenCode Zen/OVHcloud/BlockRun + 17 more; keyless start via Qoder (unlimited)/Pollinations/Kiro (~50 credits/mo)/Kilo/OVHcloud anonymous (2 RPM)/BlockRun anonymous (30 req/min); OpenAI+Anthropic SDK + CLI + MCP; works with Aider/Continue.dev/Codex/Claude Code; no paid fallback; github Shaivpidadi/FreeRideV3
||- **FreeAI** (free.ai) — OpenAI-compatible API gateway at `https://api.free.ai/v1`; EU-hosted; free tier 30K tok/day + 1000 req/month + 60 RPM, no card required (free applies until payment method linked); 588 models via BYOK; keyless start on some models (9 of 513 verified Oct 2026); api key `sk-free-…` from [free.ai/api](https://free.ai/api/)
|- 🆕 **Inception Labs** — `mercury-3`: 1M-ctx diffusion LLM; free 100M tokens one-time (no card, no payment method); reasoning + tool calling; OpenAI-compatible `https://api.inceptionlabs.ai/v1`; ~1,068 tok/sec; also on OpenRouter / Baseten / Vercel
- 🆕 **Baseten** — Mammoth-1 (27B) + Elephant-1 (9B): free on Vercel AI Gateway thru Oct 27; #1 Jev Decision Index (Mammoth) / tied-#1 Artificial Analysis Decision Index (Elephant); 16K ctx; classify / route / score (tool, not chat); `vercel.com/ai-gateway/models`
---

## 🏆 Recommended stack (coding/agent use)
1. **OpenRouter `nvidia/nemotron-3-ultra-550b-a55b:free`** — biggest brain, 1M ctx
2. → fallback `openrouter/free` (auto-router over 22 models, survives single-model outages)
3. → fallback **NVIDIA NIM `nvidia/nemotron-3-super-120b-a12b`** (40 RPM, no daily cap)
4. → fallback **Groq `openai/gpt-oss-120b`** (1,000 RPD, instant)
5. → fallback **Gemini 3.8 Flash** (limits now console-gated / not published per-model since ~Oct 18)
6. → fallback **APInex `free/deepseek-v4.1-flash`** (10M tokens/day, Google sign-in only; Oct 2026)
7. → fallback **OpenCode Zen `glm-5.3-flash-free`** (free account key; promo, may log data)
8. → emergency no-key: **Kilo Code** (200/hr, works even if all keys die)

**One-time power move:** buy $10 OpenRouter credits once → all free models jump from 50 → 1,000 RPD forever.

## 📰 Recent news (Oct 19–26, 2026)
||- 🆕 **Oct 26**: **Infron AI** (aifree.dev / api.infron.ai) — free OpenAI-compatible gateway; 6 `:free` models confirmed via live `/v1/models` probe; 1,000 req/day per account, $0/token, $5+ balance anti-abuse (never consumed); no credit card required; `qwen/qwen3.8-27b:free` (256K) was DEAD on xKiro Oct 22 — now ALIVE; `deepseek/deepseek-v4.1-flash:free` (1M ctx), `qwen/qwen3.8-27b-abliterated-cyber:free` (256K), `internlm/atria-dawn-preview:free` (256K), `inclusionai/ling-3.1-flash:free` (262K, REANIMATED — was DEAD on LLMTR L136 Oct 13), `apodex/apodex-1.1-mini:free` (262K, already tracked on OpenRouter L25) (Oct 26)
||- 🆕 **Oct 26**: **AIHubMix** (aihubmix.com / api.aihubmix.com/v1) — free OpenAI-compatible gateway; 64 free models at $0/M; 10 trial calls no card (never expire) + ~$100 req/day after $1 top-up; notable new free model IDs: `qwen3.8-max-free` (1M), `qwen3.8-flash-free` (1M), `wan3.0-video-free` + `wan3.0-video-prime-free` (first free video gen, 10/day 1/min), `coding-glm-5.3-free` + `coding-glm-5.3-flash-free` + `coding-glm-5.2-free` + `coding-glm-5-free` (GLM-5.x coding, 1M), `coding-kimi-k3-free` (1.05M), `laguna-s-2.1-free` + `laguna-xs-2.1-free` (1.05M); models list aihubmix.com/models/free (Oct 26)
|||
||- 🆕 **Oct 23**: **FreeRide** (api.free-ride.xyz) — v0.4.0a26 installable free-only LLM gateway; pip install freeride-gateway / curl -sSL https://api.free-ride.xyz/install.sh | sh / Docker; local proxy http://localhost:11343/v1; 290+ providers/90+ free tiers (~1.53B tok/mo pooled, up to 2.15B first month w/ credits); routes OpenRouter/Groq/Gemini/NVIDIA NIM/Cloudflare/HuggingFace/Z.ai/xKiro/Ollama Cloud/Kilo/OpenCode Zen/OVHcloud/BlockRun + 17 more; keyless start via Qoder (unlimited)/Pollinations/Kiro (~50 credits/mo)/OVHcloud anonymous (2 RPM)/BlockRun anonymous (30 req/min); no paid fallback; github Shaivpidadi/FreeRideV3 (Oct 23)
||- 🆕 **Oct 23**: **FreeAI** (free.ai) — OpenAI-compatible gateway https://api.free.ai/v1; EU-hosted; free tier 30K tok/day + 1000 req/month + 60 RPM, no card (free applies until payment method linked); 588 models via BYOK; keyless on 9 of 513 models verified Oct 2026; api key sk-free-… from free.ai/api (Oct 23)
||- 🔄 **Oct 23**: OpenRouter free pool grows to **22 models** — `scaledown/summarize` (1M ctx, abstractive text+image+file summarization, $0 completion, max 4K output) + `scaledown/extract` (1M ctx, description-driven entity extraction, $0 completion, max 900K output). Live on `/v1/models` API (verified); `minimax/m3.1-flash:free` confirmed DEAD (absent from API).
- 🆕 **Inception Labs Mercury 3** (`mercury-3`): NEW Oct 20; free 100M tokens (one-time, no card); 1M-ctx diffusion LLM; reasoning + tool calling; OpenAI-compatible `https://api.inceptionlabs.ai/v1`; ~1,068 tok/sec; also on OpenRouter/Baseten/Vercel
- 🆕 **Baseten Mammoth-1 (27B) + Elephant-1 (9B)**: NEW Oct 20; free on Vercel AI Gateway thru Oct 27; #1 Jev Decision Index / tied-#1 AA Decision Index; 16K ctx; classify/route/score (tool, not chat); `vercel.com/ai-gateway/models`
- 🔄 OpenRouter free pool now **22 models** (17 `:free` + 5 `$0` non-`:free` — scaledown/summarize, scaledown/extract, lyria-3-clip-preview, lyria-3-pro-preview, openrouter/free): `recursive/flint-v1.0:free` (262K ctx) (Oct 21); gemma-4-26b-a4b-it:free, gemma-4-31b-it:free, inkling:free + inkling-small:free, laguna-xs-2.1:free, lfm-2.5-2.6b:free, nemotron-3-nano-omni-30b-a3b-reasoning:free, content-safety:free, dots-3-note-preview:free, lyria-3 audio (clip+pro, $0) (Oct 20); scaledown/summarize + scaledown/extract (1M ctx, $0 completion, Oct 23)
- ☠️ OpenRouter: `inclusionai/ling-3.0-flash-fin:free` + `ling-3.0-flash-sante:free` DEAD — not found on OpenRouter API or Kilo gateway (Oct 21)
- 🆕 Kilo Code: `reflection/beam-free` (1M ctx) + `stealth/glyph-cluster` (256K ctx) + `kilo-auto/free` (256K ctx, auto-router over free pool) now free, no key needed (Oct 21)
- ☠️ Kilo Code: `stepfun/step-3.7-flash:free`, `tencent/hy3:free`, `apinex/apodex-1.1-mini:free` DEAD — 404 or priced on Kilo gateway
- 🔄 **Oct 23 probe update**: OpenCode Zen: **11 `-free` models live** (beam-free, mimo-v2.6-flash-free, jev-1.13-free, deepseek-v4.1-flash-free, glm-5.3-flash-free, nemotron-3.5-lightning-free, nemotron-3.5-super-vl-free, flint-40b-free, **big-pickle**, **longcat-2.5-preview-free**, **nemotron-3-ultra-free**); 🪦 `minimax-m3.1-flash-free` DEAD Oct 23 (absent from `/zen/v1/models`); `FreeTierError` keyless `/zen/v1/chat/completions` probe confirms big-pickle + longcat + nemotron-3-ultra-free active on free tier (app-only, OpenCode)
- 🔄 NVIDIA NIM: Oct 22 probe of `integrate.api.nvidia.com/v1/models` returns **83 total models** (was 77 Oct 20; was incorrectly reported as 91); `deepseek-ai/deepseek-v4.1-flash` + `z-ai/glm-5.3-flash` + `nvidia/nemotron-3.5-super-vl-120b-a12b` + `stepfun-ai/step-5-preview` verified live; 4 of 8 Oct-22 claimed NIM additions absent from /v1/models: `meta/llama-4-maverick-17b-128e-instruct`, `qwen/qwen3-coder-480b-a35b-instruct`, `minimaxai/minimax-m2.7`, `mistralai/mistral-nemotron`, `bytedance/seed-oss-36b-instruct`, `stepfun-ai/step-3.5-flash` (tracked per ASSERT-KTH build.nvidia.com list, not in /v1 API)
- 🆕 Google lyria-3 clip+pro audio models now free on OpenRouter (pricing $0, no `:free` suffix)
- 🆕 NVIDIA NIM: `deepseek-ai/deepseek-v4.1-flash` (552B MoE, 1M) added to free catalog Oct 17; 40 RPM / no daily cap
- 🆕 APInex (apinex.bond) gateway: ~18 free/free models, ~10M tokens/day allowance, Google sign-in only (no card)
- ☠️ qwen3.8-27b:free left OpenRouter Oct 20 (still free on Groq + OVH, NOT Kilo — priced on gateway)
- 🆕 Z.ai GLM-5.3-Flash (320B params, 18B active, natively multimodal) now free on NVIDIA NIM Oct 2026
- ☠️ NVIDIA NIM: `z-ai/glm-5.3` (non-flash, 753B text MoE, 1M ctx, FP8) DEAD Oct 28 2026 — deprecated 10/27/26 per build.nvidia.com; `z-ai/glm-5.3-flash` unaffected, migrate to it
- 🆕 NVIDIA NIM: `diffusiongemma-26b-a4b-it` (26B diffusion text-gen, parallel token gen) + `paligemma` (vision-language) now on build.nvidia.com free_endpoint filter
- 🔄 NVIDIA NIM: `deepseek-ai/deepseek-v4.1-flash` (552B MoE, 1M) added Oct 17; 40 RPM / no daily cap
- 🆕 BlockRun.ai: verified keyless, no signup, no card; **9 free NVIDIA-hosted models** incl. nemotron-3-ultra-550b (1M ctx) + nano-omni-30b-a3b-reasoning (256K) + llama-3.2-11b-vision (128K) + **nemotron-3.5-lightning** (1M) + **cohere/north-mini-code** (256K) + **poolside/laguna-xs-2.1** (262K) + **muse-glimmer-30b** (1M) + **gpt-oss-20b** (128K, keyless by direct ID) + **nemotron-super-49b** (131K, ⚠️ returns 200 but remaps to nemotron-3-super-120b, not a distinct free model); auto-routes unlisted model names
- 🆕 uncloseai: verified keyless Qwen3.8-27B-exl3 (64K) vllm endpoint live, no signup
- 🆕 LLM Tech (llmtech.eu): shared trial key (no card, no signup), 2M tok/day, qwen3.8-27b; EU-hosted (probe-verified list)
- 🆕 LLMTR (llmtr.com): Turkish keyless gateway, 27 free models Oct 23 across agnes-evren-heabsy-ifm-internlm-liquid-minimax-nace-nvidia-openai-poolside-qwen-voltropy; ☠ motif DEAD (absent probe); ling-3.1-flash DEAD Oct 13
- ☠️ **LLM7.io: both cataloged models PAID** (`gpt-oss:20b` turbo tier, `deepseek-v4-flash-0731` pro tier) — removed from free tracking Oct 21
- 🔄 **SambaNova free tier REACTIVATED** (Oct 21 Gravity + vava-nessa Oct 17): no card required (free applies until payment method linked); 20 RPM / 20 RPD / 200K tok/day per model; DeepSeek-V3.1 / Llama 3.3 70B / gpt-oss-120b (+ DeepSeek-V3.2, Gemma 4 31B preview)
- 🆕 **OVHcloud: 11 free chat models** no key/no signup (EU-hosted): Qwen3.5-397B (262K), Qwen3.8-27B (262K), gpt-oss-20b (131K), gpt-oss-120b (128K), Llama-3.3-70B (128K), Mistral-Small-3.2-24B (128K), Mistral-Nemo (128K), Qwen2.5-VL-72B (128K), Qwen3.5-9B (128K), Qwen3.6-27B (262K), Qwen3Guard variants
- 🆕 **xKiro: 21 free models** (500K tok/day per IP, dashboard API key); top: longcat-2.5-preview:free (262K), qwen/qwen3.7-flash:free (262K), qwen/qwen3.8-27b:free, qwen/qwen3.8-max:free (262K), qwen/qwen3.7-max:free; OpenAI/Anthropic SDK compatible — ⚠️ 5 Oct-21 free models dropped (qwen3.8-27b, stealth/llama-3.1-70b, nemotron-3.5-super-vl, qwen3-32b, qwen2.5-72b)
- 🆕 **NVIDIA NIM: +8 free models Oct 22** (build.nvidia.com Free Endpoint, 40 RPM no daily cap): `nvidia/nemotron-3.5-super-vl-120b-a12b` (vision, Oct 15), `stepfun-ai/step-5-preview` (multimodal reasoning, Oct 14), `meta/llama-4-maverick-17b-128e-instruct` (128-expert MoE), `qwen/qwen3-coder-480b-a35b-instruct` (480B coding MoE), `minimaxai/minimax-m2.7` (230B MoE), `mistralai/mistral-nemotron` (reinstated after Oct 3 rotation), `bytedance/seed-oss-36b-instruct`, `stepfun-ai/step-3.5-flash`; dual-confirmed build.nvidia.com Free Endpoint + ASSERT-KTH/nvidia-free-endpoints programmatic list; added to models.csv + chain.json fallback routing
- 🆕 BazaarLink (bazaarlink.ai): NEW Oct 21 free-aggregator, no card; **7 unique free models Oct 22** — reflection/beam, reflection/beam-free, nvidia/nemotron-3.5-lightning-free, stealth/glyph-cluster, deepseek/deepseek-v4-flash-0731free, qwen/qwen3.7-flash:free (bare qwen/qwen3.7-flash now PRICED — free id uses `:free` suffix), **auto:free** router NEW; 10 RPM/60 wu-day (no card) or 20/120 (credit); OpenAI-compatible https://api.bazaarlink.ai/v1; hourly probes ~96-100% (Oct 21 17:46)
- 🔄 **SambaNova free tier REACTIVATED** (Oct 21 Gravity + vava-nessa Oct 17): was "all paid / card required since Aug 14"; now free tier live, NO card needed (free applies until payment method linked); 20 RPM / 20 RPD / 200K tok/day per model; DeepSeek-V3.1 / Llama 3.3 70B / gpt-oss-120b (+ DeepSeek-V3.2, Gemma 4 31B preview)
- 🔄 **Cerebras reclassified**: was "~30 RPM dev tier, llama-3.3-70b, payment method required"; now $5/30-day trial credit (card required; FAQ "no permanent free tier"); limit ~30 RPM → 5 RPM / 30K tok/min / 1M tok/day per model; free trial models gpt-oss-120b + Qwen3-235B (+Qwen3.8-27B)
- 🆕 **Oct 22**: NVIDIA NIM free catalog adds `moonshotai/kimi-k2.6` (262K ctx), `01-ai/yi-large` (ctx unknown), `openai/gpt-oss-20b` (128K ctx); free pricing verified via `/v1/models` API (no pricing key = free); ⚠️ kimi-k2.6 marked "Unavailable" on free-model.com.
- 🆕 **Oct 22**: **UnoRouter** (api.unorouter.com/v1) — free-aggregator with **190+ free models** from 18 providers at $0; free key via registration (no card); ~1 req/min per model; newly tracked models: `mistral-large-4:free`, `deepseek-v4.1-flash-1017:free`.
- 🪦 **Oct 22 probe update**: Kilo Code no-key gateway **5→20 free** (15 added: flint-v1.0:free, xing4.0-29b-a4b:free, dots-3-note-preview:free, lfm-2.5-2.6b:free, nemotron-3.5-lightning:free, laguna-xs-2.1:free, cohere/north-mini-code:free, nemotron-3.5-content-safety:free, nemotron-3-nano-omni-30b-a3b-reasoning:free, nemotron-3-super-120b-a12b:free, minimax-m3.1-flash:free, nemotron-3.5-super-vl:free, lyria-3-pro-preview, lyria-3-clip-preview, openrouter/free); new ids use `:free` suffix (mirrors full OpenRouter free pool).
- 🔄 **Oct 23 correction**: OpenCode Zen `longcat-2.5-preview-free` — was **DEAD** (Oct 22); now **REVIVED** — absent from `/zen/v1/models` keyless listing BUT `FreeTierError` keyless `/zen/v1/chat/completions` probe confirms active free tier (app-only, OpenCode); corroborated in Zen docs catalog.
- 🪦 **Oct 22 probe update**: Groq `groq/compound` & `groq/compound-mini` **DEAD** (shut down Sept 21 2026 per Groq deprecations — `https://console.groq.com/docs/deprecations`, confirmed via live fetch; aifree.dev's Groq page returns HTTP 404, so the earlier "verified aifree.dev" stamp was stale). Groq's published table now lists only `openai/gpt-oss-120b`, `openai/gpt-oss-20b`, `qwen/qwen3.8-27b`; compound/compound-mini had no announced replacement.
- 🪦 **Oct 22 probe update**: BazaarLink **6→7 unique free**; `auto:free` router NEW; bare `qwen/qwen3.7-flash` now PRICED — free id is `qwen/qwen3.7-flash:free`.
|- 🆕 **Oct 23**: **FreeLLMAPI** (tashfeenahmed/freellmapi) v0.16.8 — installable free-only LLM gateway (Node.js 24.22.1 runtime); **34 providers / 635 endpoints / 7.4B tok/mo**; **NEW Anthropic `/v1/messages`** API support (Claude Code + Anthropic SDKs run against free pool); MCP server at `/mcp`; image/video/speech generation; tool calling + structured outputs; self-updating signed catalog; `npx freellmapi` or Docker `ghcr.io/tashfeenahmed/freellmapi` → http://localhost:3001; setup CLI for Claude Code/Codex/Aider/Cline/Roo/Continue/Cursor; custom local provider support (Ollama/vLLM/llama.cpp); **NEW IteraCompute adapter** (qwen/qwen3.8-27b, premium now — free tier 21 Nov); **NEW Keenable keyless web search**; 10 new free providers not tracked individually: SEA-LION, NavyAI, NaraRouter, Aion, Requesty, AI Horde, Routeway, AINative, Keenable
|- 🆕 **Oct 22**: **FreeLLM-API-KeyHub** (guihuashaoxiang/FreeLLM-API-KeyHub) — curated reference list tracking **22 Chinese LLM providers (178 routes / 431 models)** incl. SiliconFlow, Volcengine Ark, ZhiPu AI, Meituan LongCat, Alibaba BaiLian, Baidu QianFan; 277 stars, updated Oct 22; keyless start when available; not a direct API (monitoring source only)
|- 🆕 **Oct 23**: **Reflection Beam on Ollama Cloud** (`beam:cloud`) — free limited-time with zero data retention (ZDR); 501B/23B MoE agentic coder; 1M ctx; Apache 2.0; access via `ollama run beam:cloud` or `ollama launch claude --model beam:cloud`; requires Ollama Cloud account (no card to get free tier key); tracked in models.csv + chain.json (Oct 23)
|- ☠️ **Oct 23**: **LL Alpha Free** (`opencode/ll-alpha-free`) — DEAD; 262K ctx stealth model, was free Oct 16–20 on OpenCode Zen, removed Oct 20; never load-tested (freetokens timeline)
|- ☠️ **Oct 23**: **Cat Jam** — DEAD; 1M ctx stealth model, was free Oct 16–20 on OpenCode Zen/Go/Vercel AI Gateway, removed Oct 20 (freetokens timeline)
- ☠️ **Oct 26 cron**: NVIDIA NIM `z-ai/glm-5.3` (non-flash, 753B text MoE, 1M ctx, FP8) DEAD Oct 28 2026 — deprecated 10/27/26 per build.nvidia.com; `z-ai/glm-5.3-flash` unaffected, migrate
- 🔄 **Oct 26 cron**: `scaledown/summarize` + `scaledown/extract` (OpenRouter) prompt price ticked $0 → $0.00000004/token (completion still $0; still effectively free, NOT dead); corrects prior "$0" claim — live /v1/models verified

## 🔑 keyless-llm-api (nafigamer0) — deploy-your-own keyless proxy
- **Get:** `npx wrangler deploy` from [nafigamer0/Keyless-LLM-API](https://github.com/nafigamer0/Keyless-LLM-API) (Cloudflare Worker, single file, NEW Oct 23)
- **base_url:** `https://keyless-llm.nafimods.workers.dev/v1` (verified HTTP 200)
- **Pools 5 keyless gateways:** Kilo Code (nemotron-ultra, poolside, cohere, reflection, flint), VLM Run (qwen3.8-27b/3.5-0.8b/diffusiongemma), OVHcloud (gpt-oss-120b, Qwen3.5-397b, Llama-3.3-70b), DeepAI (deepseek-v3.2, gemma-4, gemini-2.5-flash-lite), Pollinations (gpt-oss-20b)
- **Catch:** auto-failover across upstreams; deploy your own to control rate limits; ~600 req/h pooled

## 🌐 VLM Run — keyless vision+text
- **base_url:** `https://gateway.vlm.run/v1/openai` (verified HTTP 200)
- **Limits:** 10 req/min, 30 req/hour, 100 req/day per IP
- **Models (live list):** `google/gemini-3.5-flash-lite`, `google/gemini-3.7-flash`, `meta/muse-spark-1.2`, `qwen/qwen3.8-27b`, `diffusiongemma`
- **Catch:** truly keyless (no signup); Google-Vertex Gemini models served keyless; verify with `curl gateway.vlm.run/v1/openai/models`

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
