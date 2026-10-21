# Free LLM API Guide — updated 2026-10-21

Every provider below is OpenAI-SDK-compatible. Point any tool at `base_url` + key and go.
Full model table: `models.csv` (same folder). Auto-maintained by the `freellm-watch` cron agent.

---

## ⭐ OpenRouter — the one key to rule them all
- **Get key:** https://openrouter.ai/keys (Google login, 30 sec)
- **Limits:** 20 RPM, **50 req/day per free model** → jumps to **1,000/day** after a one-time $10 credit buy
- **base_url:** `https://openrouter.ai/api/v1`
- **Best free models:** `nvidia/nemotron-3-ultra-550b-a55b:free` (1M ctx), `nvidia/nemotron-3-super-120b-a12b:free`, `nvidia/nemotron-3.5-lightning:free`, `poolside/laguna-s-2.1:free` (code), `google/gemma-4-31b-it:free`, `thinkingmachines/inkling:free` (reasoning), `google/lyria-3-pro-preview` (audio, $0)
- **Trick:** model = `openrouter/free` auto-routes across all 20 free models. Or pass a `models: [...]` array for built-in fallback.

## 🚪 No-key options (zero signup)
| Provider | base_url | Limit | Catch |
|---|---|---|---|
| **Kilo Code** | `https://api.kilo.ai/api/gateway` | 200 req/hr per IP | Logs prompts; has nemotron-ultra 1M free |
| **OVHcloud** | `https://oai.endpoints.kepler.ai.cloud.ovh.net/v1` | 2 RPM per IP/model | EU-hosted, slow trickle |
|| **LLM7.io** | `https://api.llm7.io/v1` | 60 RPM / 100K tok per 24h | ⚠️ limits CUT Oct 7 (was 1M tok) |
|| **SambaNova** | `https://api.sambanova.ai/v1` | 20 RPM / 20 RPD / 200K tok-day | New find Oct 21; standing free tier |
|| **BlockRun.ai** | `https://blockrun.ai/api/v1` | 429 per IP; keyless | Verified Oct 21; 7 NVIDIA-hosted OS free models: nemotron-3-ultra-550b (1M), nano-omni-30b-a3b-reasoning (256K), llama-3.2-11b-vision (128K) |
|| **uncloseai** | `https://hermes.ai.unturf.com/v1` | 429 per IP; keyless | Verified Oct 21; single Qwen3.8-27B-exl3 (64K) vllm endpoint |
|| **LLM Tech** | `https://api.llmtech.eu/v1` | 2M tok/day; shared trial key | EU; no signup, no card; qwen3.8-27b (probe-verified) |
|| **LLMTR** | `https://llmtr.com/v1` | Free on zero balance | Turkish gateway; agnes-3.0-flash/motif/minimax free; ling-3.1-flash free only until Oct 22 |

## 🧠 Google AI Studio (Gemini)
- **Get key:** https://aistudio.google.com/app/apikey
- **Limits:** Flash: ~15 RPM / 1,500 RPD. Pro: 5 RPM / 50 RPD. All 1M context.
- **base_url:** `https://generativelanguage.googleapis.com/v1beta`
- **Best:** `gemini-3.8-flash` (new), `gemini-2.5-pro` (best free reasoning)
- **Catch:** prompts may be used for training (not in EU/UK/CH).

## ⚡ Groq — fastest inference alive
- **Get key:** https://console.groq.com/keys
- **Limits:** 30 RPM / **1,000 RPD**
- **base_url:** `https://api.groq.com/openai/v1`
- **Best:** `openai/gpt-oss-120b`, `qwen/qwen3.8-27b`

## 🟠 Mistral
- **Get key:** https://console.mistral.ai/api-keys (free mode on by default)
- **Limits:** ~1 RPS, **$10/month free credits**
- **base_url:** `https://api.mistral.ai/v1`
- **Best:** `mistral-large-3`, `codestral` (code), `mistral-small-4` (vision)
- **Catch:** trains on your prompts unless you opt out.

