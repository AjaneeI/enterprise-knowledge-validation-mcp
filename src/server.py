"""Two read-only MCP tools. Local HTTP bind is fixed to loopback."""
import argparse
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError
from mcp.types import ToolAnnotations
from . import logic
from .models import ActionId, ProcedureId, ProcedureStatus, Readiness

ARGUMENTS = {'check_procedure_status':{'procedure_id'}, 'assess_action_readiness':{'action_id'}}

class StrictMCP(FastMCP):
    """FastMCP defaults to ignoring extra arguments; reject them explicitly."""
    async def list_tools(self):
        tools = await super().list_tools()
        for tool in tools:
            tool.inputSchema['additionalProperties'] = False
        return tools

    async def call_tool(self, name, arguments):
        if name in ARGUMENTS and set(arguments) - ARGUMENTS[name]:
            raise ToolError('Unexpected tool arguments; approval claims are not accepted')
        return await super().call_tool(name, arguments)

mcp = StrictMCP('Knowledge Operations Demo',
                instructions='Synthetic-only dated evidence snapshot. Read-only human review support; never permission for operational execution.',
                host='127.0.0.1', port=8765, json_response=True, log_level='WARNING')
READ_ONLY = ToolAnnotations(readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=False)

@mcp.tool(annotations=READ_ONLY)
def check_procedure_status(procedure_id: ProcedureId) -> ProcedureStatus:
    """Check synthetic procedure freshness. Use SOP-104@1.0 for a version or SOP-104 for current. Cite returned evidence and warnings; do not infer operational authorization."""
    return ProcedureStatus.model_validate(logic.check_procedure_status(procedure_id))

@mcp.tool(annotations=READ_ONLY)
def assess_action_readiness(action_id: ActionId) -> Readiness:
    """Assess a stored synthetic action using bound approval and supporting evidence. Missing/conflicting evidence blocks readiness. Human review always required; execution never authorized."""
    return Readiness.model_validate(logic.assess_action_readiness(action_id))

def main():
    parser = argparse.ArgumentParser(description='Local synthetic MCP demo; no operational authorization')
    parser.add_argument('--transport', choices=['streamable-http','stdio'], default='streamable-http')
    parser.add_argument('--port', type=int, default=8765)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error('port must be between 1 and 65535')
    mcp.settings.port = args.port
    mcp.run(transport=args.transport)

if __name__ == '__main__':
    main()
