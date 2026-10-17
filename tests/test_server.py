import httpx
import pytest

from isaas_vendor_catalog_agent.backend import BackendClient
from isaas_vendor_catalog_agent.server import build_server


@pytest.fixture
def anyio_backend():
    return "asyncio"


def client_returning(handler) -> BackendClient:
    return BackendClient("http://backend.test", transport=httpx.MockTransport(handler))


@pytest.mark.anyio
async def test_backend_health_reports_backend_status():
    server = build_server(client_returning(lambda req: httpx.Response(200, json={"status": "UP"})))

    result = await server.call_tool("backend_health", {})

    assert result.structured_content == {"status": "UP"}


@pytest.mark.anyio
async def test_backend_health_reports_unreachable_backend():
    def refuse(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("connection refused", request=request)

    server = build_server(client_returning(refuse))

    result = await server.call_tool("backend_health", {})

    assert result.structured_content["status"] == "UNREACHABLE"


@pytest.mark.anyio
async def test_api_key_is_sent_when_configured():
    seen = {}

    def capture(request: httpx.Request) -> httpx.Response:
        seen["key"] = request.headers.get("X-API-Key")
        return httpx.Response(200, json={"status": "UP"})

    client = BackendClient(
        "http://backend.test", api_key="secret", transport=httpx.MockTransport(capture)
    )
    await client.health()

    assert seen["key"] == "secret"
