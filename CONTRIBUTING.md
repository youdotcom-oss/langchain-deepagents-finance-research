# Contributing

## Getting Started

1. Fork the repository and create a branch from `main`.
2. Install dependencies with `uv sync`.
3. Copy `.env.example` to `.env` and fill in your API keys.

## Making Changes

- Keep changes focused. One feature or fix per pull request.
- Match the existing code style.
- If adding a new preset, add it to the `PRESETS` registry in `src/finance_research/prompts.py` following the existing pattern.

## Submitting a Pull Request

1. Ensure your branch is up to date with `main`.
2. Open a pull request with a clear description of what changed and why.

## Reporting Issues

Open an issue with steps to reproduce, expected behavior, and actual behavior. Include relevant error output and your Python version.
