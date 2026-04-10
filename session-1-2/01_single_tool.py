import anthropic
import json
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()  # picks up ANTHROPIC_API_KEY from .env

# ── Step 1: Define a single tool ──────────────────────────
# This is the JSON schema Claude reads to decide WHEN and HOW to use the tool.
# Notice: description tells Claude what it does, when to use it, and what it returns.

calculator_tool = {
    "name": "calculator",
    "description": (
        "Perform basic math operations. Use this when the user asks to "
        "calculate, compute, or do any arithmetic. Supports +, -, *, /, "
        "and ** (exponentiation). Returns the numeric result."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": (
                    "A mathematical expression to evaluate. "
                    "Examples: '2 + 2', '150 * 0.18', '2 ** 10'"
                ),
            }
        },
        "required": ["expression"],
    },
}

# ── Step 2: Send a message that should trigger tool use ───
print("=" * 60)
print("SENDING REQUEST TO CLAUDE...")
print("=" * 60)

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=[calculator_tool],
    messages=[
        {"role": "user", "content": "What is 347 * 829?"}
    ],
)

# ── Step 3: Inspect what Claude returned ──────────────────
# This is the part most tutorials skip. Let's see the RAW response.

print(f"\nStop reason: {response.stop_reason}")
print(f"Number of content blocks: {len(response.content)}")

for i, block in enumerate(response.content):
    print(f"\n--- Block {i} ---")
    print(f"Type: {block.type}")
    if block.type == "text":
        print(f"Text: {block.text}")
    elif block.type == "tool_use":
        print(f"Tool name: {block.name}")
        print(f"Tool ID: {block.id}")
        print(f"Input: {json.dumps(block.input, indent=2)}")

# ── Step 4: Execute the tool ourselves ────────────────────
# Claude didn't calculate anything. It ASKED us to. Now we do it.

if response.stop_reason == "tool_use":
    tool_block = next(b for b in response.content if b.type == "tool_use")

    # Actually run the calculation (with safety constraints)
    try:
        # WARNING: eval() is dangerous in production. We use it here for
        # simplicity. Real agents should use a safe math parser.
        result = eval(tool_block.input["expression"])
        tool_result = str(result)
        is_error = False
    except Exception as e:
        tool_result = f"Error: {str(e)}"
        is_error = True

    print(f"\n{'=' * 60}")
    print(f"TOOL EXECUTED: {tool_block.input['expression']} = {tool_result}")
    print(f"{'=' * 60}")

    # ── Step 5: Send the result back to Claude ────────────
    # We append Claude's response AND our tool result, then call again.

    followup = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        tools=[calculator_tool],
        messages=[
            {"role": "user", "content": "What is 347 * 829?"},
            {"role": "assistant", "content": response.content},
            {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_block.id,
                        "content": tool_result,
                        "is_error": is_error,
                    }
                ],
            },
        ],
    )

    print(f"\nClaude's final response: {followup.content[0].text}")
