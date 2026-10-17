# isaas-vendor-catalog-mgmt-agent-app

Standalone MCP server that lets AI agents manage iSaaS catalog listings on behalf of a vendor. It reaches marketplace data only through [`isaas-vendor-catalog-mgmt-backend`](https://github.com/isaas-org/isaas-vendor-catalog-mgmt-backend), never from the database.

## Stack

- Python 3.13, managed with [uv](https://docs.astral.sh/uv/)
- MCP Python SDK 2.x (`MCPServer`), httpx
- pytest, ruff

## Running locally

Start the vendor backend first (port 8082), then:

```bash
uv sync
uv run isaas-vendor-catalog-agent
```

The server listens on `http://127.0.0.1:8092/mcp` (streamable HTTP). For an agent client that launches servers over stdio, set `MCP_TRANSPORT=stdio`.

## Tools

| Tool | What it does |
|------|--------------|
| `backend_health` | Reports whether the vendor backend is reachable (`UP`, or `UNREACHABLE` with a reason) |

Listing management tools (items, pricing plans, media) come next, once the backend exposes those endpoints.

## Configuration

Read from environment variables (see `.env.example`):

| Variable | Default | Notes |
|----------|---------|-------|
| `BACKEND_API_URL` | `http://localhost:8082` | Vendor backend base URL |
| `BACKEND_API_KEY` | unset | Shared service key, sent as `X-API-Key` when set |
| `MCP_TRANSPORT` | `streamable-http` | `stdio` or `streamable-http` |
| `MCP_HOST` | `127.0.0.1` | |
| `MCP_PORT` | `8092` | The buyer agent app uses 8091 |

## Checks

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest
```

CI (`.github/workflows/test.yml`) runs all three on every PR and every push to `feature/**`.
