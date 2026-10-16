# Public-release audit

**Source release gates: PASS within the documented review scope. Hosted verification: pending initial publication.** The maintainer confirmed independent AI-assisted provenance and explicitly authorized a new public repository on October 16, 2026. The separate private development repositories remain unchanged.

This audit covers the sanitized source snapshot, its application/tests/fixtures, documentation, SVGs, workflow and fresh evidence. Package payloads were checked separately. There is no inherited Git history to publish. Machine-readable results are in [release-audit.json](../evidence/release-audit.json); verification details are in [verification.md](verification.md).

## Criteria

| Criterion | Result | Evidence and limits |
| --- | --- | --- |
| Secrets and credentials | PASS within inspected scope | Complete text-file pattern scan plus manual source/configuration review found no verified credential. This is not proof against unknown secrets. |
| Historical personal-email exposure | PASS for this snapshot | No Git directory, objects, commits, author/committer metadata or inherited logs are included. Existing private history was not rewritten. |
| Private planning and personal paths | PASS | Private planning documents, meeting material and historical evidence were excluded. Fresh public logs have normalized paths. Copyright attribution intentionally retains the maintainer's name. |
| Synthetic fixture provenance | PASS for documented origin | Original procedure examples came from the maintainer-confirmed ChatGPT-generated prototype; action/proof/approval cases were developed for the same independent demo. All 23 records remain unchanged. No company data source was used by the verified local workflow. |
| Original-source provenance and rights review | PASS within documented scope | Maintainer confirmed independent ChatGPT/Codex-assisted origin; preserved prototype/history and attribution corroborate it. No specific unresolved restriction identified. No legal exclusivity guarantee is made. |
| Project rights policy | PASS | Maintainer-approved All Rights Reserved notice in LICENSE; package metadata uses LicenseRef-All-Rights-Reserved. No open-source license is applied to original material. |
| Third-party license treatment | PASS within source-snapshot scope | Dependencies are not vendored; upstream obligations are preserved and inventoried in THIRD_PARTY_NOTICES.md. No third-party artwork or company logos are included. |
| Dependency advisories | PASS within queried scope | Locked Python packages and setuptools 83.0.0 returned no OSV advisory matches. The build normalization regression fails with 82.0.1 and passes with 83.0.0. Optional Inspector transitive npm packages are outside scope. |
| Source, fixture, schema and test preservation | PASS | All 13 application/fixture/test files match the reviewed source byte-for-byte. Runtime/dev lockfile is unchanged. |
| Local tests and protocol | PASS | 106 tests passed, including 36 actual MCP protocol cases across both transports. |
| Public-source reproducibility | PASS for local candidate | Independent environment install, official-client stdio and HTTP demonstrations, installed-wheel execution outside checkout and source-archive protocol smoke checks passed. |
| Workflow configuration | PASS / hosted execution pending | Three Actions pinned to immutable SHAs; contents read-only; persisted credentials disabled; bounded timeout; no deployment or explicit secrets. Hosted workflow execution is not established by local checks. |
| Documentation and claims | PASS within documented boundaries | Implemented two-tool behavior is separated from proposed enterprise applications; no endorsement, tenant compatibility, production security or workplace benefit is claimed. |
| Visual assets and navigation | PASS | Original self-contained SVGs with accessible descriptions; actual transcript fields are labeled as a summary, not an application screenshot. Local documentation/image links checked; desktop/mobile README preview inspected. |
| Repository-side controls | Hosted verification pending | Public access, clean author metadata, default branch and CI will be checked after creation. Files alone do not enable private reporting or branch protection. |

## Changes from the private engineering package

- Exported only application, fixtures, tests, lock/configuration and selected public technical documentation; did not clone or rewrite private history.
- Excluded private execution plans/ledgers, meeting proposal/PDF and historical evidence that could expose private context.
- Replaced historical logs with fresh verification evidence; normalized local paths in text transcripts.
- Patched the build backend to setuptools 83.0.0 and verified the specific exclusion behavior.
- Applied the requested rights policy and documented provenance and third-party obligations.
- Rebuilt the README with original artwork, actual demonstrations, explicit local verification badges and a clearly unexecuted candidate-CI badge.
- Hardened only the candidate workflow; application behavior, schemas, fixture and test bytes are unchanged.

## Publication authorization and hosted checks

The maintainer confirmed original-source provenance, approved the rights wording and authorized the distinct public destination on October 16, 2026. The frozen candidate manifest was verified before this publication-only documentation update. Application, fixture, test and dependency-lock bytes remain unchanged. Package/license checks are repeated for the affected material.

Initial publication must be followed by actual GitHub Actions execution, anonymous access checks, default-branch verification and inspection of the new repository's tracked files and commit metadata. A passing hosted-CI badge may only follow an observed successful run. See [verification](verification.md) for recorded results.

## Verification boundaries

The application remains a synthetic local demonstration. It has no authenticated HTTP endpoint, independently authenticated evidence, live source ACLs, enterprise tenant connection, production audit service or operational execution permission. Optional external Inspector tooling is not needed for the verified Python path. Results do not establish production security, organizational adoption, ROI or real Glean/Stellix compatibility.

No deployment or paid-service enablement is part of this release. Separate private repositories, pull requests and history are preserved.
