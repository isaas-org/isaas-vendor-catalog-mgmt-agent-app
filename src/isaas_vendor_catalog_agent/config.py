import os
from dataclasses import dataclass
from typing import Literal

Transport = Literal["stdio", "streamable-http"]


@dataclass(frozen=True)
class Settings:
    backend_api_url: str
    # Shared service key for the backend. Optional until the backend enforces it.
    backend_api_key: str | None
    transport: Transport
    host: str
    port: int


def load_settings() -> Settings:
    transport = os.environ.get("MCP_TRANSPORT", "streamable-http")
    if transport not in ("stdio", "streamable-http"):
        raise ValueError(f"MCP_TRANSPORT must be 'stdio' or 'streamable-http', got {transport!r}")

    return Settings(
        backend_api_url=os.environ.get("BACKEND_API_URL", "http://localhost:8082"),
        backend_api_key=os.environ.get("BACKEND_API_KEY") or None,
        transport=transport,
        host=os.environ.get("MCP_HOST", "127.0.0.1"),
        port=int(os.environ.get("MCP_PORT", "8092")),
    )
