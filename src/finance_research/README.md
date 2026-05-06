# `finance_research` — Core Agent Package

This package wires the LangChain Deep Agents framework to the You.com Finance Research API. It handles agent construction, subagent orchestration, tool transport, and report extraction.

## Files

| File | Purpose |
|------|---------|
| `agent.py` | `create_finance_research_agent()` — builds a Deep Agent with the selected preset, wires subagents, and configures a `CompositeBackend` (`StateBackend` for checkpoints + `FilesystemBackend` for workpapers). `run_finance_research()` is the high-level entry point. |
| `tools.py` | The `you_finance_research` LangChain tool (HTTP transport with retry logic) and `load_mcp_tools()` for MCP transport. Switch transports by changing `TOOL_TRANSPORT` (`"http"` or `"mcp"`). |
| `prompts.py` | All system prompts, workflows, and the `PRESETS` registry. Contains shared guidance on query shapes (A/B/C), effort levels, and citation handling, plus the full subagent and orchestrator prompts for the GDP preset. |
| `output.py` | `FinanceReport` dataclass and `extract_report_from_messages()` — pulls the final report from agent message history by checking `write_file` tool calls first, falling back to the last AI message. Also parses citations from `[[n]]` format. |
| `__init__.py` | Public API exports: `create_finance_research_agent`, `run_finance_research`. |
