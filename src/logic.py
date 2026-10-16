"""Deterministic, read-only assessments over a dated synthetic evidence snapshot."""
import re
import json
from pathlib import Path
from pydantic import ValidationError
from .models import ProcedureStatus, Readiness, Store

DATA_PATH = Path(__file__).resolve().parent / 'data' / 'records.json'
UNAVAILABLE = 'Synthetic evidence unavailable or invalid; human review required'

class StoreUnavailable(ValueError):
    pass

def _unique_json_fields(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate JSON field')
        result[key] = value
    return result

def load_store() -> Store:
    try:
        raw = DATA_PATH.read_text(encoding='utf-8')
        # Validate JSON object keys before Pydantic can collapse duplicates.
        json.loads(raw, object_pairs_hook=_unique_json_fields)
        return Store.model_validate_json(raw)
    except (OSError, ValueError, ValidationError):
        raise StoreUnavailable(UNAVAILABLE) from None

def _identifier(value, pattern):
    if not isinstance(value, str) or not re.fullmatch(pattern, value):
        raise ValueError('Malformed identifier')
    return value

def _procedure_input(procedure_id, version=None):
    _identifier(procedure_id, r'SOP-[0-9]{3}(?:@[0-9]+\.[0-9]+)?')
    if len(procedure_id) > 40:
        raise ValueError('Malformed identifier')
    if version is not None:
        _identifier(version, r'[0-9]+\.[0-9]+')
        if '@' in procedure_id or len(version) > 20:
            raise ValueError('Malformed version')
        return f'{procedure_id}@{version}'
    return procedure_id

def _procedure_uri(procedure):
    return f'synthetic://procedures/{procedure.id}/{procedure.version}'

def _status(store, identifier):
    family, _, version = identifier.partition('@')
    family_records = [p for p in store.procedures if p.id == family]
    current = next((p for p in family_records if p.status == 'current' and p.approved
                    and p.effective_date <= store.evaluation_time.date()), None)
    record = next((p for p in family_records if p.version == version), None) if version else current
    if record is None and not version and len(family_records) == 1:
        record = family_records[0]
    if record is None:
        return ProcedureStatus(procedure_id=identifier, found=False, status='unknown',
                               decision='unknown', warnings=['Procedure/version not found or ambiguous'])
    warnings = []
    eligible = record.status == 'current' and record.approved and record.effective_date <= store.evaluation_time.date()
    refs = [_procedure_uri(record)]
    if current and current.ref != record.ref:
        refs.append(_procedure_uri(current))
    if record.status == 'superseded':
        if current is None or record.superseded_by != current.ref:
            warnings.append('Supersession link does not identify the current approved version')
    if not record.approved:
        warnings.append('Procedure approval is absent')
    if record.effective_date > store.evaluation_time.date():
        warnings.append('Procedure is not effective at the synthetic evaluation time')
    return ProcedureStatus(procedure_id=identifier, found=True, status=record.status,
                           version=record.version, is_superseded=record.status == 'superseded',
                           current_approved_version=current.ref if current else None,
                           evidence_refs=refs, warnings=warnings,
                           decision='eligible_for_review' if eligible else 'hold_for_review')

def check_procedure_status(procedure_id: str, version: str | None = None) -> dict:
    """Version is retained only for legacy Python helpers, not the MCP schema."""
    identifier = _procedure_input(procedure_id, version)
    try:
        result = _status(load_store(), identifier)
    except StoreUnavailable:
        result = ProcedureStatus(procedure_id=identifier, found=False, status='unavailable',
                                 decision='unknown', warnings=[UNAVAILABLE])
    return result.model_dump(mode='json')

def assess_action_readiness(action_id: str) -> dict:
    _identifier(action_id, r'ACT-[0-9]{3}')
    try:
        store = load_store()
    except StoreUnavailable:
        return Readiness(action_id=action_id, found=False, approval_evidence_status='unavailable',
                         blockers=[UNAVAILABLE]).model_dump(mode='json')
    action = next((a for a in store.actions if a.id == action_id), None)
    if action is None:
        return Readiness(action_id=action_id, found=False, approval_evidence_status='missing',
                         blockers=['Action not found']).model_dump(mode='json')
    status = _status(store, action.procedure_ref)
    blockers = []
    if status.decision != 'eligible_for_review':
        blockers.append('Procedure not verified as current, approved and effective')
    if action.requested_at > store.evaluation_time:
        blockers.append('Action request is dated after the synthetic evaluation time')
    refs = [f'synthetic://actions/{action.id}', *status.evidence_refs]
    evidence = {e.id: e for e in store.evidence}
    proof_ok = True
    required = [(action.owner_confirmation_id, 'owner_confirmation')]
    required += [(e, 'supporting') for e in action.required_evidence_ids]
    for evidence_id, kind in required:
        proof = evidence.get(evidence_id)
        if proof:
            refs.append(f'synthetic://evidence/{proof.id}')
        if not proof or not (proof.action_id == action.id and proof.procedure_ref == action.procedure_ref
                             and proof.scope == action.scope and proof.kind == kind
                             and action.requested_at <= proof.recorded_at <= store.evaluation_time):
            proof_ok = False
            blockers.append(f'Missing or misbound {kind} evidence')
    approvals = [a for a in store.approvals if a.action_id == action.id]
    refs += [f'synthetic://approvals/{a.id}' for a in approvals]
    if not approvals:
        approval_status = 'missing'
    elif any(a.decision == 'rejected' for a in approvals):
        approval_status = 'conflicting'
    elif all(a.procedure_ref == action.procedure_ref and a.scope == action.scope
             and a.approver_role == action.required_approver_role
             and action.requested_at <= a.recorded_at <= store.evaluation_time < a.expires_at
             for a in approvals):
        approval_status = 'present'
    else:
        approval_status = 'insufficient'
    if approval_status != 'present':
        blockers.append(f'Human approval evidence {approval_status}')
    ready = not blockers
    return Readiness(action_id=action_id, found=True, relevant_procedure=action.procedure_ref,
                     procedure_status=status, approval_evidence_status=approval_status,
                     evidence_complete=proof_ok and approval_status == 'present', blockers=blockers,
                     evidence_refs=list(dict.fromkeys(refs)),
                     readiness='eligible_for_human_review' if ready else 'blocked',
                     ready_for_human_review=ready, evaluation_time=store.evaluation_time.isoformat()
                     ).model_dump(mode='json')

def resolve_evidence(reference: str) -> dict | None:
    """Resolve documented synthetic citation IDs; never fetch arbitrary URLs/files."""
    store = load_store()
    records = {_procedure_uri(p): p for p in store.procedures}
    for kind, items in [('actions',store.actions), ('evidence',store.evidence), ('approvals',store.approvals)]:
        records.update({f'synthetic://{kind}/{r.id}': r for r in items})
    record = records.get(reference)
    return record.model_dump(mode='json') if record else None

def get_record(procedure_id: str, version: str):
    identifier = _procedure_input(procedure_id, version)
    return next((p.model_dump(mode='json') for p in load_store().procedures if p.ref == identifier), None)

def compare_procedure_versions(procedure_id: str, old_version: str, new_version: str) -> dict:
    old, new = get_record(procedure_id, old_version), get_record(procedure_id, new_version)
    if not old or not new:
        return {'found':False, 'error':'One or both versions missing', 'synthetic_demo':True}
    return {'found':True, 'procedure_id':procedure_id, 'old_version':old_version, 'new_version':new_version,
            'removed_steps':[s for s in old['steps'] if s not in new['steps']],
            'added_steps':[s for s in new['steps'] if s not in old['steps']],
            'new_status':new['status'], 'requires_human_review':True, 'synthetic_demo':True}

def generate_review_brief(procedure_id: str, version: str) -> dict:
    status = check_procedure_status(procedure_id, version)
    record = get_record(procedure_id, version)
    return {'title':f'Procedure review: {procedure_id} v{version}', 'status_check':status,
            'source_ref':f'synthetic://procedures/{procedure_id}/{version}' if record else None,
            'steps_for_review':record['steps'] if record else [],
            'limitations':'Synthetic records; not connected to Stellix or Glean; no operational action authorized',
            'synthetic_demo':True}
