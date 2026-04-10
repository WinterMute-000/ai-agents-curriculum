import anthropic
import json
import math
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

# ╔══════════════════════════════════════════════════════════╗
# ║  TOOL DEFINITIONS                                        ║
# ║  These are the "hands" our agent can use.                ║
# ║  Notice: each description tells Claude WHAT, WHEN, and   ║
# ║  WHAT TO EXPECT BACK.                                    ║
# ╚══════════════════════════════════════════════════════════╝

tools = [
    {
        "name": "calculator",
        "description": (
            "Perform mathematical calculations. Use when the user needs "
            "arithmetic, percentages, unit conversions, or any numeric "
            "computation. Supports standard math operations and common "
            "functions like sqrt, pow, log. Returns the numeric result."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": (
                        "A Python math expression to evaluate. Can use math "
                        "module functions. Examples: '150 * 0.18', "
                        "'math.sqrt(144)', 'math.log(1000, 10)'"
                    ),
                }
            },
            "required": ["expression"],
        },
    },
    {
        "name": "lookup_fact",
        "description": (
            "Look up factual information from a knowledge base. Use when "
            "the user asks about specific facts, statistics, company data, "
            "or reference information that requires looking up rather than "
            "computing. Returns the relevant fact or 'not found' if the "
            "information isn't available."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": (
                        "The factual question or topic to look up. Be specific. "
                        "Example: 'population of India 2024', 'Anthropic founding year'"
                    ),
                }
            },
            "required": ["query"],
        },
    },
    {
        "name": "save_note",
        "description": (
            "Save a note or finding for later reference. Use when the user "
            "asks to remember, save, or record information, OR when you've "
            "computed/looked up a result that the user will likely need "
            "later. Returns confirmation with timestamp."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Short descriptive title for the note",
                },
                "content": {
                    "type": "string",
                    "description": "The content to save — facts, calculations, findings",
                },
            },
            "required": ["title", "content"],
        },
    },
]

# ╔══════════════════════════════════════════════════════════╗
# ║  TOOL EXECUTION                                          ║
# ║  This is YOUR code. Claude asks; you execute.            ║
# ╚══════════════════════════════════════════════════════════╝

# Simple in-memory storage for notes
notes = []

# Simulated knowledge base (in production, this would be a DB or API)
KNOWLEDGE_BASE = {
    "population of india": "India's population is approximately 1.44 billion as of 2024.",
    "anthropic founding year": "Anthropic was founded in 2021 by Dario and Daniela Amodei.",
    "speed of light": "The speed of light is approximately 299,792,458 meters per second.",
    "largest ocean": "The Pacific Ocean is the largest ocean, covering about 165.25 million sq km.",
    "claude model": "Claude is a family of AI models built by Anthropic.",
}


def execute_tool(tool_name: str, tool_input: dict) -> dict:
    """
    Execute a tool and return the result.
    Returns dict with 'content' and 'is_error' keys.

    This function is the bridge between Claude's decisions and
    the real world. In production, these would be API calls,
    database queries, etc.
    """
    try:
        if tool_name == "calculator":
            # Allow math module functions in expressions
            allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("_")}
            result = eval(tool_input["expression"], {"__builtins__": {}, "math": math}, allowed_names)
            return {"content": f"Result: {result}", "is_error": False}

        elif tool_name == "lookup_fact":
            query = tool_input["query"].lower()
            # Search knowledge base (fuzzy match)
            for key, value in KNOWLEDGE_BASE.items():
                if key in query or any(word in query for word in key.split()):
                    return {"content": value, "is_error": False}
            return {
                "content": f"No information found for: '{tool_input['query']}'. Try rephrasing.",
                "is_error": False,  # Not an error — just no results
            }

        elif tool_name == "save_note":
            note = {
                "title": tool_input["title"],
                "content": tool_input["content"],
                "saved_at": datetime.now().isoformat(),
            }
            notes.append(note)
            return {
                "content": f"Note saved: '{note['title']}' at {note['saved_at']}",
                "is_error": False,
            }

        else:
            return {"content": f"Unknown tool: {tool_name}", "is_error": True}

    except Exception as e:
        return {"content": f"Tool execution error: {str(e)}", "is_error": True}


# ╔══════════════════════════════════════════════════════════╗
# ║  THE AGENTIC LOOP                                        ║
# ║  This is the heart of every agent. The while loop that    ║
# ║  keeps the Observe → Think → Act cycle running.           ║
# ╚══════════════════════════════════════════════════════════╝

def run_agent(user_message: str, max_iterations: int = 10) -> str:
    """
    Run the agent loop.

    This is the 'harness' — the code that sits between the user
    and Claude, managing the conversation and executing tools.
    """
    print(f"\n{'═' * 60}")
    print(f"  USER: {user_message}")
    print(f"{'═' * 60}")

    messages = [{"role": "user", "content": user_message}]
    iteration = 0

    while iteration < max_iterations:
        iteration += 1
        print(f"\n── Iteration {iteration} ──")

        # ── THINK: Claude processes everything and decides ──
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            tools=tools,
            system=(
                "You are a helpful research assistant with access to a "
                "calculator, a fact lookup tool, and a note-saving tool. "
                "Use tools when they would help answer the user's question. "
                "Think step by step. When you've fully answered the question, "
                "respond directly to the user."
            ),
            messages=messages,
        )

        print(f"   Stop reason: {response.stop_reason}")

        # ── CHECK: Is Claude done? ──
        if response.stop_reason == "end_turn":
            # Claude has produced a final answer
            final_text = ""
            for block in response.content:
                if hasattr(block, "text"):
                    final_text += block.text
            print(f"\n{'═' * 60}")
            print(f"  AGENT: {final_text}")
            print(f"{'═' * 60}")
            return final_text

        # ── ACT: Claude wants to use tools ──
        if response.stop_reason == "tool_use":
            # Add Claude's response (with tool_use blocks) to conversation
            messages.append({"role": "assistant", "content": response.content})

            # Process each tool call
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"   🔧 Tool call: {block.name}({json.dumps(block.input)})")

                    # ── OBSERVE: Execute tool and get result ──
                    result = execute_tool(block.name, block.input)
                    print(f"   📋 Result: {result['content']}")

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result["content"],
                        "is_error": result["is_error"],
                    })

            # Send all tool results back to Claude
            messages.append({"role": "user", "content": tool_results})

    # Safety net: max iterations reached
    print(f"\n⚠️  Max iterations ({max_iterations}) reached!")
    return "I wasn't able to complete the task within the allowed steps."


# ╔══════════════════════════════════════════════════════════╗
# ║  RUN IT                                                   ║
# ║  Try different prompts to see how the agent uses tools.   ║
# ╚══════════════════════════════════════════════════════════╝

if __name__ == "__main__":
    # Test 1: Single tool use (calculator)
    run_agent("What is 15% tip on a dinner bill of $847.50?")

    print("\n\n")

    # Test 2: Multi-tool use (lookup + calculator + save)
    run_agent(
        "Look up the population of India, then calculate what 0.1% "
        "of that population is, and save the result as a note."
    )

    print("\n\n")

    # Test 3: Tool selection (should pick the right tool)
    run_agent("What is the speed of light?")
