import httpx
from mcp.server.mcpserver import MCPServer

from isaas_vendor_catalog_agent.backend import BackendClient
from isaas_vendor_catalog_agent.config import load_settings


def build_server(backend: BackendClient) -> MCPServer:
    server = MCPServer(
        name="isaas-vendor-catalog",
        instructions="Tools for managing iSaaS catalog listings on behalf of a vendor.",
    )

    @server.tool()
    async def backend_health() -> dict[str, str]:
        """Report whether the iSaaS vendor catalog backend is reachable."""
        try:
            body = await backend.health()
        except httpx.HTTPError as err:
            return {"status": "UNREACHABLE", "detail": str(err)}
        return {"status": str(body.get("status", "UNKNOWN"))}

    return server


def main() -> None:
    settings = load_settings()
    server = build_server(BackendClient(settings.backend_api_url, settings.backend_api_key))
    if settings.transport == "stdio":
        server.run("stdio")
    else:
        server.run("streamable-http", host=settings.host, port=settings.port)


if __name__ == "__main__":
    main()
