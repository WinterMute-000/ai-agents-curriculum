# Block 1 — Tools, the right way (35 min)

## 1. By hand (10 min)
Fill in the TODOs in [by_hand.py](./by_hand.py) yourself, then run it. Answer the three questions at the bottom of the file.

## 2. Build (20 min) — prompt for Claude Code

Paste this into Claude Code from the repo root:

> Read CURRICULUM.md (Block 1) and capstone/digest/config.py. Create `capstone/digest/tools.py` and `capstone/digest/agent.py`:
> - `get_topics()` tool: returns the topics and settings from topics.toml
> - `save_item(topic, title, url, summary, published)` tool: appends a finding to `capstone/data/items.jsonl`; strict schema
> - Anthropic's server-side `web_search` and `web_fetch` tools (current versions)
> - `agent.py`: runs the Tool Runner with these tools and a minimal system prompt, handles `pause_turn`, prints each tool call as it happens, and prints the final text. Runnable as `python -m capstone.digest.agent`.
> Keep it small — no memory, caching, or multi-agent yet (later blocks). Explain each design choice briefly as you go.

Then **read every file it wrote** before running it.

## 3. Break it (5 min)
- Change the `save_item` docstring to just `"Saves."`. Run again. Does Claude still save items, and with sensible fields?
- Restore it.

## Checkpoint
- When do you write the loop yourself vs use the Tool Runner?
- What runs on Anthropic's servers vs on your machine?
- Why must all parallel tool results go back in a single message?
