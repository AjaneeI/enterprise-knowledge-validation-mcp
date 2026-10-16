# Deterministic validation rules

These rules describe the implemented synthetic snapshot, not a general enterprise policy. The source of truth is [logic.py](../src/logic.py) and the strict [models](../src/models.py). Evaluation time is stored in the fixture. No current wall-clock or independent identity service is consulted.

## Procedure assessment

`check_procedure_status` accepts a procedure family or an exact `family@version` reference. A current candidate must have `status="current"`, `approved=true` and `effective_date <= evaluation_time.date()`.

An exact version selects that record. A family without a version selects an eligible current record, or the sole family record if only one exists. Missing or ambiguous selection returns `found=false`, `status="unknown"`. A missing/invalid store returns `status="unavailable"` and an unknown decision. A found record is eligible for review only if current, approved and effective; otherwise its decision is `hold_for_review`.

When another eligible current record exists, it is reported as `current_approved_version` and its citation is added. A supersession pointer that does not identify that current record produces a warning; the pointer itself does not confer currentness. Every procedure result requires human review.

## Action-readiness sequence

![Actual action-readiness flow](assets/decision-flow.svg)

1. Validate the `ACT-000`-shaped identifier. The MCP schema also rejects unknown arguments.
2. Load and validate the complete snapshot. Duplicate JSON object fields are rejected before Pydantic validation. Duplicate record IDs, contradictory current supersession and multiple current versions invalidate the store.
3. Find the action. An invalid/unavailable store or a missing action returns a blocked result immediately.
4. Assess the action's exact procedure reference. Add a blocker unless it is current, approved and effective. Add a blocker if the action request is later than evaluation time.
5. Check the owner-confirmation ID and each required supporting ID. Each record must exist and match the action ID, exact procedure, scope and expected kind. Its timestamp must satisfy `requested_at <= recorded_at <= evaluation_time`. Every failure adds a blocker. This pass sets the supporting-proof part of `evidence_complete`.
6. Select all approval records whose `action_id` equals the action. Apply the precedence below and add a blocker unless status is `present`.
7. Set `ready_for_human_review` to whether the blocker list is empty. Return the corresponding readiness, citations and evaluation timestamp.

## Approval precedence

| Condition, in order | Status |
| --- | --- |
| No approvals for the action | `missing` |
| Any selected approval has `decision="rejected"` | `conflicting` |
| Every selected approval matches procedure, scope, required role and time | `present` |
| Any remaining mismatch | `insufficient` |

The time condition is `requested_at <= recorded_at <= evaluation_time < expires_at`. Expiry is exclusive. A rejection takes precedence even when other approval records are positive or its context differs. This conservative rule has no override hierarchy.

`approver_id` must be a nonempty bounded string in the record schema. The algorithm does **not** compare it to an identity provider or verify that a person holds the asserted role. Role matching compares stored strings. Evidence and approval authenticity remain outside this prototype.

`evidence_complete` means all required owner/supporting proof passed and approval status is `present`. It does not include the separate procedure/request-time blockers; inspect the complete blocker list and readiness. A true evidence-complete field alone is not permission to proceed.

## Response invariants and failures

All action results preserve `human_review_required=true` and `execution_authorized=false`, including a positive control. An unavailable store, unknown action or failed evidence check cannot produce execution permission. Strict MCP input errors are protocol errors rather than successful blocked assessments; do not collapse the two outcomes.

References are deduplicated record IDs in a `synthetic://` namespace. The server does not fetch URLs from the fixture. An evidence record can be cited while also failing its binding check: citation presence is not proof that the record passed.

[Protocol tests](../tests/test_protocol.py), [reliability tests](../tests/test_reliability.py) and [domain tests](../tests/test_logic.py) exercise these boundaries. There is no implemented facility compatibility rule, cross-engagement reuse policy, live source ACL check or operational executor.
