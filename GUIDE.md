# Free LLM API Guide — updated 2026-10-25

Every provider below is OpenAI-SDK-compatible. Point any tool at `base_url` + key and go.
Full model table: `models.csv` (same folder). Auto-maintained by the `freellm-watch` cron agent.

---

## ⭐ OpenRouter — the one key to rule them all
- **Get key:** https://openrouter.ai/keys (Google login, 30 sec)
- **Limits:** 20 RPM, **50 req/day per free model** → jumps to **1,000/day** after a one-time $10 credit buy
- **base_url:** `https://openrouter.ai/api/v1`
- **Best free models:** `nvidia/nemotron-3-ultra-550b-a55b:free` (1M ctx), `nvidia/nemotron-3-super-120b-a12b:free`, `nvidia/nemotron-3.5-lightning:free`, `poolside/laguna-s-2.1:free` (code), `google/gemma-4-31b-it:free`, `thinkingmachines/inkling:free` (reasoning), `google/lyria-3-pro-preview` (audio, $0), `recursive/flint-v1.0:free` (262K ctx)
- **Trick:** model = `openrouter/free` auto-routes across all 22 free models. Or pass a `models: [...]` array for built-in fallback.

## 🚪 No-key options (zero signup)
| Provider | base_url | Limit | Catch |
|---|---|---|---|
| **Kilo Code** | `https://api.kilo.ai/api/gateway` | 200 req/hr per IP | Logs prompts; has nemotron-ultra 1M free |
| **OVHcloud** | `https://oai.endpoints.kepler.ai.cloud.ovh.net/v1` | 2 RPM per IP/model | EU-hosted, slow trickle |
| **BlockRun.ai** | `https://blockrun.ai/api/v1` | 429 per IP; keyless | Verified Oct 21; 7 NVIDIA-hosted OS free models: nemotron-3-ultra-550b (1M), nano-omni-30b-a3b-reasoning (256K), llama-3.2-11b-vision (128K), nemotron-3.5-lightning (1M), cohere/north-mini-code (256K), poolside/laguna-xs-2.1 (262K), muse-glimmer-30b (1M) |
| **uncloseai** | `https://hermes.ai.unturf.com/v1` | 429 per IP; keyless | Verified Oct 21; single Qwen3.8-27B-exl3 (64K) vllm endpoint |
| **LLM Tech** | `https://api.llmtech.eu/v1` | 2M tok/day; shared trial key | EU; no signup, no card; qwen3.8-27b (probe-verified) |
|| **LLMTR** | `https://llmtr.com/v1` | Free on zero balance | Turkish keyless gateway; 27 free models Oct 23 across agnes-evren-heabsy-ifm-internlm-liquid-minimax-nace-nvidia-openai-poolside-qwen-voltropy; motif DEAD (absent probe); ling-3.1-flash DEAD Oct 13 |
|| **KeylessAI** | `https://keylessai.thryx.workers.dev/v1` | ⚠️ REVIVED Oct 26 2026 | ~~NEW Oct 21 v0.4.0;~~ DNS NXDOMAIN Oct 22 (Cloudflare DoH Status:3); GitHub repo `lordbasilaiassistant-sudo/keylessai` recovered (3 stars, `npm keylessai` v0.4.0); aggregates Pollinations + ApiAirforce w/ adaptive failover (endpoint unverified); `npm keylessai` / `npx keylessai serve`; works with Aider/Cline/Continue/Codex/Claude Code |
|| **Animica** | `https://animica.dev/v1` | 30 req/min per IP (burst 12) keyless | ✨ NEW Oct 26; free keyless OpenAI-compatible endpoint; models: `kimi-k3` (DeepSeek R1 distill 32B, 1M ctx), `animica-chat`, `animica-chat-small`, `animica-knowledge` (180K ctx), `animica-embed`; no key/signup/card; CLI: `npm install -g animica` / `animica chat`; media endpoints (images/video/audio); CORS-enabled; live HTTP 200 on /v1/models + chat completion with `kimi-k3` confirmed Oct 26 |

## 🗺️ stillworks (Dobby) — live keyless endpoint selector (NEW Oct 23)

- **Get:** `curl https://stillworks.supercapybara.com/api/llm/up` — no key, no signup
- **Returns:** ranked OpenAI-compatible no-auth endpoints (`auth_mode: none`, `last_ok`, `latency_ms`, `capabilities`) — currently FreeAI `qwen-coder`, OVHcloud `Qwen3Guard`, etc.
- **One-liner:** `curl https://stillworks.supercapybara.com/api/llm/up?format=env` → outputs `OPENAI_BASE_URL` / `OPENAI_API_KEY=not-needed` / `OPENAI_MODEL` for the current top pick
- **Catch (important):** this is a **discovery/routing head**, not a distinct model provider — it walks the keyless backends already tracked in this guide (Kilo Code / OVHcloud / LLM7 / FreeAI / VLM Run). Try it first for zero-signup calls, then fall through to a concrete provider if you need a specific model. Source: `github.com/bon5co/stillworks`

## 🧠 Google AI Studio (Gemini)
- **Get key:** https://aistudio.google.com/app/apikey
- **Limits:** Per-model limits no longer published (moved to per-project, console-gated in AI Studio since ~Oct 18). Flash / Flash-Lite free; 1M context each. **Pro removed from free tier Oct 25** — use Gemini 2.5 Flash (15 RPM / 1,500 RPD) instead.
- **base_url:** `https://generativelanguage.googleapis.com/v1beta`
- **Best:** `gemini-3.8-flash` (new), `gemini-2.5-flash` (best free reasoning, replaces Pro removed Oct 25)
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
- ⚠️ Oct 28: `nvidia/nemotron-3-super-120b-a12b` DEAD on NVIDIA NIM (deprecated Oct 27); still free on LLMTR gateway — see chain.json fallback.

