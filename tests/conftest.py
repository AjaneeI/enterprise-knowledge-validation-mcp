"""Real subprocess transports; all network traffic stays on loopback."""
import asyncio
from contextlib import asynccontextmanager
from datetime import timedelta
from pathlib import Path
import socket
import subprocess
import sys
import httpx
import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamable_http_client

@pytest.fixture
def anyio_backend():
    return 'asyncio'

@asynccontextmanager
async def initialized(streams):
    async with ClientSession(streams[0], streams[1], read_timeout_seconds=timedelta(seconds=10)) as client:
        init = await client.initialize()
        assert init.serverInfo.name == 'Knowledge Operations Demo'
        yield client

@pytest.fixture(params=['stdio','streamable-http'])
async def session(request, tmp_path):
    if request.param == 'stdio':
        params = StdioServerParameters(command=sys.executable,args=['-m','src.server','--transport','stdio'])
        async with stdio_client(params) as streams:
            async with initialized(streams) as client:
                yield client
    else:
        with socket.socket() as sock:
            sock.bind(('127.0.0.1',0))
            port = sock.getsockname()[1]
        url=f'http://127.0.0.1:{port}/mcp'
        with (tmp_path/'server.log').open('w') as log:
            process=subprocess.Popen([sys.executable,'-m','src.server','--port',str(port)],stdout=log,stderr=log)
            try:
                async with httpx.AsyncClient(timeout=.5) as http:
                    for _ in range(100):
                        if process.poll() is not None:
                            pytest.fail((tmp_path/'server.log').read_text())
                        try:
                            await http.get(url)
                            break
                        except httpx.ConnectError:
                            await asyncio.sleep(.05)
                    else:
                        pytest.fail('MCP startup timed out')
                async with streamable_http_client(url) as streams:
                    async with initialized(streams) as client:
                        yield client
            finally:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=5)

@pytest.fixture(params=['duplicate_decision','contradictory_current'])
async def corrupt_session(request,tmp_path):
    import json
    from src.logic import DATA_PATH
    raw=DATA_PATH.read_text()
    if request.param=='duplicate_decision':
        raw=raw.replace('"decision": "approved"','"decision": "rejected", "decision": "approved"',1)
    else:
        data=json.loads(raw)
        data['procedures'][1]['superseded_by']='SOP-104@1.0'
        raw=json.dumps(data)
    path=tmp_path/'corrupt.json'
    path.write_text(raw)
    code='import sys; from pathlib import Path; from src import logic; logic.DATA_PATH=Path(sys.argv[1]); from src.server import mcp; mcp.run(transport="stdio")'
    params=StdioServerParameters(command=sys.executable,args=['-c',code,str(path)])
    async with stdio_client(params) as streams:
        async with initialized(streams) as client:
            yield client
