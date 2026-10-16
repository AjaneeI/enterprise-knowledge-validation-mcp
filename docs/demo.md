# Demonstrate the evidence checks

All examples use fictional records and the fixed October 16, 2026 snapshot. They are not industrial instructions.

## Three-minute walkthrough

1. Run `uv run --no-sync knowledge-ops-demo`. It launches a local stdio server and uses the official MCP client.
2. Show `scenarios.superseded`: `SOP-104@1.0` is superseded; the verified current record is `SOP-104@2.0`. Resolve its citations in the JSON fixture.
3. Show `scenarios.missing_approval`: `ACT-001` is blocked by missing stored approval evidence. A caller's assertion cannot replace that record.
4. Show `scenarios.positive_control`: `ACT-002` is eligible for human review, while `execution_authorized` remains false and `human_review_required` remains true.
5. Show `spoof_rejected=true`: the server rejects an extra `approval_received` argument.
6. End with the boundaries: synthetic data, frozen time, editable trust root, no enterprise identity and no Glean connection.

The [stdio transcript](../evidence/demo-stdio.json) and [HTTP transcript](../evidence/demo-http.json) are actual SDK responses. The illustration is a labeled summary of selected fields, not a screenshot of a user interface.

## Streamable HTTP

Run `uv run --no-sync knowledge-ops-mcp --port 8765` in one terminal, then `uv run --no-sync knowledge-ops-demo --url http://127.0.0.1:8765/mcp` in another. Pick another port if occupied. The client accepts loopback HTTP `/mcp` URLs only. Ctrl-C stops the server.

## Interactive inspection

Optional external tooling: Node.js 22.19+ and MCP Inspector 2.5.0. Start the HTTP server first, then:

```bash
HOST=127.0.0.1 npx --yes @modelcontextprotocol/inspector@2.5.0 --web --server-url http://127.0.0.1:8765/mcp --transport http
```

Use the printed local URL and its per-launch token locally. Do not disable Inspector authentication or save its token in shared artifacts. Discover the two tools and enter the arguments shown in README. Inspector is optional; it is not an application dependency or required for the verified Python path. Its npm transitive dependency tree is not pinned by this project. Stop Inspector with Ctrl-C.

## Offline fallback

After installation, `.venv/bin/knowledge-ops-demo` requires no external service. Alternatively inspect the saved JSON transcripts. A transcript is evidence of its recorded run, not a fresh execution.

## Resolve a citation

```bash
uv run --no-sync python -c 'from src.logic import resolve_evidence; print(resolve_evidence("synthetic://procedures/SOP-104/2.0"))'
```