## 🟢 Token Harbor — unified free LLM aggregator gateway
- **Get key:** https://tokenharbor.ai/signup (free signup, bearer token)
- **Limits:** Free rolling 7-day allowance per user; `:free` suffix models never bill
- **base_url:** `https://tokenharbor.ai/v1`
- **Best:** `claude-haiku-5.5:free` (200K ctx, free limited-time Oct 7 campaign), `deepseek-v4.1-flash:free` (1M ctx), `deepseek-v4-flash:free` (1M ctx), `mimo-v2.6-flash:free` (1M ctx), `mimo-v2.5:free` (1M ctx)
- **Note:** NEW Oct 26; aggregates OpenRouter/Groq/DeepSeek/etc into single `$0/token` gateway

## 🟢 InferAll — free NVIDIA NIM gateway
- **Get key:** https://api.inferall.ai/signup (free signup; $5 one-time starter pack → spendable balance)
- **Limits:** 50 chat / 100 text per day shared pool across 10 NIM models; $0/token; 127 models total
- **base_url:** `https://api.inferall.ai/v1`
- **Best:** `nvidia/nemotron-3-ultra-550b-a55b` (1M ctx), `z-ai/glm-5.3-flash` (1M ctx), `openai/gpt-oss-20b` (128K ctx)
- **Note:** NEW Oct 26; OpenAI+Anthropic SDK compatible; key prefix `ifu_`

## 🟢 FHRouter — free no-card frontier gateway
- **Get key:** https://fhrouter.com (free signup, no credit card)
- **Limits:** 3 always-free frontier models; no credit card, no expiring trial, free for everyone (single account key); rate-limited per model (unpublished); no keyless access
- **base_url:** `https://fhrouter.com/v1`
- **Models:** `grok-4.6`, `deepseek-v4-flash`, `glm-5.3-flash`
- **Note:** NEW Oct 25; OpenAI+Anthropic SDK compatible; live HTTP 200 + GitHub repo `fhrouter/fhrouter` verified Oct 25; `/v1/models` requires account key (no keyless); context + rate limits unpublished

## 🟢 Hetzner Inference (experimental)

Free while experimental • OpenAI-compatible • EU infrastructure • no SLA

| Model | Shape | Context | Modalities | Free limit (per key) |
|---|---|---|---|---|
| `Qwen/Qwen3.6-35B-A3B-FP8` | Causal LM + Vision (MoE 35B total / 3B active) | 262K | text, image | 4M in / 100k out per 60s · 10 req/60s per key; no daily cap |
| `Qwen3.8-27B` | Dense (27B) | 262K | text, image | same |

**Key:** Obtain a free token at `experiments.hetzner.com` → Inference → Create API Token (no credit card). Base URL: `https://inference.hetzner.com/api/v1`.

**Hermes:** Install `iamimmanuelraj/hermes-hetzner-provider` — `git clone https://github.com/iamimmanuelraj/hermes-hetzner-provider ~/.hermes/plugins/model-providers/hetzner`

