import httpx
import pytest

from isaas_vendor_catalog_agent.backend import BackendClient


def echo_api_key(request: httpx.Request) -> httpx.Response:
    return httpx.Response(200, json={"status": "UP", "key": request.headers.get("X-API-Key")})


@pytest.mark.anyio
async def test_api_key_is_sent_when_configured():
    client = BackendClient(
        "http://backend.test", api_key="secret", transport=httpx.MockTransport(echo_api_key)
    )

    body = await client.health()

    assert body["key"] == "secret"


@pytest.mark.anyio
async def test_no_api_key_header_when_not_configured():
    client = BackendClient("http://backend.test", transport=httpx.MockTransport(echo_api_key))

    body = await client.health()

    assert body["key"] is None
