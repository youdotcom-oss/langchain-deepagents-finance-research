import asyncio
import json
import logging
import ssl
from datetime import timedelta
from typing import Literal

import httpx
from langchain.tools import tool

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
RETRY_BACKOFF_SECONDS = 5

# ---------------------------------------------------------------------------
# Tool transport method
# ---------------------------------------------------------------------------
# Set to "http" for direct HTTP calls (recommended — simpler, no MCP overhead)
# Set to "mcp" to use the You.com MCP server via langchain-mcp-adapters
TOOL_TRANSPORT = "http"

# ---------------------------------------------------------------------------
# HTTP transport settings (used when TOOL_TRANSPORT = "http")
# ---------------------------------------------------------------------------
# read=None means no read timeout — the Finance Research API can take 10+ min
# at "exhaustive" effort. Connect timeout stays at 30s for fast failure on
# unreachable servers.
HTTP_API_TIMEOUT = httpx.Timeout(30.0, read=None)

HTTP_ENDPOINT = "https://api.you.com/v1/finance_research"

# ---------------------------------------------------------------------------
# MCP transport settings (used when TOOL_TRANSPORT = "mcp")
# ---------------------------------------------------------------------------
# The MCP server exposes multiple tools; we filter to just "you-finance".
MCP_SERVER_URL = "https://api.you.com/mcp?tools=you-finance"
MCP_TOOL_NAME = "you-finance"

# Custom httpx timeout for MCP — the default SSE read timeout is 300s which
# is too short for deep/exhaustive research. This factory overrides it.
MCP_HTTP_TIMEOUT = httpx.Timeout(120.0, read=None)


def _mcp_http_client_factory(
    headers: dict[str, str] | None = None,
    timeout: httpx.Timeout | None = None,
    auth: httpx.Auth | None = None,
) -> httpx.AsyncClient:
    """Custom httpx client factory for MCP transport."""
    return httpx.AsyncClient(
        headers=headers,
        timeout=MCP_HTTP_TIMEOUT,
        auth=auth,
        follow_redirects=True,
    )


# ---------------------------------------------------------------------------
# HTTP tool implementation
# ---------------------------------------------------------------------------
def create_you_finance_tool(api_key: str):
    """Create a LangChain tool that calls the You.com Finance Research API via direct HTTP."""

    @tool(parse_docstring=True)
    async def you_finance_research(
        input: str,
        research_effort: Literal["deep", "exhaustive"] = "deep",
    ) -> str:
        """Research financial and macroeconomic topics with cited sources.

        Calls the You.com Finance Research API to get finance-grade research, source-backed numeric answers,
        or exact public/company/macroeconomic evidence.
        Invokes the you-finance MCP tool which internally runs multi-step research,
        consults structured public data (World Bank, IMF, OECD, Eurostat, FRED) as well as licensed private data,
        verifies sources across parallel branches, and returns cited answers with [[n]] source tags.

        Args:
            input: The research question (max 40,000 characters).
            research_effort: How thorough the research should be. lite is fast,
                standard is default, deep is thorough, exhaustive is most complete.
        """
        body = {
            "input": input,
            "research_effort": research_effort,
        }

        headers = {"Content-Type": "application/json", "X-API-Key": api_key}

        last_error = None
        response = None
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                async with httpx.AsyncClient(timeout=HTTP_API_TIMEOUT) as client:
                    response = await client.post(
                        HTTP_ENDPOINT,
                        headers=headers,
                        json=body,
                    )
                break
            except (ssl.SSLError, httpx.ConnectError, httpx.RemoteProtocolError) as e:
                last_error = e
                if attempt < MAX_RETRIES:
                    wait = RETRY_BACKOFF_SECONDS * attempt
                    logger.warning(
                        "you-finance call failed (attempt %d/%d): %s. Retrying in %ds...",
                        attempt,
                        MAX_RETRIES,
                        e,
                        wait,
                    )
                    await asyncio.sleep(wait)

        if response is None:
            return f"Error: request failed after {MAX_RETRIES} attempts. Last error: {last_error}"

        if response.status_code != 200:
            return f"Error {response.status_code}: {response.text}"

        data = response.json()
        output = data.get("output", {})
        content = output.get("content", "")
        content_type = output.get("content_type", "text")
        sources = output.get("sources", [])

        if content_type == "object":
            result = json.dumps(content, indent=2)
        else:
            result = content

        if sources:
            result += "\n\n### Sources\n"
            for i, src in enumerate(sources, 1):
                title = src.get("title", "Untitled")
                url = src.get("url", "")
                result += f"[[{i}]] {title}: {url}\n"

        return result

    return you_finance_research


# ---------------------------------------------------------------------------
# MCP tool loader
# ---------------------------------------------------------------------------
async def load_mcp_tools(api_key: str):
    """Load the you-finance tool via MCP transport."""
    from langchain_mcp_adapters.client import MultiServerMCPClient

    client = MultiServerMCPClient(
        {
            "ydc-server": {
                "transport": "http",
                "url": MCP_SERVER_URL,
                "headers": {"Authorization": f"Bearer {api_key}"},
                "timeout": timedelta(seconds=600),
                "sse_read_timeout": timedelta(seconds=600),
                "httpx_client_factory": _mcp_http_client_factory,
            }
        }
    )

    all_tools = await client.get_tools()
    tools = [t for t in all_tools if t.name == MCP_TOOL_NAME]
    if not tools:
        available = [t.name for t in all_tools]
        raise RuntimeError(
            f"{MCP_TOOL_NAME} tool not found. Available tools: {available}"
        )

    return tools, client
