"""Validated synthetic records and public response contracts."""
from datetime import date
from typing import Annotated, Literal
from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, model_validator

ProcedureId = Annotated[str, Field(strict=True, pattern=r'^SOP-[0-9]{3}(@[0-9]+\.[0-9]+)?$', max_length=40)]
ProcedureRef = Annotated[str, Field(strict=True, pattern=r'^SOP-[0-9]{3}@[0-9]+\.[0-9]+$', max_length=40)]
ActionId = Annotated[str, Field(strict=True, pattern=r'^ACT-[0-9]{3}$')]
Text = Annotated[str, Field(min_length=1, max_length=200, pattern=r'\S')]

class Record(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)

class Procedure(Record):
    id: Annotated[str, Field(pattern=r'^SOP-[0-9]{3}$')]
    version: Annotated[str, Field(pattern=r'^[0-9]+\.[0-9]+$', max_length=20)]
    status: Literal['current', 'superseded', 'under_review']
    owner: Text
    effective_date: date
    superseded_by: ProcedureRef | None
    steps: list[Text]
    approved: bool

    @property
    def ref(self) -> str:
        return f'{self.id}@{self.version}'

class Action(Record):
    id: ActionId
    procedure_ref: ProcedureRef
    scope: Text
    required_approver_role: Text
    requested_at: AwareDatetime
    owner_confirmation_id: str | None
    required_evidence_ids: list[str] = Field(min_length=1)

class Evidence(Record):
    id: Annotated[str, Field(pattern=r'^EVD-[0-9]{3}$')]
    action_id: ActionId
    procedure_ref: ProcedureRef
    scope: Text
    kind: Literal['owner_confirmation', 'supporting']
    recorded_by: Text
    recorded_at: AwareDatetime
    summary: Text

class Approval(Record):
    id: Annotated[str, Field(pattern=r'^APR-[0-9]{3}$')]
    action_id: ActionId
    procedure_ref: ProcedureRef
    scope: Text
    approver_id: Text
    approver_role: Text
    decision: Literal['approved', 'rejected']
    recorded_at: AwareDatetime
    expires_at: AwareDatetime

class Store(Record):
    schema_version: Literal[1]
    synthetic_demo: Literal[True]
    evaluation_time: AwareDatetime
    procedures: list[Procedure]
    actions: list[Action]
    evidence: list[Evidence]
    approvals: list[Approval]

    @model_validator(mode='after')
    def unambiguous_records(self):
        for records, keys in [
            (self.procedures, [p.ref for p in self.procedures]),
            (self.actions, [a.id for a in self.actions]),
            (self.evidence, [e.id for e in self.evidence]),
            (self.approvals, [a.id for a in self.approvals]),
        ]:
            if len(keys) != len(set(keys)):
                raise ValueError('Duplicate record identifier')
        if any(p.status == 'current' and p.superseded_by is not None for p in self.procedures):
            raise ValueError('Current procedure has contradictory supersession evidence')
        current = [p.id for p in self.procedures if p.status == 'current']
        if len(current) != len(set(current)):
            raise ValueError('Ambiguous current procedure')
        return self

class ProcedureStatus(Record):
    procedure_id: str
    found: bool
    status: Literal['current', 'superseded', 'under_review', 'unknown', 'unavailable']
    version: str | None = None
    is_superseded: bool = False
    current_approved_version: str | None = None
    evidence_refs: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    decision: Literal['eligible_for_review', 'hold_for_review', 'unknown']
    human_review_required: Literal[True] = True
    synthetic_demo: Literal[True] = True

class Readiness(Record):
    action_id: str
    found: bool
    relevant_procedure: str | None = None
    procedure_status: ProcedureStatus | None = None
    approval_evidence_status: Literal['present', 'missing', 'insufficient', 'conflicting', 'unavailable']
    evidence_complete: bool = False
    blockers: list[str] = Field(default_factory=list)
    human_review_required: Literal[True] = True
    evidence_refs: list[str] = Field(default_factory=list)
    readiness: Literal['eligible_for_human_review', 'blocked'] = 'blocked'
    ready_for_human_review: bool = False
    execution_authorized: Literal[False] = False
    synthetic_demo: Literal[True] = True
    evaluation_time: str | None = None
