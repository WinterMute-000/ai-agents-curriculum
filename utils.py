"""Shared utilities for curriculum exercises."""

from pathlib import Path
from dotenv import load_dotenv

# Load .env from repo root, overriding any stale system env vars
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env", override=True)
