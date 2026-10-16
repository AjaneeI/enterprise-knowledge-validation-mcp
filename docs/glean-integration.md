# Glean integration readiness

Documentation checked October 16, 2026. **Implemented:** local MCP server, validated tools and protocol tests. **Designed:** a possible authenticated remote connection. **Unverified:** Stellix tenant features, administrative access, actual Glean calls and business fit.

## Documented connection requirements

| Area | Official documentation says |
| --- | --- |
| Transport | Remote SSE or Streaming HTTP; this prototype uses Streamable HTTP. |
| Reachability | HTTPS reachable by Glean; private networks need coordinated proxy/allowlist arrangements. |
| Authentication | API key and several OAuth modes, including user/admin and client credentials. Choose the tenant-supported mode. |
| Administration | For custom servers, Admin console → Platform → Tools → Vendor Provided Tools → import. Check the Connectors catalog first. |
| Discovery | Admin connects and imports the exposed tools, then configures availability. |
| Publishing | Enable selected tools for Agents and optionally Glean; apply creator role controls where available. |
| User identity | Discovery authorization does not grant end-user authorization in the per-user OAuth flow. |
| Agent availability | Confirm current agent/channel support and tenant entitlement with the administrator; availability and configuration can change. |

Source: [Glean remote MCP guide](https://docs.glean.com/administration/actions/connect-remote-mcp-servers-to-glean). Its general prerequisites discuss authorization-code OAuth while its authentication table supports other modes; confirm the chosen mode with the tenant administrator rather than assuming one configuration fits every tenant.

## Existing capabilities and the hypothesis

Glean already provides document verification and deprecation, owner review reminders, and verified-result indicators. [How verification works](https://docs.glean.com/user-guide/knowledge/verification/how-verification-works), [Populate content](https://docs.glean.com/get-started/golive/populate-content).

Glean also provides configurable write confirmations; behavior depends on channel and configuration. Read-only lookups do not receive those write confirmations. [Human confirmations](https://docs.glean.com/agents/actions/human-in-the-loop-experience-for-actions).

The proposed extension is a deterministic cross-record rule: bind one action to an exact procedure version, scope, named approval evidence and supporting records, then return explicit blockers and citations. That is the prototype's implemented logic. Whether it adds anything useful beyond a native Glean configuration remains a question for stakeholders. It is not a claim that Glean lacks governance or approval features.

## Proposed secure connection, requiring authorization

An approved Glean host could call an organization-managed HTTPS endpoint in an approved network. That endpoint would authenticate requests and consult a protected evidence system. The two read-only functions would retain their narrow contracts; the host would show evidence, blockers and uncertainty to a human reviewer. A real operational system would retain its own authorization controls. See the [architecture](architecture.md).

Prefer a per-user identity flow when source permissions differ by person. If a service identity is approved, explicitly define its evidence scope and prevent it from granting broader access than intended. Select and test a tenant-supported authentication method with the administrator; no OAuth service, API key validation, identity propagation or ACL enforcement is implemented here.

Before connection: appoint a policy/data owner, approve hosting and network access, define least-privilege access and retention, validate identity mapping, and agree on audit requirements. With an authorized test tenant: initialize, discover both tools, publish only to the test audience, invoke both scenarios, and test denied/revoked credentials, unauthorized users, timeout/error handling and evidence visibility. Confirm that Glean displays blockers faithfully and does not translate readiness into execution permission.

No endpoint has been deployed and no credentials have been requested. Successful local HTTP calls do not prove Glean compatibility. Protocol version, tenant entitlement, feature rollout and approved network/auth configuration still require a permitted tenant test.
