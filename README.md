# Finance Research Agent

A [LangChain Deep Agents](https://docs.langchain.com/oss/python/deepagents/overview) project that performs financial research using [You.com's Finance Research API](https://you.com/docs/finance-research/overview). 

This project is focused on conducting **GDP macroeconomic analysis**. There is a predefined preset for researching **software company valuations** as well, but can you easily add more. Simply clone `examples/eu_gdp_analysis.py` and change your primary query. Then, configure your agent's system behavior by creating a system prompt in `prompts.py`.

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
└── examples/
    └── eu_gdp_analysis.py       # GDP preset example
```

## Setup

### Prerequisites

- Python 3.14+
- [uv](https://docs.astral.sh/uv/)
- A **You.com API key** — [sign up at you.com](https://you.com/platform) and get an API key.
- An **Anthropic API key** — [get one at console.anthropic.com](https://console.anthropic.com). You can easily use any other model provider supported by LangChain.

### Install

```bash
uv sync
```

### Environment Variables

Copy `.env.example` to `.env` and fill in your keys:

```
ANTHROPIC_API_KEY=your_anthropic_api_key
YDC_API_KEY=your_you_com_api_key  # Required: get from you.com/platform

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
    query="What was the GDP in 2024 for each EU country?",
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

See [`STREAMING_SPEC.md`](./STREAMING_SPEC.md) for the full SSE event reference and frontend integration guide.

## Deployment

### Docker

```bash
docker build -t finance-research .
docker run -p 8000:8000 \
  -e ANTHROPIC_API_KEY=your_key \
  -e YDC_API_KEY=your_key \
  finance-research
```

### Railway

The project ships with a `Dockerfile` and is ready to deploy on [Railway](https://railway.com). Set the required environment variables (`ANTHROPIC_API_KEY`, `YDC_API_KEY`) in the Railway service settings. Optionally set `API_SECRET` to protect the `/run` endpoint.

## Architecture

The GDP preset uses multi-subagent orchestration with the canonical Deep Agents patterns:

1. **Plan** — The orchestrator calls `write_todos` to lay out a layered research plan as a checklist.
2. **Layer 1 — Landscape scan** — Dispatches `landscape-scanner` subagent to retrieve data tables for all 27 EU member states via Shape A queries. Results written to `/workpapers/landscape_scan.md`.
3. **Layer 2 — Anomaly detection** — Dispatches `anomaly-analyst` subagent to compute the regional mean, flag outliers (>=2.0 pp deviation), and recommend investigation targets. Writes to `/workpapers/anomaly_analysis.md` with a fenced JSON block at the end that the orchestrator parses to extract investigation targets. Pure analysis, no API calls.
4. **Layer 3a — Quantitative decomposition** — Dispatches `expenditure-decomposer` and `sector-decomposer` in parallel (two `task` calls in one message).
5. **Layer 3b — Country investigation fan-out** — Dispatches one `country-investigator` subagent per anomalous country, in parallel. Each runs Shape B queries and writes its own workpaper.
6. **Cross-reference** — The orchestrator reads all workpapers, checks for contradictions, and dispatches `general-purpose` for verification queries if needed.
7. **Synthesize** — Merges all workpapers into a final report with unified `[[n]]` citation numbering. Written to `/final_report.md`.

Each subagent receives the `you_finance_research` tool explicitly — the orchestrator itself doesn't have the tool (it coordinates via `task` dispatch, not direct API calls). The built-in `general-purpose` subagent is overridden with an explicit spec that includes the tool, so the orchestrator can dispatch ad-hoc verification queries. The orchestrator runs on Opus 4.6 for complex coordination and synthesis; all subagents run on Sonnet 4.6.

## Tool Transport

The agent supports two methods for calling the Finance Research API, controlled by `TOOL_TRANSPORT` in `agent.py`:

- **`http`** (default) — Direct HTTP POST via `httpx`. Simpler, no MCP overhead.
- **`mcp`** — Uses the You.com MCP server via `langchain-mcp-adapters`. Useful if you want the standard MCP tool interface.

Both methods are fully implemented; swap by changing a single constant.
