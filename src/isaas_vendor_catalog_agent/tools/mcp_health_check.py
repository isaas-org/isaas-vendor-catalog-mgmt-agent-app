import httpx
from mcp.server.mcpserver import MCPServer

from isaas_vendor_catalog_agent.backend import BackendClient


class HealthCheckTools:
    """Tools that report whether the services this agent depends on are reachable."""

    def __init__(self, backend: BackendClient) -> None:
        self._backend = backend

    def register(self, server: MCPServer) -> None:
        server.add_tool(self.backend_health)

    async def backend_health(self) -> dict[str, str]:
        """Report whether the iSaaS vendor catalog backend is reachable."""
        try:
            body = await self._backend.health()
        except httpx.HTTPError as err:
            return {"status": "UNREACHABLE", "detail": str(err)}
        return {"status": str(body.get("status", "UNKNOWN"))}
