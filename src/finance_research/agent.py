import logging
import os
import shutil
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any

from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, StateBackend
from deepagents.backends.filesystem import FilesystemBackend
from langgraph.checkpoint.memory import MemorySaver

from finance_research.output import FinanceReport, extract_report_from_messages
from finance_research.prompts import PRESETS
from finance_research.tools import (
    TOOL_TRANSPORT,
    load_mcp_tools,
    you_finance_research,
)

logger = logging.getLogger(__name__)


@dataclass
class AgentSession:
    agent: Any
    reports_dir: str
    mcp_client: Any = field(default=None)


# ---------------------------------------------------------------------------
# Shared config
# ---------------------------------------------------------------------------
SKILLS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "skills",
    "youdotcom-finance-research",
)


def _copy_skill_files_to_backend(root_dir: str) -> None:
    """Copy skill files into the FilesystemBackend root directory.

    Subagents reference skills via paths like /skills/youdotcom-finance-research/,
    which resolve against the backend's root directory.
    """
    target_dir = os.path.join(root_dir, "skills", "youdotcom-finance-research")
    os.makedirs(target_dir, exist_ok=True)
    for filename in os.listdir(SKILLS_DIR):
        if filename.startswith("."):
            continue
        src = os.path.join(SKILLS_DIR, filename)
        if os.path.isfile(src):
            shutil.copy2(src, os.path.join(target_dir, filename))


# ---------------------------------------------------------------------------
# Agent factory
# ---------------------------------------------------------------------------
async def create_finance_research_agent(
    preset: str = "gdp",
    output_format: str = "markdown",
    output_dir: str | None = None,
):
    """Create a finance research agent with the given preset.

    Args:
        preset: Which research preset to use. One of: "gdp", "software_valuations".
        output_format: "markdown" or "json" for the final report format.
        output_dir: Directory where workpapers and final report are written.
            Defaults to ./reports/<timestamp>/ so files are always visible.
    """
    if preset not in PRESETS:
        available = ", ".join(PRESETS.keys())
        raise ValueError(f"Unknown preset '{preset}'. Available: {available}")

    if not os.environ.get("YDC_API_KEY"):
        raise ValueError("YDC_API_KEY environment variable is required.")

    # --- Choose tool transport ---
    mcp_client = None
    if TOOL_TRANSPORT == "mcp":
        tools, mcp_client = await load_mcp_tools()
    else:
        tools = [you_finance_research]

    # --- Build system prompt from preset ---
    preset_config = PRESETS[preset]
    today = date.today().strftime("%B %d, %Y")
    system_prompt = (
        preset_config["system_prompt"].format(date=today)
        + "\n\n"
        + preset_config["workflow"]
    )

    # --- Set up backend ---
    # Use a stable, visible output directory so workpapers and the final report
    # are easy to inspect after the run. Fall back to a dated ./reports/ subdir.
    if output_dir:
        reports_dir = output_dir
    else:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        reports_dir = os.path.join(os.getcwd(), "reports", ts)
    os.makedirs(reports_dir, exist_ok=True)

    # CompositeBackend: agent-internal state (checkpoints, offloaded results) goes to StateBackend (in-memory);
    # Explicit file writes (workpapers, report) go to FilesystemBackend rooted at reports_dir.
    backend = CompositeBackend(
        default=StateBackend(),
        routes={
            "/": FilesystemBackend(root_dir=reports_dir, virtual_mode=True),
        },
    )

    # Copy skill files into the backend so subagents can read them
    _copy_skill_files_to_backend(reports_dir)

    # Create workpapers directory
    os.makedirs(os.path.join(reports_dir, "workpapers"), exist_ok=True)

    checkpointer = MemorySaver()

    # --- Build subagent list ---
    # Subagents do NOT inherit tools from the orchestrator — each one must
    # receive its tools explicitly.  Pass the finance research tool(s) so the
    # factory can wire them into every subagent that calls the API.
    subagent_factory = preset_config.get("subagents")
    subagents = subagent_factory(today, tools=tools) if subagent_factory else None

    # --- Build orchestrator tools list ---
    # When subagents handle the research, the orchestrator coordinates via
    # `task` dispatch — it doesn't need the Finance Research API tool itself.
    # In single-agent mode (no subagents), the orchestrator calls the API directly.
    if subagents:
        agent_tools = []
    else:
        agent_tools = list(tools)

    agent = create_deep_agent(
        model="anthropic:claude-opus-4-6",
        tools=agent_tools,
        system_prompt=system_prompt,
        subagents=subagents,
        backend=backend,
        checkpointer=checkpointer,
    )

    return AgentSession(
        agent=agent,
        reports_dir=reports_dir,
        mcp_client=mcp_client,
    )


async def run_finance_research(
    query: str,
    preset: str = "gdp",
    output_format: str = "markdown",
    thread_id: str = "finance-research-1",
    output_dir: str | None = None,
) -> FinanceReport:
    """Run a finance research query and return a structured report.

    Args:
        query: The research question to investigate.
        preset: Which research preset to use. One of: "gdp", "software_valuations".
        output_format: "markdown" or "json".
        thread_id: Thread ID for conversation state.
        output_dir: Directory for workpapers and final report. Defaults to ./reports/<timestamp>/.

    Returns:
        A FinanceReport with findings, citations, and formatted output.
    """
    session = await create_finance_research_agent(
        preset=preset,
        output_format=output_format,
        output_dir=output_dir,
    )

    config = {"configurable": {"thread_id": thread_id}}

    result = await session.agent.ainvoke(
        {"messages": [{"role": "user", "content": query}]},
        config=config,
    )

    report = extract_report_from_messages(result["messages"], query)

    if output_format == "json":
        print(report.to_json_string())
    else:
        print(report.to_markdown())

    return report
