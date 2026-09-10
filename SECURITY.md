# Security Policy

**Status:** Publication candidate
**Applies to:** PROJECT ACCORD public claim, challenge, and evidence surfaces

This policy is intentionally scoped to material published in the PROJECT ACCORD public
repository. It does not disclose or document the private reference implementation.

## What should be treated as a security-relevant report?

Examples include:

- a way to make the public challenge harness accept malformed or ambiguous evidence
  records as valid;
- parser differential, duplicate-key, canonicalization, or digest inconsistencies;
- a path by which public evidence tooling creates a stronger claim than the underlying
  evidence supports;
- claim-boundary behavior that silently promotes authorization into execution or effect;
- a disclosure that reveals private implementation detail not required for public
  falsification;
- accidental publication of secrets, credentials, personal data, private repository
  metadata, private tests, internal red-team material, or proprietary implementation
  identifiers;
- a reproducible counterexample that appears to falsify a published ACCORD claim within
  its declared scope.

A disagreement with a research assumption is welcome, but it is not automatically a
security vulnerability. Claim counterexamples should be evaluated against the public
falsification contract.

## Public challenge versus confidential security report

Use the public challenge mechanism for non-sensitive counterexamples that can be safely
shared.

Do **not** publish a report as a public issue, fixture, pull request, discussion, or other
public artifact if it contains:

- credentials or secrets;
- personal or confidential third-party data;
- non-public repository material;
- an exploit that would create avoidable harm if disclosed before review; or
- implementation details that were obtained through unauthorized access.

## Confidential reporting channel

A verified confidential reporting channel is a **publication requirement** and has not
yet been declared by this candidate document.

Before PROJECT ACCORD is made public, the maintainers must verify and publish one
confidential reporting path, preferably repository-native private vulnerability
reporting where available.

Until that gate is closed, this candidate must not be represented as having a complete
public vulnerability-reporting process.

## Scope and authority

A report does not gain authority merely because it is submitted, and acceptance by a
mechanical harness does not establish truth.

Likewise, a successful public self-check verifies only the sanitized artifact's declared
integrity properties. It does not authenticate the private reference implementation or
prove a public claim.

## Coordinated disclosure expectations

For a confidential security report, please preserve enough information to reproduce and
evaluate the issue while minimizing unrelated data.

Useful material can include:

- affected public file and revision;
- the public claim or evidence record involved;
- minimal reproduction steps;
- expected versus observed behavior;
- a minimized fixture or artifact;
- integrity hashes where relevant; and
- impact within the stated public claim boundary.

Do not send unrelated private datasets or bulk exports when a minimized reproducer is
sufficient.

## Out of scope

The public repository does not authorize:

- access to private PROJECT ACCORD repositories or infrastructure;
- credential attacks;
- social engineering;
- denial-of-service activity;
- destructive testing;
- privacy-invasive collection; or
- testing against third-party systems without authorization.

Publication of a challenge contract is not authorization to attack systems outside the
published public artifacts.

## No overclaim

Resolution of a reported issue does not by itself establish formal verification,
production readiness, universal safety, or absence of other defects.
