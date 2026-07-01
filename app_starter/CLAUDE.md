# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

`uv` is at `/Users/hudatariq/Library/Python/3.9/bin/uv` if not on PATH.

```bash
# Setup
uv venv && source .venv/bin/activate
uv pip install -e .

# Run MCP server
uv run main.py

# Run all tests
uv run pytest

# Run a single test
uv run pytest tests/test_document.py::TestBinaryDocumentToMarkdown::test_binary_document_to_markdown_with_docx
```

## Architecture

The project is an MCP server built with `FastMCP`. The entrypoint is `main.py`, which instantiates the server and registers tools by passing functions to `mcp.tool()()`. Tools live in the `tools/` package as plain Python functions — they are independent of MCP and can be tested directly.

**Adding a new tool:**

1. Define the function in `tools/` using `pydantic.Field` for parameter descriptions:

```python
from pydantic import Field

def my_tool(
    param: str = Field(description="What this parameter does"),
) -> str:
    """One-line summary.

    Detailed explanation of functionality.

    When to use:
    - ...

    Examples:
    >>> my_tool("input")
    "output"
    """
    ...
```

2. Register it in `main.py`:

```python
from tools.my_module import my_tool
mcp.tool()(my_tool)
```

Tool docstrings are surfaced directly to the AI client, so they should explain *when* to use the tool, not just what it does.

## Key Dependencies

- `mcp[cli]==1.8.0` — MCP server framework (`FastMCP`)
- `markitdown[docx,pdf]` — converts binary DOCX/PDF to markdown via `MarkItDown` + `StreamInfo`
- `pydantic` — parameter validation and `Field` descriptions for tool parameters

## Code Style

- Always apply appropriate types to function args