## 🟢 NVIDIA NIM — highest free daily volume
- **Get key:** https://build.nvidia.com (free dev program: sign up, verify phone, no card needed)
- **Limits:** 40 RPM, **no daily cap** per model; 83 models online (free dev program)
- **base_url:** `https://integrate.api.nvidia.com/v1`
- **Best:** `nvidia/nemotron-3-ultra-550b-a55b` (1M ctx), `deepseek-ai/deepseek-v4.1-flash` (NEW Oct 17; 552B MoE, 1M ctx), `z-ai/glm-5.3-flash` (NEW Oct 21; first natively multimodal GLM-5, 320B params, 1M ctx)
- ⚠️ Oct 3: they killed nemotron-3-nano, llama-3.3-70b, gpt-oss-120b… free list rotates — check build.nvidia.com/models.

## Others worth a key (details in models.csv)
- **Cerebras** https://cerebras.ai — needs payment method on file now
- **Cohere** — 1,000 calls/month, non-commercial only
- **Cloudflare Workers AI** — 10K neurons/day, 60+ models
- **Ollama Cloud** — session (5h) + weekly caps, `https://ollama.com/v1`
- **APInex** (apinex.bond) — NEW Oct 2026 gateway; ~18 `:free` models at $0, ~10M tokens/day shared allowance, Google sign-in + daily sign-in; OpenAI-compatible base `https://api.apinex.bond/v1`
- **Z AI** (GLM-4.7-Flash, 200K ctx) — https://api.z.ai/api/paas/v1 intl endpoint
- **Hugging Face router** — $0.10/mo credit: `https://router.huggingface.co/v1`
- ❌ **GitHub Models — RETIRED July 2026.** Don't bother.
- **OpenCode Zen** (opencode.ai/zen/v1) — NEW Oct 2026; free account key (no card), OpenAI-compatible; 9 free `-free` models confirmed (beam-free, mimo-v2.6-flash-free, jev-1.13-free, longcat-2.5-preview-free, deepseek-v4.1-flash-free, glm-5.3-flash-free, minimax-m3.1-flash-free, nemotron-3.5-lightning-free, nemotron-3.5-super-vl-free). ⚠️ promo/limited-time, data may be logged, direct API fingerprint-gated.

---

## 🏆 Recommended stack (coding/agent use)
1. **OpenRouter `nvidia/nemotron-3-ultra-550b-a55b:free`** — biggest brain, 1M ctx
2. → fallback `openrouter/free` (auto-router over 20 models, survives single-model outages)
3. → fallback **NVIDIA NIM `nvidia/nemotron-3-super-120b-a12b`** (40 RPM, no daily cap)
4. → fallback **Groq `openai/gpt-oss-120b`** (1,000 RPD, instant)
5. → fallback **Gemini 3.8 Flash** (1,500 RPD, huge quota)
6. → fallback **APInex `free/deepseek-v4.1-flash`** (10M tokens/day, Google sign-in only; Oct 2026)
7. → fallback **OpenCode Zen `glm-5.3-flash-free`** (free account key; promo, may log data)
8. → emergency no-key: **Kilo Code** (200/hr, works even if all keys die)

**One-time power move:** buy $10 OpenRouter credits once → all free models jump from 50 → 1,000 RPD forever.

