# AI Agents Curriculum — Zero to Expert

Hands-on code exercises from a structured deep dive into AI agents, agentic architectures, and production deployment patterns.

The curriculum builds one real system end to end: a **research digest agent** that researches chosen topics daily, remembers what it has already reported, and runs on GCP. See [CURRICULUM.md](./CURRICULUM.md) for the full plan.

## Layout

| Path | What's there |
|------|--------------|
| [CURRICULUM.md](./CURRICULUM.md) | The 4-hour plan: 8 blocks, checkpoints |
| [labs/](./labs/) | Small by-hand exercises, one folder per block |
| [capstone/](./capstone/) | The digest agent — grows with every block |
| [session-1-2/](./session-1-2/) | Earlier work: tool use & a manual agentic loop |

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # then fill in your API key
python -m capstone.digest.config   # sanity check
```
