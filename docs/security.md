# Security and limitations

This prototype supports review of synthetic evidence. It cannot approve or execute real work.

## Tested boundaries

The two MCP tools read a packaged JSON snapshot. Inputs have strict identifier patterns, no caller-controlled file paths, and no accepted approval/owner/evidence booleans. Unknown arguments are rejected before dispatch. Outputs have Pydantic schemas. All readiness results require human review and explicitly deny execution authorization.

Approval checks bind the stored record to the action ID, exact procedure version, scope, required approver role and evidence window. Owner confirmation and supporting evidence must match the same action, procedure and scope. Missing proof, conflicting decisions, invalid timing, missing records and invalid datasets block readiness. Duplicate record IDs and multiple current procedure versions invalidate the snapshot. Each returned citation identifies a real record in that loaded snapshot.

The standalone HTTP server binds only 127.0.0.1; the CLI offers no public host option. Stdio is available for an offline demonstration. Protocol tests exercise errors and recovery through the official SDK. Read-only annotations describe behavior; they are not access controls.

## Trust model and gaps

The JSON file is the trust root. It is editable by whoever controls this local project. Approval names and roles are synthetic assertions, with no identity provider, digital signature, role registry, revocation service or protected audit log. A malicious fixture editor can forge a consistent approval. The server checks internal consistency, not independent authenticity.

Time is deliberately frozen at the fixture evaluation timestamp. The prototype has no live authorization, user permissions, tenant separation, source ACL enforcement, TLS, rate limits or authenticated HTTP access. Loopback still permits access by other local processes. Do not expose it through a public address, tunnel or reverse proxy, and do not load real internal records.

The server does not consume natural-language instructions from evidence, fetch cited URLs or call a model. This limits the local demonstration's instruction attack surface. It does not prove that a future Glean/model workflow resists prompt injection or interprets returned blockers correctly. A server-name check is a collision safeguard, not proof of identity.

The corpus is small and hand-authored. Procedure currentness and approval policy are simplified. A broken supersession pointer produces a warning and separately reports a verified current record if present. A single rejected approval conservatively blocks the action; no override hierarchy is implemented. One invalid record blocks the entire dataset rather than trusting a partial load. There is no approval-reversal or version-history workflow.

## Before any authorized pilot

Agree on a real authoritative evidence system and policy owner. Validate record provenance, role entitlement, revocation, timestamps and freshness with that owner. Implement authenticated, permission-scoped data access, transport security, audit retention, user identity mapping and scoped error handling. Test revoked/wrong-user credentials, denied sources, cross-user access, expired evidence, model interpretation and failure behavior. Keep the assessment separate from any operational execution system.

No credentials, company documents, paid APIs or tenant access are required to demonstrate this version. Passing tests establish only the local behaviors tested; they do not establish production safety or organizational fit.
