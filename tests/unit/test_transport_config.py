from tradingview_mcp.transport_config import transport_security_from_env


def test_allowed_hosts_are_expanded_for_remote_mcp(monkeypatch):
    monkeypatch.setenv(
        "MCP_ALLOWED_HOSTS",
        "mcp.example.com, staging-mcp.example.com",
    )

    security = transport_security_from_env()

    assert security is not None
    assert security.enable_dns_rebinding_protection is True
    assert "mcp.example.com" in security.allowed_hosts
    assert "mcp.example.com:*" in security.allowed_hosts
    assert "staging-mcp.example.com" in security.allowed_hosts
    assert "staging-mcp.example.com:*" in security.allowed_hosts
    assert "localhost:*" in security.allowed_hosts
    assert "https://mcp.example.com" in security.allowed_origins
    assert "https://mcp.example.com:*" in security.allowed_origins


def test_missing_allowed_hosts_preserves_sdk_default(monkeypatch):
    monkeypatch.delenv("MCP_ALLOWED_HOSTS", raising=False)

    assert transport_security_from_env() is None
