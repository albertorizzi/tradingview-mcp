"""Transport security configuration for remote MCP deployments."""

from __future__ import annotations

import os

from mcp.server.transport_security import TransportSecuritySettings

_LOCAL_HOSTS = ["127.0.0.1:*", "localhost:*", "[::1]:*"]
_LOCAL_ORIGINS = [
    "http://127.0.0.1:*",
    "http://localhost:*",
    "http://[::1]:*",
]


def transport_security_from_env() -> TransportSecuritySettings | None:
    """Build DNS-rebinding protection settings from ``MCP_ALLOWED_HOSTS``.

    ``MCP_ALLOWED_HOSTS`` is a comma-separated list of hostnames without a URL
    scheme, for example ``mcp.example.com,staging-mcp.example.com``.

    When the variable is not set, return ``None`` so FastMCP keeps its normal
    local-development defaults.
    """
    raw_hosts = os.environ.get("MCP_ALLOWED_HOSTS", "")
    configured_hosts = list(
        dict.fromkeys(host.strip() for host in raw_hosts.split(",") if host.strip())
    )

    if not configured_hosts:
        return None

    allowed_hosts = [*_LOCAL_HOSTS]
    allowed_origins = [*_LOCAL_ORIGINS]

    for host in configured_hosts:
        allowed_hosts.extend([host, f"{host}:*"])
        allowed_origins.extend(
            [
                f"http://{host}",
                f"https://{host}",
                f"http://{host}:*",
                f"https://{host}:*",
            ]
        )

    return TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=list(dict.fromkeys(allowed_hosts)),
        allowed_origins=list(dict.fromkeys(allowed_origins)),
    )
