"""Catches a dependency resolve that makes the supplied server unimportable."""
def test_server_imports():
    from src.server import mcp
    assert mcp.name == "Knowledge Operations Demo"
