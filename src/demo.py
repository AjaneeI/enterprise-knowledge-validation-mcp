"""A real official-SDK MCP client; stdio starts and closes its own local server."""
import argparse
import asyncio
from contextlib import AsyncExitStack
from datetime import timedelta
import json
import sys
from urllib.parse import urlsplit
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamable_http_client

async def demonstrate(url=None):
    async with AsyncExitStack() as stack:
        if url:
            streams=await stack.enter_async_context(streamable_http_client(url))
        else:
            params=StdioServerParameters(command=sys.executable,args=['-m','src.server','--transport','stdio'])
            streams=await stack.enter_async_context(stdio_client(params))
        session=await stack.enter_async_context(ClientSession(streams[0],streams[1],read_timeout_seconds=timedelta(seconds=10)))
        init=await session.initialize()
        if init.serverInfo.name!='Knowledge Operations Demo':
            raise RuntimeError('Unexpected MCP server identity; refusing to invoke tools')
        tools=await session.list_tools()
        if {t.name for t in tools.tools}!={'check_procedure_status','assess_action_readiness'}:
            raise RuntimeError('Unexpected tool contract')
        results={}
        cases=[('superseded','check_procedure_status',{'procedure_id':'SOP-104@1.0'}),
               ('missing_approval','assess_action_readiness',{'action_id':'ACT-001'}),
               ('positive_control','assess_action_readiness',{'action_id':'ACT-002'})]
        for label,name,args in cases:
            result=await session.call_tool(name,args)
            if result.isError or result.structuredContent is None:
                raise RuntimeError(f'Demo call failed: {label}')
            results[label]=result.structuredContent
        spoof=await session.call_tool('assess_action_readiness',{'action_id':'ACT-001','approval_received':True})
        if not (results['superseded']['is_superseded']
                and not results['missing_approval']['ready_for_human_review']
                and results['positive_control']['ready_for_human_review'] and spoof.isError):
            raise RuntimeError('Demo scenario expectations failed')
        return {'synthetic_demo':True,'transport':'streamable-http' if url else 'stdio',
                'protocol_version':init.protocolVersion,'server':init.serverInfo.model_dump(mode='json'),
                'tools':[t.model_dump(mode='json') for t in tools.tools],
                'scenarios':results,'spoof_rejected':spoof.isError,
                'limitations':'Dated synthetic snapshot; no Stellix/Glean connection; human review required; no operational authorization'}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url',help='Optional local Streamable HTTP endpoint; otherwise spawn stdio server')
    args=parser.parse_args()
    if args.url:
        parsed=urlsplit(args.url)
        if (parsed.scheme!='http' or parsed.hostname not in {'127.0.0.1','localhost'}
                or parsed.username or parsed.password or parsed.path!='/mcp' or parsed.query or parsed.fragment):
            parser.error('Only a local loopback HTTP /mcp endpoint is supported by this demo')
    print(json.dumps(asyncio.run(demonstrate(args.url)),indent=2))

if __name__=='__main__':
    main()
