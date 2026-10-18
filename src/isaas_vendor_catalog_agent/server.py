from mcp.server.mcpserver import MCPServer

from isaas_vendor_catalog_agent.backend import BackendClient
from isaas_vendor_catalog_agent.config import load_settings
from isaas_vendor_catalog_agent.tools.mcp_health_check import HealthCheckTools


def build_server(backend: BackendClient) -> MCPServer:
    server = MCPServer(
        name="isaas-vendor-catalog",
        instructions="Tools for managing iSaaS catalog listings on behalf of a vendor.",
    )
    HealthCheckTools(backend).register(server)
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
