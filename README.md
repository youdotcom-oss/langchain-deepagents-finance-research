# Finance Research Agent

A [LangChain Deep Agents](https://docs.langchain.com/oss/python/deepagents/overview) project that performs financial research using [You.com's Finance Research API](https://you.com/docs/finance-research/overview). 

This project is focused on conducting **GDP macroeconomic analysis**. There is a predefined preset for researching **software company valuations** as well, but can you easily add more. Simply clone `examples/eu_gdp_analysis.py` and change your primary query. Then, configure your agent's system behavior by creating a system prompt in `prompts.py`.

## How It Works

The agent decomposes broad financial questions into precise queries, sends them to You.com's Finance Research API through the `you-finance` tool, and synthesizes the cited results into a structured report. The Finance Research API handles the heavy lifting internally — multi-step research, source verification, and citation generation — so the agent focuses on query planning and report assembly.

## Presets

| Preset | Description | Example Query |
|--------|-------------|---------------|
| `gdp` | GDP and macroeconomic analysis across countries/regions | EU GDP by country with anomaly detection |
| `software_valuations` | Public software company valuation multiples | Median EV/Revenue and EV/EBITDA by segment |

Each preset provides a tailored system prompt, query decomposition strategy, and report structure. The underlying tool, skill files, and agent machinery are shared.

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
│       ├── agent.py             # Deep Agent setup with HTTP/MCP tool
│       ├── prompts.py           # Preset system prompts and workflows
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

The agent uses a thin orchestration layer on top of the Finance Research API:

1. **Preset selection** — Choose a research preset (`gdp` or `software_valuations`) that configures the system prompt, query decomposition strategy, and report structure.
2. **Decompose** — Break the user's question into scoped `youdotcom-finance-research` queries with the right effort level (`deep` or `exhaustive`) and source control.
3. **Query** — Call `youdotcom-finance-research` via direct HTTP (or MCP). The API internally runs parallel research branches, consults structured public data, and returns cited answers with `[[n]]` source tags.
4. **Synthesize** — Merge results from multiple tool calls into a unified report with re-numbered citations.

The agent does **not** duplicate work the Finance Research API already handles (source verification, cross-referencing, multi-step evidence gathering).

## Tool Transport

The agent supports two methods for calling the Finance Research API, controlled by `TOOL_TRANSPORT` in `agent.py`:

- **`http`** (default) — Direct HTTP POST via `httpx`. Simpler, no MCP overhead.
- **`mcp`** — Uses the You.com MCP server via `langchain-mcp-adapters`. Useful if you want the standard MCP tool interface.

Both methods are fully implemented; swap by changing a single constant.
