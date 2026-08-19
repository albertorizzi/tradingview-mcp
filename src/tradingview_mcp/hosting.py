"""Deployment entry point for the TradingView MCP server."""

from __future__ import annotations

from tradingview_mcp import server
from tradingview_mcp.transport_config import transport_security_from_env


def main() -> None:
    security = transport_security_from_env()
    if security is not None:
        # FastMCP creates the Streamable HTTP session manager lazily when
        # ``run()`` starts, so updating the settings here applies the allowlist
        # before any HTTP transport is created.
        server.mcp.settings.transport_security = security

    server.main()
