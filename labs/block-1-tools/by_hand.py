"""Block 1, by hand: the Tool Runner.

In session-1-2 you wrote the agentic loop yourself (~60 lines). Here the SDK
runs the loop; you only write the tool. Fill in the TODOs, then run from the
repo root:

    python labs/block-1-tools/by_hand.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # so `capstone` imports work

from anthropic import beta_tool

from capstone.digest.config import MAIN_MODEL, client


# TODO 1: Turn this into a tool with the @beta_tool decorator.
#   - The SDK builds the JSON schema from the type hints and the docstring.
#   - Write the docstring the way you wrote `description` in session-1-2:
#     what it does, when to use it, what it returns. Document the argument
#     in an "Args:" section.
def word_count(text: str) -> str:
    return str(len(text.split()))


# TODO 2: Create a runner with client.beta.messages.tool_runner(...)
#   - model=MAIN_MODEL, max_tokens=16000
#   - tools=[word_count]
#   - messages=[{"role": "user", "content": "How many words are in 'the quick brown fox jumps'? And in 'hello world'?"}]
runner = None


# TODO 3: Iterate the runner. Each item is one API response (a BetaMessage).
#   For each one, print:
#     - message.stop_reason
#     - for each block in message.content: block.type, and the name/input for
#       "tool_use" blocks or the text for "text" blocks
#
# Questions to answer from the output:
#   a) How many API calls did the runner make? Where in session-1-2 did each one happen?
#   b) Did Claude ask for both word counts in ONE response (parallel tool calls)?
#   c) What did you NOT have to write that 02_multi_tool_agent.py needed?
