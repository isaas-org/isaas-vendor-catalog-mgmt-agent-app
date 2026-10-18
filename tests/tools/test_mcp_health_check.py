import httpx
import pytest

from isaas_vendor_catalog_agent.backend import BackendClient
from isaas_vendor_catalog_agent.server import build_server


def healthy_backend(request: httpx.Request) -> httpx.Response:
    return httpx.Response(200, json={"status": "UP"})


def refusing_backend(request: httpx.Request) -> httpx.Response:
    raise httpx.ConnectError("connection refused", request=request)


def server_with(handler):
    backend = BackendClient("http://backend.test", transport=httpx.MockTransport(handler))
    return build_server(backend)


@pytest.mark.anyio
async def test_backend_health_reports_backend_status():
    result = await server_with(healthy_backend).call_tool("backend_health", {})

    assert result.structured_content == {"status": "UP"}


@pytest.mark.anyio
async def test_backend_health_reports_unreachable_backend():
    result = await server_with(refusing_backend).call_tool("backend_health", {})

    assert result.structured_content["status"] == "UNREACHABLE"


@pytest.mark.anyio
async def test_backend_health_is_registered_without_arguments():
    tools = await server_with(healthy_backend).list_tools()

    health = next(tool for tool in tools if tool.name == "backend_health")
    assert health.input_schema.get("properties", {}) == {}
