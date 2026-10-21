# Free LLM API Guide — updated 2026-10-21

Every provider below is OpenAI-SDK-compatible. Point any tool at `base_url` + key and go.
Full model table: `models.csv` (same folder). Auto-maintained by the `freellm-watch` cron agent.

---

## ⭐ OpenRouter — the one key to rule them all
- **Get key:** https://openrouter.ai/keys (Google login, 30 sec)
- **Limits:** 20 RPM, **50 req/day per free model** → jumps to **1,000/day** after a one-time $10 credit buy
- **base_url:** `https://openrouter.ai/api/v1`
- **Best free models:** `nvidia/nemotron-3-ultra-550b-a55b:free` (1M ctx), `nvidia/nemotron-3-super-120b-a12b:free`, `nvidia/nemotron-3.5-lightning:free`, `poolside/laguna-s-2.1:free` (code)
- **Trick:** model = `openrouter/free` auto-routes across all 20 free models. Or pass a `models: [...]` array for built-in fallback.

## 🚪 No-key options (zero signup)
| Provider | base_url | Limit | Catch |
|---|---|---|---|
| **Kilo Code** | `https://api.kilo.ai/api/gateway` | 200 req/hr per IP | Logs prompts; has nemotron-ultra 1M free |
| **OVHcloud** | `https://oai.endpoints.kepler.ai.cloud.ovh.net/v1` | 2 RPM per IP/model | EU-hosted, slow trickle |
| **LLM7.io** | `https://api.llm7.io/v1` | 60 RPM / 250 req-hr | Catalog rotates; `turbo` tier only |

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
- **Get key:** https://build.nvidia.com (free dev program)
- **Limits:** 40 RPM / **10,000 RPD** per model, 100+ models
- **base_url:** `https://integrate.api.nvidia.com/v1`
- **Best:** `nvidia/nemotron-3-ultra-550b-a55b` (1M ctx), `nvidia/nemotron-3-super-120b-a12b`
- ⚠️ Oct 3: they killed 5 models (nemotron-3-nano, llama-3.3-70b, gpt-oss-120b…). List rotates.

## Others worth a key (details in models.csv)
- **Cerebras** https://cerebras.ai — needs payment method on file now
- **Cohere** — 1,000 calls/month, non-commercial only
- **Cloudflare Workers AI** — 10K neurons/day, 60+ models
- **Ollama Cloud** — session (5h) + weekly caps, `https://ollama.com/v1`
- **Z AI** (GLM-4.7-Flash, 200K ctx) — https://api.z.ai/api/paas/v1 intl endpoint
- **Hugging Face router** — $0.10/mo credit: `https://router.huggingface.co/v1`
- ❌ **GitHub Models — RETIRED July 2026.** Don't bother.

---

## 🏆 Recommended stack (coding/agent use)
1. **OpenRouter `nvidia/nemotron-3-ultra-550b-a55b:free`** — biggest brain, 1M ctx
2. → fallback `openrouter/free` (auto-router, survives single-model outages)
3. → fallback **Groq `openai/gpt-oss-120b`** (1,000 RPD, instant)
4. → fallback **Gemini 3.8 Flash** (1,500 RPD, huge quota)
5. → emergency no-key: **Kilo Code** (200/hr, works even if all keys die)

**One-time power move:** buy $10 OpenRouter credits once → all free models jump from 50 → 1,000 RPD forever.

## 📰 Recent news (week of Oct 14–21, 2026)
- 🆕 OpenRouter free pool grew 17 → **20 models**: `minimax-m3.1-flash:free` (Oct 19), `xing4.0-29b-a4b:free` (Oct 16), `nemotron-3.5-super-vl:free` (Oct 15, vision)
- 🆕 Google launched **Gemini 3.8 Flash** on free tier (1M ctx / 65K out)
- ☠️ NVIDIA NIM retired 5 models Oct 3 (see above) — free catalogs churn fast; a June free list is already 100% stale
- 📉 DeepSeek V4 Flash input prices spiked on paid tiers — free routes unaffected
- 🔧 **freellmapi** repo: 34 providers / 635 free endpoints behind one `/v1` gateway with auto-failover + encrypted keys — worth self-hosting if we outgrow manual chains
