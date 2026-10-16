# Future applications and pilot considerations

Everything in this document is proposed. The implemented example remains two read-only MCP tools over fictional procedure, action, evidence and approval records. It does not diagnose an organization's needs or establish an enterprise rollout plan.

## Contextual knowledge reuse

A useful future question could be: does a previous engagement's knowledge apply to this new situation, and what must a reviewer establish before reuse?

| Potential dimension | Discovery question | Current implementation |
| --- | --- | --- |
| Source authority and revision | Which owner/version is authoritative, and how fresh must it be? | Fixed procedure status and effective date only |
| Facility and system context | Do equipment, software, configuration and operating assumptions match? | No compatibility model or live system connection |
| Permitted reuse | May the source be used in this engagement and by this person? | No source ACL or contractual reuse enforcement |
| Approval scope | Does approval cover the new context, purpose and recipient? | Exact synthetic action/procedure/scope/role/time comparisons only |
| Exceptions and uncertainty | Who resolves missing context or conflicting authority? | Conservative blockers, no override workflow |

A real design would need permission-scoped sources, an agreed applicability model, policy ownership and representative permitted examples. Similar wording across documents would not prove compatibility. The frozen synthetic tests provide no evidence about real plant systems or customer engagements.

## Proposed adoption pilot

1. Select one recurring review task with a workflow owner. Map the current handoff, failure modes and authoritative evidence. Avoid choosing a custom MCP extension before comparing Glean-native verification, confirmation and existing workflow tools.
2. Define what a reviewer needs to see and who resolves a blocker. Keep operational permission in the existing authorized system. Agree on privacy, access, retention and rollback before involving real records.
3. With an authorized test tenant and secured service, test transport, user identity, source permissions and faithful display of blockers. Include denied access, revoked credentials, stale evidence and ambiguous results.
4. Invite a small opt-in cohort through existing enablement channels. Give participants a concrete task, a short explanation of citations and an escalation route. This is employee adoption of a workflow, not a requirement for employees to install an MCP server.
5. Compare against an agreed baseline, collect reasons for confusion or abandonment and decide with the workflow owner whether to adjust, stop or expand.

Potential measures include correct task completion, missed blockers, review effort, successful escalation, repeat use and user-reported usefulness. Choose definitions and acceptable thresholds with stakeholders before collection. No task-time savings, adoption rate or ROI has been measured here.

## Evidence required before broader use

A future pilot would need an approved environment, source/policy owners, verified role entitlements, tenant-supported authentication, least-privilege data access, audit requirements and an incident/failure handoff. An employer or client must authorize its own data and systems. Passing this repository's tests does not supply that permission or establish enterprise security certification.

[Potential Glean connection](glean-integration.md) · [Security boundaries](security.md) · [Implemented validation](validation-rules.md)
