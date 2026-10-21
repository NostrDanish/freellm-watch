# freellm-watch

Self-maintaining free-LLM tracker. A Hermes agent (`freellm-scout` profile) re-checks
tashfeenahmed/freellmapi + mnfst/awesome-free-llm-apis every 6h and AI news daily,
then keeps these files current:

- `GUIDE.md` — how to actually use every free LLM API (keys, limits, base URLs)
- `models.csv` — every free model: provider, context, daily limits, how to get a key
- `chain.json` — ordered fallback chain when a free model dies
- `monitor.sh` — git-pulls the watched repos, restarts the local freellmapi gateway on change

No keys, no secrets. Updated by cron, pushed by hand.
