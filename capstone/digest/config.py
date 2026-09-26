"""Shared configuration: env loading, model choices, paths, and the API client.

Run `python -m capstone.digest.config` from the repo root as a sanity check.
"""

import sys
import tomllib
from pathlib import Path

import anthropic
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[2]
CAPSTONE_DIR = REPO_ROOT / "capstone"
DATA_DIR = CAPSTONE_DIR / "data"          # gitignored: memory store, generated digests
TOPICS_FILE = CAPSTONE_DIR / "topics.toml"

# override=True so a stale system-level ANTHROPIC_API_KEY can't shadow .env
load_dotenv(REPO_ROOT / ".env", override=True)

# Windows consoles default to cp1252; force UTF-8 so model output prints cleanly
sys.stdout.reconfigure(encoding="utf-8")

MAIN_MODEL = "claude-opus-5"        # orchestrator / single agent
WORKER_MODEL = "claude-haiku-4-5"   # parallel researchers (Block 5)

# Opus 5 can decline a request (stop_reason "refusal"). With these params the API
# re-runs a declined request on a fallback model inside the same call.
# Spread into beta calls: client.beta.messages.tool_runner(..., **REFUSAL_FALLBACK)
REFUSAL_FALLBACK = {"betas": ["server-side-fallback-2026-07-01"], "fallbacks": "default"}

client = anthropic.Anthropic()


def load_topics() -> dict:
    with open(TOPICS_FILE, "rb") as f:
        return tomllib.load(f)


if __name__ == "__main__":
    topics = load_topics()
    print(f"anthropic SDK {anthropic.__version__}")
    print(f"main={MAIN_MODEL} worker={WORKER_MODEL}")
    print(f"topics: {', '.join(t['name'] for t in topics['topics'])}")
    reply = client.messages.create(
        model=WORKER_MODEL,
        max_tokens=64,
        messages=[{"role": "user", "content": "Reply with just: OK"}],
    )
    print(f"API check: {reply.content[0].text}")
