# Security

This is a local synthetic demonstration, not an authenticated enterprise service. Do not load internal records or expose the loopback server publicly. See [the trust model](docs/security.md) for controls and limitations.

If you discover a possible issue, avoid including credentials, personal information or real company records in a public discussion. Use an available private reporting channel on GitHub if one is available. Private vulnerability reporting has not yet been verified for this repository. There is no production support or response-time commitment.

The verification workflow uses immutable Action references, read-only contents permissions, credential persistence disabled and a ten-minute timeout. It does not deploy. Repository-side security alerts, private reporting, branch protection and required checks must be configured separately in repository settings; they are not enabled by these files.
