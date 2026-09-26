# Curriculum — 4 Hours, One Agent, Shipped

**Goal:** understand every core agent concept by building one real system: a **research digest agent** that researches your topics every morning, remembers what it already told you, and runs by itself on GCP.

**Tools:** Claude Code (building), Claude Desktop (using your agent over MCP), GCP (deploying).

## How each block works

1. **By hand (~10 min):** write the core idea yourself in `labs/`. Small, ugly, yours.
2. **Build (~rest):** drive Claude Code to add the feature to `capstone/`. Read every diff; change things; break things on purpose.
3. **Checkpoint:** answer the block's questions out loud (or in `NOTES.md`). If you can't, re-read the diff before moving on.

## What you're building

```
                ┌──────────────── Cloud Scheduler (daily) ───────────────┐
                ▼                                                         │
 topics.toml ─► Orchestrator (Opus 5) ──delegate──► Researchers (Haiku 4.5, parallel)
                │      │                               │ web_search / web_fetch
                │      └── memory tool ◄── what's already been reported
                ▼
             digest.md ──► delivered (GCS / email)

 Claude Desktop ──MCP──► same tools, interactively
```

---

## Day 1 — Build the agent (2h)

### Setup (10 min)
- [ ] Rotate your API key in the Anthropic Console and put the new one in `.env`
- [ ] Web search enabled for your org in Console settings
- [ ] `pip install -r requirements.txt` · `python -m capstone.digest.config` prints OK

### Block 1 — Tools, the right way (35 min)
- **By hand:** `labs/block-1-tools/` — one `@beta_tool` + the Tool Runner. Compare to your 1.2 manual loop.
- **Build:** capstone tools: `get_topics`, `save_item`, plus server tools `web_search` / `web_fetch`. Strict schemas.
- **Break it:** make a tool description vague. Watch tool choice degrade. Restore it.
- **Checkpoint:** When do you write the loop yourself vs use the Tool Runner? What runs on Anthropic's servers vs yours? Why must parallel tool results go back in *one* message?

### Block 2 — Prompting & thinking (25 min)
- **By hand:** the same research question at effort `low` vs `high` — diff quality, output tokens, latency.
- **Build:** the digest system prompt (audience, format, what "new" means); prompt caching on the stable prefix.
- **Case study:** why did 1.2's `lookup_fact` return India for "speed of light in vacuum"?
- **Checkpoint:** What does effort actually trade? Name three things that silently break caching. How do you prove a cache hit?

### Block 3 — Memory & state (30 min)
- **By hand:** conversation state is just a list you resend — prove it by editing history.
- **Build:** the memory tool, backed by `capstone/data/memory/` — reported URLs + your feedback. Context editing for long runs.
- **Test:** run twice; the second digest must contain no repeats.
- **Checkpoint:** Conversation state vs memory tool vs compaction vs context editing — when each?

### Block 4 — MCP (20 min)
- **By hand:** a 10-line MCP server with one tool.
- **Build:** expose the digest tools as an MCP server; connect it to **Claude Desktop** and Claude Code. Ask Desktop "what did my digest cover this week?"
- **Checkpoint:** What does MCP standardize, and what doesn't it? Local stdio server vs remote server?

**✅ End of Day 1:** a working single agent, runnable from the terminal and usable from Claude Desktop.

---

## Day 2 — Scale it and ship it (2h)

### Block 5 — Multi-agent (35 min)
- **By hand:** a `delegate(task)` tool whose implementation is another Claude call.
- **Build:** orchestrator + one Haiku researcher per topic, running in parallel; orchestrator synthesizes. Measure cost & quality vs the single agent.
- **Compare (10 min):** rebuild one researcher with the **Claude Agent SDK**.
- **Checkpoint:** When is multi-agent worth it? Manual loop vs Tool Runner vs Agent SDK vs Managed Agents — who owns the loop, who owns the infra?

### Block 6 — Evals (25 min)
- **Build:** ~10 cases (topics + expected properties) and a Claude-as-judge grader with a rubric.
- **Experiment:** change one prompt; did the score move beyond noise?
- **Checkpoint:** How do you know a change helped? What makes a grader trustworthy?

### Block 7 — Ship it on GCP (45 min)
- **Build:** Cloud Run **job** (built from source — no Docker needed), triggered daily by Cloud Scheduler. API key in Secret Manager; memory in a GCS bucket; digest delivered.
- **Harden:** iteration caps, task budget, retries on 429/5xx, refusal handling + fallbacks, structured logs to Cloud Logging, cost per run.
- **Stretch:** compare with Anthropic **Managed Agents** scheduled deployments.
- **Checkpoint:** Self-hosted loop vs managed platform — what do you give up? What fails in production that never failed locally?

### Block 8 — Wrap (15 min)
- Cost per run, README, what you'd change next.

---

## Reference

| Concept | Where you touch it |
|---|---|
| Tool definitions, strict schemas, parallel calls | Block 1 |
| Server tools (web search/fetch) | Block 1 |
| System prompts, effort, adaptive thinking, caching | Block 2 |
| Memory tool, context editing, compaction | Block 3 |
| MCP servers & clients | Block 4 |
| Orchestrator/worker, model tiering, Agent SDK | Block 5 |
| Evals, LLM-as-judge | Block 6 |
| Deployment, secrets, scheduling, guardrails, refusals | Block 7 |

Earlier work: `session-1-2/` — manual tool-use loop from scratch (the foundation everything above automates).
