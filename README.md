# Finance Research Agent

A [LangChain Deep Agents](https://docs.langchain.com/oss/python/deepagents/overview) project that performs financial research using [You.com's Finance Research API](https://you.com/docs/finance-research/overview). 

This project is focused on conducting **GDP macroeconomic analysis**. There is a predefined preset for researching **software company valuations** as well, but you can easily add more. Simply clone `examples/eu_gdp_analysis.py` and change your primary query. Then, configure your agent's system behavior by creating a system prompt in `prompts.py`.

## How It Works

The GDP preset uses a multi-subagent architecture built on Deep Agents. An orchestrator agent coordinates five specialized subagents — `landscape-scanner`, `anomaly-analyst`, `expenditure-decomposer`, `sector-decomposer`, and `country-investigator` — each with a focused system prompt and access to the You.com Finance Research API. The orchestrator plans the research via `write_todos`, dispatches subagents via the `task` tool, fans out per-country investigations in parallel, cross-references all workpapers for contradictions, and synthesizes the final report.

Each subagent writes its output to a named workpaper file on a `FilesystemBackend`. The Finance Research API handles the heavy lifting internally — multi-step research, source verification, and citation generation — so the subagents focus on query construction, and the orchestrator focuses on workflow coordination and report assembly.

## Presets

| Preset | Description | Example Query |
|--------|-------------|---------------|
| `gdp` | GDP and macroeconomic analysis across countries/regions | EU GDP by country with anomaly detection |
| `software_valuations` | Public software company valuation multiples | Median EV/Revenue and EV/EBITDA by segment |

Each preset provides a tailored system prompt, query decomposition strategy, and report structure. The GDP preset uses multi-subagent orchestration with workpapers. The software valuations preset uses single-agent mode. The underlying tool, skill files, and agent machinery are shared.

## Project Structure

```
├── server.py                    # FastAPI streaming server (SSE)
├── Dockerfile                   # Docker deployment config
├── STREAMING_SPEC.md            # SSE streaming protocol spec for frontend integration
├── LICENSE                      # MIT license
├── CONTRIBUTING.md              # Contribution guidelines
├── skills/
│   └── youdotcom-finance-research/
│       ├── SKILL.md             # Finance Research API orchestration skill
│       └── openapi_finance_research.yaml # OpenAPI spec for reference
├── src/
│   └── finance_research/
│       ├── agent.py             # Deep Agent setup, subagents, FilesystemBackend
│       ├── tools.py             # Finance Research API tool (HTTP + MCP transports)
│       ├── prompts.py           # Orchestrator + subagent prompts and workflows
│       └── output.py            # Markdown/JSON report formatters
├── examples/
│   └── eu_gdp_analysis.py       # GDP preset example
└── reports/                     # Output directory — workpapers and final reports from local runs
    └── YYYYMMDD_HHMMSS/       # Timestamped run directories
```

## Setup

### Prerequisites

- Python 3.14+
- [uv](https://docs.astral.sh/uv/)
- A **You.com API key** — [sign up at you.com](https://you.com/platform) and get an API key.
- A **Fireworks API key** — [get one at fireworks.ai](https://fireworks.ai). The agent runs Minimax M2.7 (orchestrator) and M2.5 (subagents) via Fireworks. You can easily use OpenRouter, Anthropic and many other providers.

### Install

```bash
uv sync
```

### Environment Variables

Copy `.env.example` to `.env` and fill in your keys:

```
FIREWORKS_API_KEY=your_fireworks_api_key  # Required for using models via Fireworks
YDC_API_KEY=your_you_com_api_key  # Required: get one for free from you.com/platform

# Enable auth when running as a server 
API_SECRET=your_api_secret

# LangSmith
LANGSMITH_API_KEY=your_langsmith_api_key  # Optional

# Enable LangSmith traces
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://aws.api.smith.langchain.com
LANGSMITH_PROJECT="My LangSmith project"
```

## Usage

### Run the examples

```bash
# GDP analysis
uv run python examples/eu_gdp_analysis.py

# JSON output
uv run python examples/eu_gdp_analysis.py --format json
```

### Use programmatically

```python
import asyncio
from finance_research.agent import run_finance_research

# GDP preset
report = asyncio.run(run_finance_research(
    query="Using the latest available GDP data for 2025, analyze each country within the EU economic zone. Highlight those that are increasing or decreasing at an anomalous rate. Specify and break down which industries are causing these shifts and investigate macroeconomic trends within each country that are contributing.",
    preset="gdp",
))

# Software valuations preset
report = asyncio.run(run_finance_research(
    query="Median revenue and EBITDA multiples for public software companies over 5 years",
    preset="software_valuations",
))
```

## Streaming Server

`server.py` is a FastAPI server that wraps the agent and streams results back to the client via Server-Sent Events (SSE). This is useful for building frontends that show live progress as the agent researches.

### Run locally

```bash
uv run uvicorn server:app --host 0.0.0.0 --port 8000
```

### Endpoints

**`GET /health`**

Returns server status and available presets.

```json
{"status": "ok", "presets": ["gdp", "software_valuations"]}
```

**`POST /run`**

Starts a research run and streams SSE events.

```bash
curl -s -N --no-buffer \
  -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{"preset": "gdp", "query": "What is Germany GDP in 2024?"}'
```

Request body:

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `preset` | `"gdp" \| "software_valuations"` | `"gdp"` | Research preset to use |
| `query` | `string` | required | The research question |
| `output_format` | `"markdown" \| "json"` | `"markdown"` | Format of the final report |

If `API_SECRET` is set, include `Authorization: Bearer <secret>` in the request headers.

The stream emits events of type: `status`, `tool_call`, `tool_result`, `token`, `thinking` (model-dependent), `report`, `error`, and `step` (node completion). See [`STREAMING_SPEC.md`](./STREAMING_SPEC.md) for the full event reference and frontend integration guide.

## Deployment

### Docker

```bash
docker build -t finance-research .
docker run -p 8000:8000 \
  -e FIREWORKS_API_KEY=your_key \
  -e YDC_API_KEY=your_key \
  finance-research
```

### Railway

The project ships with a `Dockerfile` and is ready to deploy on [Railway](https://railway.com). Set the required environment variables (`FIREWORKS_API_KEY`, `YDC_API_KEY`) in the Railway service settings. Optionally set `API_SECRET` to protect the `/run` endpoint.

## Architecture

The GDP preset uses multi-subagent orchestration with the canonical Deep Agents patterns:

1. **Plan** — The orchestrator calls `write_todos` to lay out a layered research plan as a checklist.
2. **Layer 1 — Landscape scan** — Dispatches `landscape-scanner` subagent to retrieve data tables for all 27 EU member states via Shape A queries. Results written to `/workpapers/landscape_scan.md`.
3. **Layer 2 — Anomaly detection** — Dispatches `anomaly-analyst` subagent to compute the regional mean, flag outliers (>=2.0 pp deviation), and recommend investigation targets. Writes to `/workpapers/anomaly_analysis.md` with a fenced JSON block at the end that the orchestrator parses to extract investigation targets. Pure analysis, no API calls.
4. **Layer 3a — Quantitative decomposition** — Dispatches `expenditure-decomposer` and `sector-decomposer` in parallel (two `task` calls in one message).
5. **Layer 3b — Country investigation fan-out** — Dispatches one `country-investigator` subagent per anomalous country, in parallel. Each runs Shape B queries and writes its own workpaper.
6. **Cross-reference** — The orchestrator reads all workpapers, checks for contradictions, and dispatches `general-purpose` for verification queries if needed.
7. **Synthesize** — Merges all workpapers into a final report with unified `[[n]]` citation numbering. Written to `/final_report.md`.

Each subagent receives the `you_finance_research` tool explicitly — the orchestrator itself doesn't have the tool (it coordinates via `task` dispatch, not direct API calls). The built-in `general-purpose` subagent is overridden with an explicit spec that includes the tool, so the orchestrator can dispatch ad-hoc verification queries. The orchestrator runs on Minimax M2.7 via Fireworks for complex coordination and synthesis; all subagents run on Minimax M2.5 via Fireworks.

## Extending and Modifying

This section is written as a map for coding agents and developers who want to fork, extend, or tune the project. All paths are relative to the repo root.

### Switching LLM Provider

**1. Add the provider package** to `pyproject.toml` dependencies (e.g. `langchain-anthropic`) and run `uv sync`.

**2. Set the API key** in `.env` (e.g. `ANTHROPIC_API_KEY=...`).

**3. Update model strings.** The project uses LangChain's `init_chat_model` string format (`<provider>:<model>`). There are two places to change:

- **Orchestrator** — `src/finance_research/agent.py`, the `create_deep_agent(..., model=...)` call (line ~140).  
  Current: `"fireworks:accounts/fireworks/models/minimax-m2p7"`
- **Subagents** — `src/finance_research/prompts.py`, inside `_gdp_subagents()`, the `subagent_model` variable (line ~264).  
  Current: `"fireworks:accounts/fireworks/models/minimax-m2p5"`

You can use **different models per subagent** by overriding the `"model"` key on individual subagent dicts in the list returned by `_gdp_subagents()`.

### Adjusting System Prompts

All prompts live in `src/finance_research/prompts.py` and are assembled from three layers:

| Layer | What it controls | Where |
|-------|------------------|-------|
| Shared fragments | Query-shape guidance, effort levels, citation format, API retrieval coverage | `_SHARED_TOOL_PREAMBLE`, `_SHARED_EFFORT_LEVELS`, `_SHARED_CITATION_FORMAT`, `_API_RETRIEVAL_COVERAGE` |
| Orchestrator prompt | Workflow choreography, subagent dispatch instructions, analytical frameworks, report structure | `GDP_ORCHESTRATOR_PROMPT` / `GDP_ORCHESTRATOR_WORKFLOW` |
| Subagent prompts | Specialist role definitions, per-layer task descriptions, output file paths | `LANDSCAPE_SCANNER_PROMPT`, `ANOMALY_ANALYST_PROMPT`, etc. |

**To tune the analytical framework** (e.g. change the expenditure decomposition from C+I+G+NX to a different taxonomy), edit the **orchestrator prompt** (`GDP_ORCHESTRATOR_PROMPT`) — this is what the orchestrator sees when synthesizing the final report.

**To change what data a subagent retrieves**, edit that subagent's prompt directly (e.g. add fiscal-balance retrieval to `LANDSCAPE_SCANNER_PROMPT`). Make sure the orchestrator's workflow (`GDP_ORCHESTRATOR_WORKFLOW`) references the same workpaper path if you change it.

### Adjusting Subagents

The GDP preset's subagent list is built by `_gdp_subagents()` in `prompts.py` (returned as a `list[dict]`). Each dict has:

```python
{
    "name": "landscape-scanner",
    "description": "...",
    "system_prompt": LANDSCAPE_SCANNER_PROMPT.format(date=date),
    "tools": api_tools,          # or [] for no-tool subagents
    "skills": api_skills,        # or omitted
    "model": subagent_model,     # can override per subagent
}
```

**Common modifications:**
- **Remove a subagent** — delete its dict from the list. Update the orchestrator workflow so it no longer dispatches that step.
- **Add a subagent** — write a new prompt constant, create a new dict with a unique `"name"`, and add a workflow step that dispatches it via `task(subagent_type="your-name", description="...")`.
- **Give a subagent different tools** — some subagents (e.g. `anomaly-analyst`) set `"tools": []` because they only reason over existing workpapers. Others get `api_tools` so they can call the Finance Research API.
- **Change the anomaly threshold** — the 2.0 pp and 1.5 pp thresholds are hardcoded in `ANOMALY_ANALYST_PROMPT` (lines ~360-370). Adjust the numbers in that prompt and update the orchestrator workflow to match.

### Adding a New Preset

A preset is an entry in the `PRESETS` dict at the bottom of `prompts.py`:

```python
PRESETS = {
    "gdp": {
        "system_prompt": GDP_ORCHESTRATOR_PROMPT,
        "workflow": GDP_ORCHESTRATOR_WORKFLOW,
        "description": "GDP and macroeconomic analysis",
        "subagents": _gdp_subagents,   # callable: (date, tools) -> list[dict]
    },
    "software_valuations": {
        "system_prompt": SOFTWARE_VALUATIONS_PROMPT,
        "workflow": SOFTWARE_VALUATIONS_WORKFLOW,
        "description": "Public software company valuation multiples",
        "subagents": [],  # empty list = single-agent mode, no subagents
    },
}
```

To add a new preset:

1. Write a system prompt and workflow (or reuse the shared fragments).
2. Optionally write a subagent factory function (signature: `def _my_subagents(date: str, tools: list | None = None) -> list[dict]`).
3. Add the entry to `PRESETS`.
4. The preset name is automatically exposed by `/health` and accepted by the server and example scripts.

### Tuning Server Behavior

- **Auth** — `API_SECRET` env var enables bearer-token auth on `POST /run`. Set it empty to disable. See `_check_auth()` in `server.py`.
- **CORS** — `allow_origins=["*"]` in `server.py`; tighten for production.
- **SSE events** — The `_stream_agent()` function in `server.py` emits events. Add new event types by adding `_sse_event("my_event", {...})` calls inside the chunk-processing loops.
- **Tool transport** — Change `TOOL_TRANSPORT` in `tools.py` (default `"http"`, alternative `"mcp"`).
- **LangSmith cost tracking** — `tools.py` attaches per-call You.com API cost metadata to LangSmith traces via `@traceable` and `get_current_run_tree().set(usage_metadata={...})`. Costs are defined in `YDC_COST_PER_CALL` (deep: $0.11, exhaustive: $0.50).

## Tool Transport

The agent supports two methods for calling the Finance Research API, controlled by `TOOL_TRANSPORT` in `tools.py`:

- **`http`** (default) — Direct HTTP POST via `httpx`. Simpler, no MCP overhead.
- **`mcp`** — Uses the You.com MCP server via `langchain-mcp-adapters`. Useful if you want the standard MCP tool interface.

Both methods are fully implemented; swap by changing a single constant.
