# Session 1.2 — Tool Use & Function Calling
## Files
- 01_single_tool.py: Bare mechanics of a single tool call — request/response inspection
- 02_multi_tool_agent.py: Full multi-tool agent with agentic loop, 3 tools (calculator, fact lookup, note saver)

## How to run
```bash
cd session-1-2
python 01_single_tool.py   # See the raw tool call mechanics
python 02_multi_tool_agent.py   # Run the full agent with 3 test prompts
```

## Key concepts
- Tool definitions as JSON schemas
- The agentic while loop (stop_reason check)
- Tool execution in YOUR code, not Claude's
- Max iteration safety cap