## Others worth a key (details in models.csv)
- **Cerebras** https://cerebras.ai — $5/30-day trial credit (card required; FAQ "no permanent free tier"); 5 RPM / 30K uncached tok/min / 1M tok/day per model; free trial models: gpt-oss-120b, Qwen3-235B, Qwen3.8-27B
- **Cohere** — 1,000 calls/month, non-commercial only
- **Cloudflare Workers AI** — 10K neurons/day, 60+ models
- **Ollama Cloud** — credit-based $0 (no card); session caps replaced by credit pool Oct 8; base `https://ollama.com/v1`
- **APInex** (apinex.bond) — NEW Oct 2026 gateway; ~18 `:free` models at $0, ~10M tokens/day shared allowance, Google sign-in + daily sign-in; OpenAI-compatible base `https://api.apinex.bond/v1`
- **xKiro** (xkiro.com) — NEW Oct 2026; free-forever plan (no card), **21 free models** at $0, 500K tokens/day; OpenAI + Anthropic SDK compatible. base_url `https://api.xkiro.com/v1`; key `sk-xt-…` from [dashboard](https://xkiro.com/dashboard/api/keys). Top free: `longcat-2.5-preview:free` (262K), `qwen/qwen3.7-flash:free` (262K), `qwen/qwen3-max:free` (262K), `qwen/qwen3.8-max:free` (262K), `qwen/qwen3.7-max:free`. ⚠️ 5 Oct-21 top-free dropped from live listing (qwen3.8-27b, stealth/llama-3.1-70b, nemotron-3.5-super-vl, qwen3-32b, qwen2.5-72b). High-volume no-card alternative to OpenRouter
- **freelm** — installable free-only LLM gateway (LiteLLM alternative), pip/npm, auto-failover across OpenRouter/Groq/Gemini/Ollama free tiers (no card); github shihabshahrier/freelm (June 2026 tool, newly tracked Oct 21)
- **UnoRouter** — 🆕 NEW Oct 22; free-aggregator aggregating 18 provider APIs (OpenRouter/NVIDIA/Gemini/etc.); **190+ free models** at $0; key = free registration (unorouter.com/en/register, no card); ~1 req/min per model; OpenAI-compatible; models include `mistral-large-4:free`, `deepseek-v4.1-flash-1017:free`; base `https://api.unorouter.com/v1`
- **freellmpool** — installable free-only LLM gateway, pip/npm, auto-failover across 22 provider free tiers (Groq/NVIDIA/OpenRouter/Gemini/Cloudflare/Mistral/Cohere/.../LLM7); keyless start via Pollinations/OVH/Kilo/LLM7 (no card); local OpenAI-compatible proxy/CLI/library/MCP with per-day quota tracking; github 0xzr/freellmpool (NEW Oct 2026 v0.13.0)
- **omniroute** — 🆕 NEW Oct 2026 installable free AI gateway (MIT, GitHub `dbegineer/omniroute`, default branch `release/v3.8.49`): `npm install -g omniroute` then point any tool at `http://localhost:20128/v1`; **one endpoint routes across 290 providers / 90+ free tiers (40+ free forever, $0 no card)** — keyless out-of-box via wired-in OpenCode Free + Felo (a fresh install answers with no signup/config); pooled **~1.53B free tokens/mo** (up to ~2.15B first month w/ signup credits); auto-fallback circuit breakers, 19 routing strategies, RTK+Caveman compression, MCP+A2A+CLI, OpenAI↔Claude↔Gemini compat; built-in free-forever providers include Qoder (unlimited), Pollinations (no key), Kiro (~50 credits/mo), NVIDIA NIM, Z.AI GLM-Flash, SiliconFlow, Kilo, OpenCode Zen, Baidu; **15 ToS-flagged providers require explicit opt-in**; live budget at `/dashboard/free-tiers`
- **FreeTheAI** — 🆕 NEW Oct 2026 free OpenAI-compatible API (`https://api.freetheai.org/v1`; the old `api.freetheai.xyz` is dead): 50+ models, IDs `fta/<provider>/<model>` (e.g. `fta/zai/glm-5.3`); **no card** — free account (email/Discord confirm) + [daily check-in](https://freetheai.org/checkin) unlocks free models until 00:00 UTC; **50 requests/day** on free models (resets 00:00 UTC, failed requests don't count); streaming, tool calling, web search, image/video gen; MIT, GitHub `Free-The-Ai/free-ai` (35★); model list at `freetheai.org/models`
- **AnyAPI** — NEW Oct 2026 gateway (`https://api.anyapi.ai/v1`), 400+ models, OpenAI-compatible, permanent free tier (100K tokens/day free, no credit card); added to freellmapi as provider; key at dash.anyapi.ai
- **Kenari** (https://kenari.id) — 🆕 NEW Oct 2026 OpenAI-compatible free-only pooled gateway (Node/Python/JS SDKs); **22 free models (19 chat + 3 image)** via shared daily allowance (50 req/day, 5 RPM, no top-up); base `https://api.kenari.id/v1`; free chat incl. `qwen3-8-omni-flash:free` (Poolside Qwen, 1M ctx), `agnes-2-5-flash:free` (Agnes, 512k ctx, vision), `nemotron-3-5-super-vl:free` (NVIDIA, 512k ctx), `glm-4-7-flash:free` (Zhipu, 200k ctx), `hy3:free` (Tencent, 196k ctx), `longcat-2-5-preview:free` (Meituan, 1M ctx), `muse-spark-1-3-contributor:free` (Meta, 1.05M ctx), `solar-mini4:free` (Upstage, 512k ctx), `xing4-0-29b-a4b:free`, `ornith-1-5-122b:free`, `nemotron-3-ultra-550b-a55b:free` (1M ctx); free image gen via `agnes-image-2-5-flash:free` + `agnes-image-2-0-flash:free`; Voxtral transcription via FreeLLMAPI adapter (#1703); API key from https://kenari.id; previously only sub-mentioned under FreeLLMAPI. live-verified via /v1/models 2026-10-26.

|- **IteraCompute** — 🆕 NEW Oct 22; OpenAI-compatible (`https://api.iteracompute.com/v1`); **1 model truly free** — `qwen/qwen3.8-27b` (262K ctx, 128K free tier); **30M tok/month** (signup key, no card); 160K TPM; key validation OFF; 120s timeout (queues at peak); ⚠️ `moonshotai/kimi-k3-free` ($0 pricing) requires $10 recharge — excluded from chain; 30 of 32 catalog models paid; key via iteracompute.com/signup
- **onomeo** — NEW Oct 21; OpenAI-compatible gateway (`https://onomeo.com/v1`), Bearer API-key; free models share 30 calls/5h per account (1,500 site-wide shared window); long requests count as 1 call per 50K chars; models delivered via signed catalog (Premium now, Free after 30-day gate); free answers branded "— via onomeo.com" (freellmapi adapter strips this); 403/429 = quota/throttle on valid key, not auth failure; freellmapi adapter validates returned model identity (Oct 24 fix #1694: 502 on mismatch \u2192 failover)
| - **Z AI** (GLM-4.7-Flash, 200K ctx; GLM-4.6V-Flash NEW Oct 23, free vision; GLM-4.5-Flash DEAD Oct 22) — https://api.z.ai/api/paas/v1 intl endpoint
| - **BazaarLink** (bazaarlink.ai) — NEW Oct 21; free no-card API key (`bazaarlink.ai/keys`); OpenAI-compatible `https://api.bazaarlink.ai/v1`; shared free pool: 10 RPM / 60 wu-day (no card) or 20 RPM / 120 wu-day (credit); 20 RPM site cap, 2 concurrent, resets 00:00 UTC; 6 always-free + auto:free router + 9 new ZDR (Zero Dollar Research) free-tier models Oct 25: qwen/qwen3.7-flash, reflection/beam (501B MoE agentic coder), reflection/beam-free, nvidia/nemotron-3.5-lightning-free, stealth/glyph-cluster, deepseek/deepseek-v4-flash-0731free, openai/gpt-6-luna (1050K), anthropic/claude-haiku-5.5 (1000K), openai/gpt-5.6-luna (1050K), google/gemini-3.8-flash (1048K), openai/gpt-6.1-sol (1050K), anthropic/claude-sonnet-5.5 (1000K), anthropic/claude-opus-5.5 (1000K), openai/gpt-6-astra (1050K), x-ai/grok-4.7 (500K); hourly probes Oct 21 ~96-100% success
||- **Hugging Face router** — ❌ $0.10/mo credit REMOVED Oct 7; no free tier without card; base `https://router.huggingface.co/v1`
- ❌ **GitHub Models — RETIRED July 2026.** Don't bother.
- **OpenCode Zen** (opencode.ai/zen/v1) — NEW Oct 2026; free account key (no card), OpenAI-compatible; **11 free `-free` models confirmed** (beam-free, mimo-v2.6-flash-free, jev-1.13-free, longcat-2.5-preview-free, deepseek-v4.1-flash-free, glm-5.3-flash-free, nemotron-3.5-lightning-free, nemotron-3.5-super-vl-free, flint-40b-free, **big-pickle**, **nemotron-3-ultra-free**). ⚠️ promo/limited-time, data may be logged, direct API fingerprint-gated.
|- **FreeLLMAPI** (tashfeenahmed/freellmapi) — 🆕 NEW Oct 2026 v0.16.10 installable free-only LLM gateway (pip/npm/Docker `ghcr.io/tashfeenahmed/freellmapi`, Node.js 24); **34 free LLM providers / 635 endpoints / 474 model families / 7.4B tok/mo** pooled; OpenAI + **Anthropic `/v1/messages`** compat (Claude Code + Anthropic SDKs run against free pool); MCP server at `/mcp`; image/video/speech gen incl. Mistral Voxtral transcription; tool calling + structured outputs; self-updating signed catalog (+26 net catalog routes v0.16.10); STREAM_KEEPALIVE_MS (SSE pings); BUDGET_ALERT_WEBHOOK_URL (80/100% alerts); setup CLI for Claude Code/Codex/Aider/Cline/Roo/Continue/Cursor; custom local provider support (Ollama/vLLM/llama.cpp); IteraCompute adapter; **Keenable** + **Brave Search** ($5/mo free credits); `npx freellmapi` → http://localhost:3001; 34 free providers incl. 11 not tracked individually: SEA-LION, NavyAI, NaraRouter, Aion, Requesty, AI Horde, Routeway, AINative, Keenable, Kenari (BazaarLink + onomeo tracked separately)

||- **FreeRide** (api.free-ride.xyz) — installable free-only LLM gateway; local OpenAI-compatible proxy at `http://localhost:11343/v1`; 290+ providers/90+ free tiers (~1.53B tok/mo pooled, up to ~2.15B first month w/ signup credits); routes OpenRouter/Groq/Gemini/NVIDIA NIM/Cloudflare/HuggingFace/Z.ai/xKiro/Ollama Cloud/Kilo/OpenCode Zen/OVHcloud/BlockRun + 17 more; keyless start via Qoder (unlimited)/Pollinations/Kiro (~50 credits/mo)/Kilo/OVHcloud anonymous (2 RPM)/BlockRun anonymous (30 req/min); OpenAI+Anthropic SDK + CLI + MCP; works with Aider/Continue.dev/Codex/Claude Code; no paid fallback; github Shaivpidadi/FreeRideV3
||- **FreeAI** (free.ai) — OpenAI-compatible API gateway at `https://api.free.ai/v1`; EU-hosted; free tier 30K tok/day + 1000 req/month + 60 RPM, no card required (free applies until payment method linked); 588 models via BYOK; keyless start on some models (9 of 513 verified Oct 2026); api key `sk-free-…` from [free.ai/api](https://free.ai/api/)
|- 🆕 **Inception Labs** — `mercury-3`: 1M-ctx diffusion LLM; free 100M tokens one-time (no card, no payment method); reasoning + tool calling; OpenAI-compatible `https://api.inceptionlabs.ai/v1`; ~1,068 tok/sec; also on OpenRouter / Baseten / Vercel
- 🆕 **Baseten** — Mammoth-1 (27B) + Elephant-1 (9B): free on Vercel AI Gateway thru Oct 27; #1 Jev Decision Index (Mammoth) / tied-#1 Artificial Analysis Decision Index (Elephant); 16K ctx; classify / route / score (tool, not chat); `vercel.com/ai-gateway/models`
- 🆕 **ElectronHub** (api.electronhub.ai) — 21 keyless free models with `:free` suffix; no card, no signup — keyless `curl https://api.electronhub.ai/v1/models` confirmed live; 200 req/day, 5 RPM; OpenAI-compatible `https://api.electronhub.ai/v1`; `ek-` prefix for paid tier; models: gpt-oss-20b:free, gpt-oss-120b:free, gemma-4-26b-a4b-it:free, gemma-4-31b-it:free, deepseek-v3.2:free, glm-5:free, glm-5.1:free, glm-5.2:free, qwen3.6-27b:free, qwen3.8-27b:free, aion-3.0:free, minimax-m2.7:free, nemotron-3.5-lightning:free, glm-4.7:free, glm-4.7-flash:free, +7 more (21 confirmed live Oct 25)
- 🆕 **AMD Radeon Cloud** (developer.amd.com.cn) — 16 free public API models via Token Factory; base `https://developer.amd.com.cn/radeon/api/v1`; `rc-` key from developer.amd.com.cn/radeon/tokenfactory (no card); API endpoint confirmed live (returns login-required JSON without key); models: DeepSeek-V4-Flash (1M ctx), DeepSeek-V4.1-Flash (1M), Qwen3.8-Flash-Next (262K), Qwen3.8-27B (262K), GLM-5.3-Flash (262K), MiMo-V2.6-Flash (1M), Gemma-4-31B-IT (262K), MiniCPM5-2B (131K), MiniCPM-V-4.7-35B-A3B (262K), OmniVoice (TTS), MinerU2.5-Pro (OCR), d3, d3-flash, Clef, +1 more
- 🆕 **SiliconFlow** (siliconflow.cn) — free Qwen3-8B tier; base `https://api.siliconflow.cn/v1`; signup required (no card); OpenAI-compatible; 1000 RPM / 50K TPM
---

## 🏆 Recommended stack (coding/agent use)
1. **OpenRouter `nvidia/nemotron-3-ultra-550b-a55b:free`** — biggest brain, 1M ctx
2. → fallback `openrouter/free` (auto-router over 22 models, survives single-model outages)
3. → fallback **LLMTR `nvidia/nemotron-3-super-120b-a12b`** (1000 req/day, no card; NVIDIA NIM version DEAD Oct 28)
4. → fallback **Groq `openai/gpt-oss-120b`** (1,000 RPD, instant)
5. → fallback **Gemini 3.8 Flash** (limits now console-gated / not published per-model since ~Oct 18)
6. → fallback **APInex `free/deepseek-v4.1-flash`** (10M tokens/day, Google sign-in only; Oct 2026)
7. → fallback **OpenCode Zen `glm-5.3-flash-free`** (free account key; promo, may log data)
8. → emergency no-key: **Kilo Code** (200/hr, works even if all keys die)

**One-time power move:** buy $10 OpenRouter credits once → all free models jump from 50 → 1,000 RPD forever.

## 📰 Recent news (Oct 19–26, 2026)
||- 🆕 **Oct 26**: **Infron AI** (aifree.dev / api.infron.ai) — free OpenAI-compatible gateway; 5 `:free` models confirmed via live `/v1/models` probe (not 6 — `inclusionai/ling-3.1-flash:free` confirmed DEAD, absent from probe); 1,000 req/day per account, $0/token, $5+ balance anti-abuse (never consumed); no credit card required; `qwen/qwen3.8-27b:free` (256K) was DEAD on xKiro Oct 22 — now ALIVE; `deepseek/deepseek-v4.1-flash:free` (1M ctx), `qwen/qwen3.8-27b-abliterated-cyber:free` (256K), `internlm/atria-dawn-preview:free` (256K), `apodex/apodex-1.1-mini:free` (262K, DEAD on OpenRouter Oct 25 — alive on Infron only) (Oct 26)
||- 🆕 **Oct 26**: **AIHubMix** (aihubmix.com / api.aihubmix.com/v1) — free OpenAI-compatible gateway; 45 free models at $0/M (live Oct 25 probe; was claimed 64 Oct 26); 10 trial calls no card (never expire) + ~$100 req/day after $1 top-up; notable new free model IDs: `qwen3.8-max-free` (1M), `qwen3.8-flash-free` (1M), `coding-glm-5.3-free` + `coding-glm-5.3-flash-free` + `coding-glm-5.2-free` + `coding-glm-5-free` (GLM-5.x coding, 1M), `coding-kimi-k3-free` (1.05M), `laguna-s-2.1-free` + `laguna-xs-2.1-free` (1.05M); ☠️ DEAD Oct 25: `gpt-5.5-free`, `gpt-image-2-free`, `wan3.0-video-free`, `wan3.0-video-prime-free` (absent from 45 free-suffix live list); models list aihubmix.com/models/free (Oct 26)
||- 🆕 **Oct 26**: **Token Harbor** (tokenharbor.ai) — unified free LLM aggregator gateway; `:free` suffix models never bill; free rolling 7-day allowance per user; 5 free models at $0/token: claude-haiku-5.5:free (200K ctx, free limited-time Oct 7 campaign), deepseek-v4.1-flash:free (1M), deepseek-v4-flash:free (1M), mimo-v2.6-flash:free (1M), mimo-v2.5:free (1M); OpenAI-compatible base https://tokenharbor.ai/v1; bearer token; signup at tokenharbor.ai (Oct 26)
||- 🆕 **Oct 26**: **InferAll** (api.inferall.ai/v1) — free OpenAI+Anthropic compatible gateway; 10+ open-source NVIDIA NIM models at $0 in/out after $5 one-time starter pack; 50 chat / 100 text per day shared pool; 3 free models: nvidia/nemotron-3-ultra-550b-a55b (1M ctx), z-ai/glm-5.3-flash (1M ctx), openai/gpt-oss-20b (128K ctx); key prefix `ifu_`; 127 models total; signup at api.inferall.ai (Oct 26)
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
- 🆕 BlockRun.ai: verified keyless, no signup, no card; **7 free NVIDIA-hosted models** (live Oct 25 probe; was claimed 9 Oct 26) incl. nemotron-3-ultra-550b (1M ctx) + nano-omni-30b-a3b-reasoning (256K) + llama-3.2-11b-vision (128K) + **nemotron-3.5-lightning** (1M) + **cohere/north-mini-code** (256K) + **poolside/laguna-xs-2.1** (262K) + **muse-glimmer-30b** (1M); ☠️ `gpt-oss-20b` + `nemotron-super-49b` NOT confirmed free on live probe (absent from billing_mode=free list); auto-routes unlisted model names
- 🆕 uncloseai: verified keyless Qwen3.8-27B-exl3 (64K) vllm endpoint live, no signup
- 🆕 LLM Tech (llmtech.eu): shared trial key (no card, no signup), 2M tok/day, qwen3.8-27b; EU-hosted (probe-verified list)
- 🔄 LLMTR (llmtr.com): Turkish keyless gateway, 40 free models Oct 26 across agnes-evren-fastino-greenpt-heabsy-ifm-internlm-liquid-llmtr-minimax-nace-nvidia-openai-perplexity-poolside-qwen-together-typesafe-upstage-voltropy; ☠ motif DEAD (absent probe); ling-3.1-flash DEAD Oct 13
- ☠️ **LLM7.io: both cataloged models PAID** (`gpt-oss:20b` turbo tier, `deepseek-v4-flash-0731` pro tier) — removed from free tracking Oct 21
- 🔄 **SambaNova free tier REACTIVATED** (Oct 21 Gravity + vava-nessa Oct 17): no card required (free applies until payment method linked); 20 RPM / 20 RPD / 200K tok/day per model; DeepSeek-V3.1 / Llama 3.3 70B / gpt-oss-120b (+ DeepSeek-V3.2, Gemma 4 31B preview)
- 🆕 **OVHcloud: 11 free chat models** no key/no signup (EU-hosted): Qwen3.5-397B (262K), Qwen3.8-27B (262K), gpt-oss-20b (131K), gpt-oss-120b (128K), Llama-3.3-70B (128K), Mistral-Small-3.2-24B (128K), Mistral-Nemo (128K), Qwen2.5-VL-72B (128K), Qwen3.5-9B (128K), Qwen3.6-27B (262K), Qwen3Guard variants
- 🆕 **xKiro: 21 free models** (500K tok/day per IP, dashboard API key); top: longcat-2.5-preview:free (262K), qwen/qwen3.7-flash:free (262K), qwen/qwen3.8-27b:free, qwen/qwen3.8-max:free (262K), qwen/qwen3.7-max:free; OpenAI/Anthropic SDK compatible — ⚠️ 5 Oct-21 free models dropped (qwen3.8-27b, stealth/llama-3.1-70b, nemotron-3.5-super-vl, qwen3-32b, qwen2.5-72b)
- 🆕 **NVIDIA NIM: +8 free models Oct 22** (build.nvidia.com Free Endpoint, 40 RPM no daily cap): `nvidia/nemotron-3.5-super-vl-120b-a12b` (vision, Oct 15), `stepfun-ai/step-5-preview` (multimodal reasoning, Oct 14), `meta/llama-4-maverick-17b-128e-instruct` (128-expert MoE), `qwen/qwen3-coder-480b-a35b-instruct` (480B coding MoE), `minimaxai/minimax-m2.7` (230B MoE), `mistralai/mistral-nemotron` (reinstated after Oct 3 rotation), `bytedance/seed-oss-36b-instruct`, `stepfun-ai/step-3.5-flash`; dual-confirmed build.nvidia.com Free Endpoint + ASSERT-KTH/nvidia-free-endpoints programmatic list; added to models.csv + chain.json fallback routing
- 🆕 BazaarLink (bazaarlink.ai): NEW Oct 21 free-aggregator, no card; **7 unique free models Oct 22** — reflection/beam, reflection/beam-free, nvidia/nemotron-3.5-lightning-free, stealth/glyph-cluster, deepseek/deepseek-v4-flash-0731free, qwen/qwen3.7-flash:free (bare qwen/qwen3.7-flash now PRICED — free id uses `:free` suffix), **auto:free** router NEW; 10 RPM/60 wu-day (no card) or 20/120 (credit); OpenAI-compatible https://api.bazaarlink.ai/v1; hourly probes ~96-100% (Oct 21 17:46)
- 🔄 **SambaNova free tier REACTIVATED** (Oct 21 Gravity + vava-nessa Oct 17): was "all paid / card required since Aug 14"; now free tier live, NO card needed (free applies until payment method linked); 20 RPM / 20 RPD / 200K tok/day per model; DeepSeek-V3.1 / Llama 3.3 70B / gpt-oss-120b (+ DeepSeek-V3.2, Gemma 4 31B preview)
- 🔄 **Cerebras reclassified**: was "~30 RPM dev tier, llama-3.3-70b, payment method required"; now $5/30-day trial credit (card required; FAQ "no permanent free tier"); limit ~30 RPM → 5 RPM / 30K tok/min / 1M tok/day per model; free trial models gpt-oss-120b + Qwen3-235B (+Qwen3.8-27B)
- 🆕 **Oct 22**: NVIDIA NIM free catalog adds `moonshotai/kimi-k2.6` (262K ctx), `01-ai/yi-large` (ctx unknown), `openai/gpt-oss-20b` (128K ctx); free pricing verified via `/v1/models` API (no pricing key = free); ⚠️ kimi-k2.6 marked "Unavailable" on free-model.com.
- 🆕 **Oct 23**: NVIDIA NIM adds `nvidia/nemotron-3.5-bolt-e4b` — 4B conversational LLM (8B BF16 params), 64K ctx; Gemma-4-E4B-it post-trained; free dev-program endpoint (phone verify, no card, 40 RPM no daily cap) at build.nvidia.com; "Start building with a free API endpoint" per NVIDIA Technical Report (research.nvidia.com); NOT yet on OpenRouter (only super-vl/lightning/content-safety per Oct 25 live probe) — added to models.csv + nvidianim chain routing.
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

## Fish Audio

**Free tier:** `s2.1-pro-free` TTS model at $0/M UTF-8 bytes (fair-use, no hard cap)
**Endpoint:** `POST https://api.fish.audio/v1/tts`
**Models:** `s2.1-pro-free` — 83 languages, 2 voices, same quality as paid s2.1-pro
**Key:** Free Bearer API key from fish.audio (no card required)
**Limits:** No hard token cap — fair-use only; free access guaranteed through Nov 30 2026
**Notes:** s2.1-pro-free blog at fish.audio/blog/s2-1-pro-free-api (live); s2.2-pro-free blog post returned 404 (removed); confirmed via web search + docs.fish.audio. /v1/speech, /, /v1/models endpoints return 404 — only /v1/tts is live.

## 📰 News — Oct 24-28
- 🆕 **Oct 25 — FHRouter (fhrouter.com):** free no-card OpenAI-compatible gateway (`https://fhrouter.com/v1`); 3 always-free frontier models — `grok-4.6`, `deepseek-v4-flash`, `glm-5.3-flash` — no credit card, no expiring trial, free for everyone (single account key); live HTTP 200 + GitHub repo `fhrouter/fhrouter` verified Oct 25; `/v1/models` requires account key (no keyless); context + rate limits unpublished. Added to chain.json fallback.
- **Qwen3 → Paid on OpenRouter (Oct 24):** Qwen3 8B, Qwen3 235B A22B, Qwen3 VL 8B Thinking, Qwen3 30B A3B Thinking 2507 all moved from free `:free` to paid tier on OpenRouter. Not tracked in this guide as free OpenRouter models (no update needed). Qwen3.8-27B remains the only Qwen3 on free lists (still free on Groq/OVH/Infron, dead on OpenRouter).
- **DeepSeek V4.1-Flash-1017 (Oct 17):** model version update; API alias `deepseek-flash` unchanged. New Search & Fetch APIs at $0.75/1K calls (paid from Oct 31). Model already tracked on NVIDIA NIM + Token Harbor + OpenCode Zen + APINex + UnoRouter.
- **Hermes Desktop on Omarchy:** installable via `omarchy pkg add hermes-desktop` (v2026.9.7-6, MIT). Free UI app (requires paid LLM provider); uses nemotron-3-ultra-550b-a55b backend.
- **ElectronHub (Oct 26):** 21 keyless free models with `:free` suffix (no card, no signup — `curl https://api.electronhub.ai/v1/models` works); 200 req/day, 5 RPM; models include gpt-oss-20b:free, gpt-oss-120b:free, gemma-4-26b-a4b-it:free, gemma-4-31b-it:free, nemotron-3.5-lightning:free, deepseek-v3.2:free, glm-5:free, glm-5.2:free, qwen3.6-27b:free, qwen3.8-27b:free, aion-3.0:free, minimax-m2.7:free, +7 more
- **AMD Radeon Cloud (Oct 26):** 16 free public API models via Token Factory; base `https://developer.amd.com.cn/radeon/api/v1`; `rc-` key from developer.amd.com.cn/radeon/tokenfactory (no card); API endpoint confirmed live (returns login-required JSON without key); models: DeepSeek-V4-Flash (1M), Qwen3.8-27B, GLM-5.3-Flash, MiMo-V2.6-Flash, Gemma-4-31B-IT, MiniCPM-V-4.7-35B-A3B, +10 more
- **SiliconFlow (Oct 26):** free Qwen3-8B tier; base `https://api.siliconflow.cn/v1`; signup required (no card); OpenAI-compatible; 1000 RPM / 50K TPM
- **AIHubMix GPT-5.5-free + GPT-Image-2-free (Oct 26):** newly added to 45-model free pool on `https://api.aihubmix.com/v1`; 10 trial calls no card + ~$100 req/day after $1 top-up; ☠️ `gpt-5.5-free` + `gpt-image-2-free` DEAD Oct 25 (absent from live /v1/models probe)
- ⚠️ **Chutes.ai CORRECTION (Oct 24):** was incorrectly marked DEAD — API confirmed live (HTTP 200) at `llm.chutes.ai/v1` (`api.chutes.ai/v1` returns 404 = wrong endpoint probed); early-access 200 req/day free program ended Feb 2026; now requires $5 one-time top-up (not subscription, no card); some models remain free at $0–$0.30/MTok; status.chutes.ai confirms all systems operational Oct 17, 2026; 14 TEE models
- ☠️ **Oct 25 probe:** OpenRouter `apodex/apodex-1.1-mini:free` — confirmed DEAD, absent from live `/v1/models` API (was verified free Oct 24 via model page, 36.8B prompt tokens). OpenRouter `:free` count now 17 (was 18), total 22 free models. `apinex/apodex-1.1-mini:free` on Kilo Code gateway already dead Oct 21.
- 🆕 **Oct 25 probe:** BazaarLink 9 new ZDR (Zero Dollar Research) free-tier models discovered via `/v1/models` (`zdr=true`): `openai/gpt-6-luna` (1050K), `anthropic/claude-haiku-5.5` (1000K), `openai/gpt-5.6-luna` (1050K), `google/gemini-3.8-flash` (1048K), `openai/gpt-6.1-sol` (1050K), `anthropic/claude-sonnet-5.5` (1000K), `anthropic/claude-opus-5.5` (1000K), `openai/gpt-6-astra` (1050K), `x-ai/grok-4.7` (500K). Requires BAZARONLINK_API_KEY (bazaarlink.ai/keys); free tier 10 RPM/60 wu-day (no card), 20 RPM/120 wu-day (credit). ⚠ keyless quotas are per-IP.
- 🆕 **Oct 25:** Hetzner Inference API (`inference.hetzner.com/api/v1`) — free while experimental, OpenAI-compatible, no credit card (free token from `experiments.hetzner.com`). 2 models per official docs: `Qwen/Qwen3.6-35B-A3B-FP8` (MoE 35B/3B active, 262K, text+image), `Qwen3.8-27B` (dense 27B, 262K, text+image). Hetzner blog: taking a break from large models (Kimi/DeepSeek/GLM rows removed). Rate limits corrected: 4M in / 100k out per 60s, 10 req/60s per key; no daily cap. Hermes plugin: `iamimmanuelraj/hermes-hetzner-provider`.
- 🆕 **Oct 25:** Fish Audio `s2.1-pro-free` TTS model — free at $0/M UTF-8 bytes (fair-use, no hard cap); `POST https://api.fish.audio/v1/tts`; 83 languages, 2 voices, same quality as paid s2.1-pro; free Bearer API key from fish.audio (no card); free access guaranteed through Nov 30 2026
- 🛠️ **Oct 25:** smfworks/hermes-omarchy boot integration — `bin/hermes-omarchy-setup install` (idempotent) sets up Hermes Desktop autostart + Ollama user unit on Omarchy; installable via `omarchy pkg add hermes-omarchy`; MIT
- 🛠️ **Oct 25:** ninepointlabs/omarchy-hermes-chat — Omarchy shell plugin (Quickshell) bar icon + dropdown for quick Hermes agent chat; talks to `hermes` CLI directly (no gateway); `./install.sh`; MIT
- 🆕 **Oct 25 — Nous Portal free tier:** 8 model IDs ending `:free` (poolside/laguna-s-2.1, laguna-xs-2.1, upstage/solar-mini4, meituan/longcat-2.0, stepfun/step-3.7-flash, meituan/longcat-2.5-preview, reflection/beam-1.0-501b-a23b, ornith/ornith-1.5-122b) at the OpenAI-compatible base `https://inference-api.nousresearch.com/v1`; free signup at portal.nousresearch.com (no card); 50 RPM / 500K TPM account-wide free tier. Live `/v1/models` probe confirms `$0` pricing on all 8 (424 total models, 8 `:free`; ctx 256K–1M). 7 IDs not previously tracked — adding to models.csv + chain.json.
- 🆕 **Oct 25 — BeatAPI free text models:** 5 `-free` IDs (glm-5.3-free, glm-5.3-flash-free, deepseek-v4.1-flash-free, deepseek-v4-flash-0731-free, gemini-3.8-flash-free) at the OpenAI-compatible base `https://api.beatapi.io/v1`; default `auto` group, `$0`/token, no card; 1 RPM before first top-up / 10 RPM after. Docs confirm free IDs omit published context/output limits (docs.beatapi.io/free-models).
- 🆕 **Oct 14:** Hermes Agent v0.22.0 "Threshold Release" — Plugin Catalog now lists 600 reviewed plugins; "Providers as plugins" lets you install out-of-tree LLM providers via `hermes plugins install` and select them with `--provider chatgpt` (picks ChatGPT Codex OAuth). Release: github.com/nousresearch/hermes-agent/releases/tag/v0.22.0
- 🆕 **Oct 21:** crueber/omarchy-hermes-desktop-overlay — Omarchy plugin adding a Quake-style pull-down HUD; `SUPER+SHIFT+H` drops a floating Hermes window over 3/4 of the screen (Hyprland special workspace with slide animation); auto-launches Hermes if not running. `omarchy plugin add https://github.com/crueber/omarchy-hermes-desktop-overlay`; MIT
- 🆕 **Oct 21:** PSthelyBlog/omarchy-hermes-companion v0.5.0 — Always-on Hermes agent plugin that watches the screen, speaks up when useful, and answers voice requests ("hey Hermes"). `omarchy plugin add https://github.com/PSthelyBlog/omarchy-hermes-companion.git --enable`; MIT
- 🆕 **Oct 21:** r0b0tlab/omarchy-hermes-usage — Hermes Agent usage monitoring plugin for Omarchy. `omarchy plugin add https://github.com/r0b0tlab/omarchy-hermes-usage.git --enable`; MIT
- 🆕 **Oct 21:** meeting-overlay — Native Hermes desktop plugin for meeting mode; right-docked pane + status-chip + phone-mirror PWA + Hammerspoon menu-bar controller. Docs: hermes-agent.nousresearch.com/docs/plugins/meeting-overlay
