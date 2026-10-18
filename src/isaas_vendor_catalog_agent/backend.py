from typing import Any

import httpx


class BackendClient:
    """Async client for isaas-vendor-catalog-mgmt-backend.

    This service never connects to the database; all marketplace data goes
    through the backend's API so business rules live in one place.
    """

    def __init__(
        self,
        base_url: str,
        api_key: str | None = None,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        headers = {"X-API-Key": api_key} if api_key else {}
        self._http = httpx.AsyncClient(
            base_url=base_url, headers=headers, timeout=10.0, transport=transport
        )

    async def health(self) -> dict[str, Any]:
        res = await self._http.get("/actuator/health")
        res.raise_for_status()
        return res.json()

    async def aclose(self) -> None:
        await self._http.aclose()