## 📰 Recent news (Oct 19–21, 2026)
- 🔄 OpenRouter free pool now **20 models** (17 `:free` + 3 `$0` non-`:free` — lyria-3-pro-clip-preview, lyria-3-pro-preview, openrouter/free): gemma-4-26b-a4b-it:free, gemma-4-31b-it:free, inkling:free + inkling-small:free, laguna-xs-2.1:free, lfm-2.5-2.6b:free, nemotron-3-nano-omni-30b-a3b-reasoning:free, content-safety:free, dots-3-note-preview:free, lyria-3 audio (clip+pro, $0) (Oct 20)
- ☠️ OpenRouter: `inclusionai/ling-3.0-flash-fin:free` + `ling-3.0-flash-sante:free` DEAD — not found on OpenRouter API or Kilo gateway (Oct 21)
- 🆕 Kilo Code: `reflection/beam-free` (1M ctx) + `stealth/glyph-cluster` (256K ctx) now free, no key needed (Oct 21)
- ☠️ Kilo Code: `stepfun/step-3.7-flash:free`, `tencent/hy3:free`, `apinex/apodex-1.1-mini:free` DEAD — 404 or priced on Kilo gateway
- 🆕 OpenCode Zen: 7 new `-free` models (beam-free, mimo-v2.6-flash-free, jev-1.13-free, longcat-2.5-preview-free, deepseek-v4.1-flash-free, glm-5.3-flash-free, minimax-m3.1-flash-free); `big-pickle` + `nemotron-3-ultra-free` removed from free tier
- 🔄 NVIDIA NIM model count: 83 models (was 77); `deepseek-ai/deepseek-v4.1-flash` + `z-ai/glm-5.3-flash` confirmed in catalog
- 🆕 Google lyria-3 clip+pro audio models now free on OpenRouter (pricing $0, no `:free` suffix)
- 🆕 NVIDIA NIM: `deepseek-ai/deepseek-v4.1-flash` (552B MoE, 1M) added to free catalog Oct 17; 40 RPM / no daily cap
- 🆕 APInex (apinex.bond) gateway: ~18 free/free models, ~10M tokens/day allowance, Google sign-in only (no card)
- ☠️ qwen3.8-27b:free left OpenRouter Oct 20 (still free on Groq + OVH, NOT Kilo — priced on gateway)
- 🆕 Z.ai GLM-5.3-Flash (320B params, 18B active, natively multimodal) now free on NVIDIA NIM Oct 2026
- 🆕 NVIDIA NIM: `z-ai/glm-5.3` (non-flash, 753B text MoE, 1M ctx, FP8) free endpoint — dual-confirmed build.nvidia.com free_endpoint + freellm.net Verified
- 🆕 NVIDIA NIM: `diffusiongemma-26b-a4b-it` (26B diffusion text-gen, parallel token gen) + `paligemma` (vision-language) now on build.nvidia.com free_endpoint filter
- 🔄 NVIDIA NIM: `deepseek-ai/deepseek-v4.1-flash` (552B MoE, 1M) added Oct 17; 40 RPM / no daily cap
- 🆕 Google lyria-3 clip+pro audio models free on OpenRouter ($0 pricing, no `:free` suffix)
- 🔧 Ollama Cloud: no new free cloud tier (Oct probe); freellmapi = 34 providers / 635 endpoints, auto-failover
- 🆕 BlockRun.ai: verified keyless, no signup, no card; 7 free NVIDIA-hosted models incl. nemotron-3-ultra-550b (1M ctx) + nano-omni-30b-a3b-reasoning (256K) + llama-3.2-11b-vision (128K); auto-routes unlisted model names
- 🆕 uncloseai: verified keyless Qwen3.8-27B-exl3 (64K) vllm endpoint live, no signup
- 🆕 LLM Tech (llmtech.eu): shared trial key (no card, no signup), 2M tok/day, qwen3.8-27b; EU-hosted (probe-verified list)
- 🆕 LLMTR (llmtr.com): Turkish keyless gateway, agnes-3.0-flash / motif / minimax free on zero balance; ⚠ ling-3.1-flash free only until Oct 22
- ℹ️ Google stopped allowing ZDR (zero-data-retention) for Gemini routing via OpenRouter (Oct 18) — retention change affecting all OR+Gemini traffic, incl. free
- 🔧 freellmapi v0.16.6 (Oct 20): adds ZCode provider + new /v1/usage endpoint
- 🆕 Google Antigravity: agent-first IDE/CLI with $0 Individual plan serving Gemini + claude-opus/s + gpt-oss-120b
