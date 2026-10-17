# Agent instructions

Standalone MCP server (Python) that lets external agents manage iSaaS catalog listings on behalf of a vendor. Project decisions and history are in the knowledge base: https://github.com/isaas-org/isaas-catalog-kb-agent-based-development

## Rules

- Never commit or push to `main`. Work only on the feature branch the repo owner names (pattern `feature/FD-<n>_<Description>`).
- All data comes from `isaas-vendor-catalog-mgmt-backend` through `BackendClient` (`backend.py`). Never connect to the database from this service.
- The MCP SDK is v2 (`mcp>=2.3,<3`): servers are `mcp.server.mcpserver.MCPServer`, not the v1 `FastMCP`.
- Each tool gets a test that drives it through `server.call_tool(...)` with an `httpx.MockTransport` backend.
- Tools report backend failures as data the agent can act on, not as unhandled exceptions.

## Commands

- Install: `uv sync`
- Lint and test: `uv run ruff check . && uv run ruff format --check . && uv run pytest`
- Run: `uv run isaas-vendor-catalog-agent` (streamable HTTP on 127.0.0.1:8092, path `/mcp`)
