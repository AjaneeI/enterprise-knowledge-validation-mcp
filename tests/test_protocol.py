"""The app contract over the official MCP client, never direct function calls."""
import jsonschema
import pytest

pytestmark=pytest.mark.anyio

async def test_discovery_exposes_two_validated_read_only_tools(session):
    listed=await session.list_tools()
    tools={t.name:t for t in listed.tools}
    assert set(tools)=={'check_procedure_status','assess_action_readiness'}
    for name, arg in [('check_procedure_status','procedure_id'),('assess_action_readiness','action_id')]:
        tool=tools[name]
        assert set(tool.inputSchema['properties'])=={arg}
        assert tool.inputSchema['required']==[arg]
        assert tool.inputSchema['additionalProperties'] is False
        assert tool.outputSchema
        assert tool.annotations.readOnlyHint
        assert tool.annotations.openWorldHint is False

@pytest.mark.parametrize('name,args,status_key,want',[
    ('check_procedure_status',{'procedure_id':'SOP-104@1.0'},'status','superseded'),
    ('check_procedure_status',{'procedure_id':'SOP-104@2.0'},'status','current'),
    ('check_procedure_status',{'procedure_id':'SOP-999'},'status','unknown'),
    ('assess_action_readiness',{'action_id':'ACT-001'},'approval_evidence_status','missing'),
    ('assess_action_readiness',{'action_id':'ACT-002'},'approval_evidence_status','present'),
    ('assess_action_readiness',{'action_id':'ACT-003'},'approval_evidence_status','conflicting'),
    ('assess_action_readiness',{'action_id':'ACT-999'},'found',False),
])
async def test_invocation_returns_structured_validated_evidence(session,name,args,status_key,want):
    result=await session.call_tool(name,args)
    assert not result.isError
    assert result.structuredContent[status_key]==want
    tool=next(t for t in (await session.list_tools()).tools if t.name==name)
    jsonschema.validate(result.structuredContent,tool.outputSchema)
    assert result.structuredContent['human_review_required'] is True
    if name=='assess_action_readiness':
        assert result.structuredContent['execution_authorized'] is False
    if want=='superseded':
        assert result.structuredContent['current_approved_version']=='SOP-104@2.0'

@pytest.mark.parametrize('name,args',[
    ('check_procedure_status',{}),
    ('check_procedure_status',{'procedure_id':'../../etc/passwd'}),
    ('check_procedure_status',{'procedure_id':104}),
    ('check_procedure_status',{'procedure_id':'SOP-104\n'}),
    ('assess_action_readiness',{'action_id':'ACT-001','approval_received':True}),
    ('assess_action_readiness',{'action_id':'ACT-001','owner_confirmed':True,'evidence_attached':True}),
    ('assess_action_readiness',{'action_id':True}),
    ('assess_action_readiness',{'action_id':'ACT-001\n'}),
    ('no_such_tool',{}),
])
async def test_bad_calls_are_errors_and_session_remains_usable(session,name,args):
    result=await session.call_tool(name,args)
    assert result.isError
    assert 'Traceback' not in str(result.content)
    recovery=await session.call_tool('assess_action_readiness',{'action_id':'ACT-001'})
    assert not recovery.isError
    assert recovery.structuredContent['approval_evidence_status']=='missing'
    assert recovery.structuredContent['ready_for_human_review'] is False

async def test_corrupt_snapshot_fails_closed_through_protocol(corrupt_session):
    result=await corrupt_session.call_tool('assess_action_readiness',{'action_id':'ACT-002'})
    assert not result.isError
    assert result.structuredContent['approval_evidence_status']=='unavailable'
    assert result.structuredContent['ready_for_human_review'] is False
    assert result.structuredContent['evidence_refs']==[]
    status=await corrupt_session.call_tool('check_procedure_status',{'procedure_id':'SOP-104@2.0'})
    assert not status.isError
    assert status.structuredContent['status']=='unavailable'
