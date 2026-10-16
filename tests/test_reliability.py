"""Mutate stored evidence to catch unsafe approvals, corruption and stale links."""
import json
import pytest
from src import logic

@pytest.fixture
def store(tmp_path,monkeypatch):
    data=json.loads(logic.DATA_PATH.read_text())
    path=tmp_path/'records.json'
    def save():
        path.write_text(json.dumps(data))
    save()
    monkeypatch.setattr(logic,'DATA_PATH',path)
    return data,save,path

@pytest.mark.parametrize('field,value',[
    ('procedure_ref','SOP-104@1.0'), ('scope','another-scope'),
    ('approver_role','Unqualified role'),
    ('recorded_at','2026-10-16T08:00:00Z'),
    ('recorded_at','2026-10-16T13:00:00Z'),
    ('expires_at','2026-10-16T12:00:00Z'),
    ('expires_at','2026-10-15T12:00:00Z'),
    ('action_id','ACT-001'),
])
def test_misbound_or_out_of_window_approval_never_qualifies(store,field,value):
    data,save,_=store
    data['approvals'][0][field]=value
    save()
    result=logic.assess_action_readiness('ACT-002')
    assert not result['ready_for_human_review']
    assert result['approval_evidence_status'] in {'missing','insufficient'}
    assert result['execution_authorized'] is False

@pytest.mark.parametrize('field,value',[
    ('action_id','ACT-001'),('procedure_ref','SOP-104@1.0'),('scope','wrong'),
    ('kind','supporting'),('recorded_at','2026-10-16T13:00:00Z'),
    ('recorded_at','2026-10-16T08:00:00Z'),
])
def test_misbound_owner_evidence_blocks_readiness(store,field,value):
    data,save,_=store
    data['evidence'][2][field]=value
    save()
    result=logic.assess_action_readiness('ACT-002')
    assert result['approval_evidence_status']=='present'
    assert not result['evidence_complete']
    assert not result['ready_for_human_review']

@pytest.mark.parametrize('missing',['owner','supporting'])
def test_missing_required_proof_blocks_and_never_fabricates_citation(store,missing):
    data,save,_=store
    eid='EVD-003' if missing=='owner' else 'EVD-004'
    data['evidence']=[e for e in data['evidence'] if e['id']!=eid]
    save()
    result=logic.assess_action_readiness('ACT-002')
    assert not result['evidence_complete']
    assert not result['ready_for_human_review']
    assert f'synthetic://evidence/{eid}' not in result['evidence_refs']

@pytest.mark.parametrize('kind',['procedures','actions','approvals','evidence'])
def test_duplicate_ids_make_store_unavailable(store,kind):
    data,save,_=store
    data[kind].append(data[kind][0].copy())
    save()
    result=logic.assess_action_readiness('ACT-002')
    assert result['approval_evidence_status']=='unavailable'
    assert not result['ready_for_human_review']
    assert result['evidence_refs']==[]

@pytest.mark.parametrize('kind,field',[
    ('approvals','approver_id'),('evidence','recorded_by'),('actions','scope'),
])
def test_whitespace_identity_is_not_evidence(store,kind,field):
    data,save,_=store
    # Select ACT-002's first proof/approval/action.
    row=next(r for r in data[kind] if r.get('action_id',r.get('id'))=='ACT-002')
    row[field]='   '
    save()
    result=logic.assess_action_readiness('ACT-002')
    assert result['approval_evidence_status']=='unavailable'
    assert not result['ready_for_human_review']

@pytest.mark.parametrize('mode',['missing','invalid_json','invalid_schema','naive_time','string_boolean'])
def test_unreadable_or_invalid_store_is_controlled_failure(store,mode):
    data,save,path=store
    if mode=='missing':
        path.unlink()
    elif mode=='invalid_json':
        path.write_text('{broken secret-path-marker')
    else:
        if mode=='invalid_schema': data['unexpected']='secret-path-marker'
        if mode=='naive_time': data['evaluation_time']='2026-10-16T12:00:00'
        if mode=='string_boolean': data['procedures'][1]['approved']='true'
        save()
    status=logic.check_procedure_status('SOP-104')
    readiness=logic.assess_action_readiness('ACT-002')
    assert status['status']=='unavailable'
    assert readiness['approval_evidence_status']=='unavailable'
    assert readiness['blockers']==[logic.UNAVAILABLE]
    assert not readiness['ready_for_human_review']
    assert 'secret-path-marker' not in str(readiness)
    assert str(path) not in str(readiness)


def test_ambiguous_current_versions_fail_closed(store):
    data,save,_=store
    data['procedures'][0]['status']='current'
    save()
    assert logic.check_procedure_status('SOP-104')['status']=='unavailable'


def test_broken_supersession_link_warns_without_inventing_evidence(store):
    data,save,_=store
    data['procedures'][0]['superseded_by']='SOP-999@9.0'
    save()
    result=logic.check_procedure_status('SOP-104@1.0')
    assert result['warnings']
    assert result['current_approved_version']=='SOP-104@2.0'
    assert all('SOP-999' not in r for r in result['evidence_refs'])


def test_future_procedure_never_counts_as_current_approved(store):
    data,save,_=store
    data['procedures'][1]['effective_date']='2026-11-01'
    save()
    result=logic.check_procedure_status('SOP-104@2.0')
    assert result['decision']=='hold_for_review'
    assert result['current_approved_version'] is None
    assert not logic.assess_action_readiness('ACT-002')['ready_for_human_review']


def test_unknown_reference_never_resolves_to_a_fabricated_record():
    assert logic.resolve_evidence('synthetic://approvals/APR-999') is None
    assert logic.resolve_evidence('file:///etc/passwd') is None

@pytest.mark.parametrize('target',['SOP-104@1.0','SOP-999@9.0','SOP-104@2.0'])
def test_current_procedure_with_supersession_pointer_is_not_ready(store,target):
    data,save,_=store
    data['procedures'][1]['superseded_by']=target
    save()
    assert logic.check_procedure_status('SOP-104@2.0')['decision']!='eligible_for_review'
    result=logic.assess_action_readiness('ACT-002')
    assert not result['ready_for_human_review']
    assert result['blockers']


def test_duplicate_json_decisions_do_not_erase_rejection(store):
    _,_,path=store
    raw=path.read_text()
    assert '"decision": "approved"' in raw
    path.write_text(raw.replace('"decision": "approved"','"decision": "rejected", "decision": "approved"',1))
    result=logic.assess_action_readiness('ACT-002')
    assert result['approval_evidence_status']=='unavailable'
    assert not result['ready_for_human_review']
    assert result['evidence_refs']==[]
