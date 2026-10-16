"""Catches unsafe claims and the missing single-identifier tool contracts."""
import pytest
from src import logic

@pytest.mark.parametrize('identifier,status,version,current', [
    ('SOP-104@1.0', 'superseded', '1.0', 'SOP-104@2.0'),
    ('SOP-104@2.0', 'current', '2.0', 'SOP-104@2.0'),
    ('SOP-104', 'current', '2.0', 'SOP-104@2.0'),
    ('SOP-205@1.0', 'under_review', '1.0', None),
])
def test_status_contract(identifier,status,version,current):
    result = logic.check_procedure_status(identifier)
    assert result['status'] == status
    assert result['version'] == version
    assert result['is_superseded'] == (status == 'superseded')
    assert result['current_approved_version'] == current
    assert result['evidence_refs']
    for ref in result['evidence_refs']:
        assert logic.resolve_evidence(ref)


def test_missing_procedure_is_unknown():
    result = logic.check_procedure_status('SOP-999')
    assert result['found'] is False
    assert result['decision'] == 'unknown'
    assert result['evidence_refs'] == []
    assert result['warnings']

@pytest.mark.parametrize('identifier', ['', '../SOP-104', 'SOP-104@x', 'sop-104', 'SOP-104\n', 104])
def test_malformed_procedure_is_rejected(identifier):
    with pytest.raises(ValueError):
        logic.check_procedure_status(identifier)

@pytest.mark.parametrize('action,approval,ready', [
    ('ACT-001','missing',False),
    ('ACT-002','present',True),
    ('ACT-003','conflicting',False),
    ('ACT-004','insufficient',False),
    ('ACT-005','present',False),
])
def test_readiness_uses_stored_evidence(action,approval,ready):
    result = logic.assess_action_readiness(action)
    assert result['approval_evidence_status'] == approval
    assert result['ready_for_human_review'] is ready
    assert result['human_review_required'] is True
    assert result['execution_authorized'] is False
    assert bool(result['blockers']) is (not ready)
    for ref in result['evidence_refs']:
        assert logic.resolve_evidence(ref)


def test_missing_action_fails_closed():
    result = logic.assess_action_readiness('ACT-999')
    assert result['found'] is False
    assert not result['ready_for_human_review']
    assert result['blockers']
    assert result['evidence_refs'] == []

@pytest.mark.parametrize('identifier', ['', '../ACT-001', 'act-001', 'ACT-001\n', True])
def test_malformed_action_rejected(identifier):
    with pytest.raises(ValueError):
        logic.assess_action_readiness(identifier)


def test_python_caller_cannot_supply_approval():
    with pytest.raises(TypeError):
        logic.assess_action_readiness('ACT-001', approval_received=True)
