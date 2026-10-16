# Verification record

This document describes the fresh local candidate checks. Results and timestamps are in `evidence/verification.json`; full pytest output is in `evidence/tests.txt`. Remote candidate CI has not run because no public repository exists. The workflow is prepared, and its commands are exercised locally; that is not a claim of hosted CI success.

## Reproduce

```bash
uv sync --locked --extra dev
uv run --no-sync pytest -q
uv run --no-sync pytest tests/test_protocol.py --collect-only -q
uv run --no-sync knowledge-ops-demo
uv build
```

The full suite contains 106 tests, including 36 actual official-client protocol cases over stdio and Streamable HTTP. It covers tool discovery/schemas, input errors, status and readiness, evidence corruption, duplicate JSON fields, contradictory supersession, error recovery and subprocess operation. Test and source bytes are preserved from the reviewed implementation.

## Package checks

A separate environment installs locked runtime dependencies and the non-editable wheel. Running `knowledge-ops-demo` outside the checkout verifies packaged source and fixture loading. The source archive is also extracted separately and its protocol smoke cases run. The final archive additionally runs the complete 106-test suite. `evidence/package-checks.json` records initial payload hashes and smoke checks; `evidence/final-package-checks.json` and `evidence/final-sdist-tests.txt` record final archive verification. The final source archive includes its workflow and security document so README navigation is preserved.

## Demonstrations

- `evidence/demo-stdio.json`: actual official SDK session, two scenarios, positive control and spoof rejection.
- `evidence/demo-http.json`: the same scenarios over loopback Streamable HTTP.
- `evidence/demo-wheel.json`: real installed-wheel client demonstration outside the checkout.

Artwork extracts selected fields from those results and does not represent a separate application UI. Console paths in public text evidence are normalized to `<candidate>` or `<verification-workspace>`; results are unchanged. Raw local logs remain outside the distribution.

## Build advisory

The build backend is pinned to setuptools 83.0.0, replacing 82.0.1 affected by GHSA-h35f-9h28-mq5c / CVE-2026-59890. The installed upstream wheel was inspected for normalized MANIFEST matching, and the Unicode exclusion regression is checked separately. OSV identifies 83.0.0 as fixed; the upstream advisory's patched-version label has lagged that record. [Upstream advisory](https://github.com/pypa/setuptools/security/advisories/GHSA-h35f-9h28-mq5c) · [Upstream normalization fix](https://github.com/pypa/setuptools/commit/dd9f436a36486b4cb8a4c70a2321548b0be09b8f).

## Scope

Passing local tests establish the behavior exercised here, not production safety, model quality, actual source permissions, Glean tenant compatibility, workplace adoption or ROI. Optional Inspector interactive behavior is not re-certified by the Python checks. See [release audit](public-release-audit.md) and [security](security.md).

## Separate read-only review

A separate AI-assisted reviewer found no material privacy, preservation, claims or workflow defect. It identified a minor source-archive navigation omission, corrected by including the workflow and security document in the archive. Final archive payload inspection and the full 106-test suite passed after that packaging correction. See `evidence/independent-review.json`. This review does not establish legal ownership or production security.
