# Visual evidence and design

The visual system was created for this project: navy/indigo backgrounds, cyan evidence accents, violet policy accents and light technical diagrams. A linked-node/check symbol represents evidence converging on an assessment. No employer logo, copied Gateway artwork, external image, custom font binary or frontend is included.

Gateway informed the presentation standard: a clear opening, workflow explanation, genuine evidence, visible trust boundaries and navigation into technical detail. The project uses its own layouts and terminology. The full engineering case study remains in README and supporting documents; the backend has no graphical application.

## Five visual sections

| Visual | Asset | Implementation or evidence source |
| --- | --- | --- |
| Project identity and review path | [hero.svg](assets/hero.svg) | Two tools, synthetic records and human-review boundary |
| Implemented architecture | [architecture.svg](assets/architecture.svg) | [Server](../src/server.py), [models](../src/models.py), [logic](../src/logic.py), packaged fixture |
| Genuine MCP demonstration gallery | [demonstrations.svg](assets/demonstrations.svg) | Selected verbatim fields from the actual [stdio transcript](../evidence/demo-stdio.json) |
| Evidence-validation decision flow | [decision-flow.svg](assets/decision-flow.svg) | `assess_action_readiness`, store validation and response invariants |
| Trust boundaries | [trust-boundary.svg](assets/trust-boundary.svg) | Implemented local controls, editable trust root and unimplemented enterprise controls |

The gallery also provides individual [procedure](assets/demo-procedure.svg) and [readiness](assets/demo-readiness.svg) captures. The three small local-verification badges are separate from the live GitHub workflow badge.

## Demonstration provenance

The MCP demo starts an actual stdio subprocess, initializes the official SDK client, discovers both tools and calls them. The source transcript includes the superseded procedure, missing approval, positive control and rejected extra-argument case.

The captures render selected response fields as text. They are not edited execution results or screenshots of a fictional product UI. The displayed call line combines the actual tool name and argument object used by [the demo](../src/demo.py). See [capture provenance](../evidence/visual-capture-provenance.json) for the transcript SHA-256, selected field names and exact values. All fixture information is synthetic.

Reproduce the underlying execution:

```bash
uv run --no-sync knowledge-ops-demo
```

The capture summary deliberately omits other response fields; use the full JSON to investigate them. A recorded capture demonstrates its recorded run, not a current enterprise result.

## Diagram accuracy

The architecture shows exactly two MCP tools, a packaged evidence source and typed responses. A separate dashed area labels every Glean connection as proposed. It does not depict an authenticated endpoint as implemented.

The decision flow follows input/store validation, action lookup, procedure and request-time checks, owner/supporting proof, stored-approval precedence and blocker aggregation. Invalid stores and unknown actions return early. Stored role equality does not establish identity or entitlement. [Exact rules](validation-rules.md) explain these distinctions.

The trust diagram makes the editable fixture and unauthenticated local transport visible. Human review is a returned requirement; there is no enforced operational approval workflow or executor. Production requirements remain future work.

## Rendering review

Every SVG is rendered for inspection, including the standalone captures and small badges. The review checks typography, padding, contrast, text bounds, actual output fidelity and palette consistency. README is also reviewed through GitHub's Markdown renderer and the public repository page. Detailed local QA outputs remain outside the source snapshot; hosted test/build evidence is available through [Actions](https://github.com/AjaneeI/enterprise-knowledge-validation-mcp/actions/workflows/test.yml).
