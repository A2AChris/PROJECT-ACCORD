# PROJECT ACCORD — Public Challenge Adjudication Contract

**Status:** Public-surface challenge adjudication contract
**Revision:** `v0.3`

## Purpose

The challenge harness establishes mechanical well-formedness only. The lifecycle contract
establishes public receipt and process visibility. This contract defines the separate
governance step for a completed substantive disposition.

It does not turn automation, a maintainer, or a reviewer into a truth oracle.

## Separation rule

The following remain distinct:

1. submission;
2. public receipt;
3. mechanical validity;
4. substantive review;
5. final adjudication; and
6. claim-state consequence.

`WELL_FORMED_CHALLENGE_SUBMISSION` is not admissibility, confirmation, falsification,
verification, safety, or pass.

## Decision authority versus review provenance

Review provenance and decision authority are different assertions.

A reviewer may supply analysis without possessing authority to change public claim state.
The project maintainer may possess publication authority without that fact creating an
independence claim.

For revision `v0.3`, the only decision-authority class permitted to register a final
public adjudication is:

- `PROJECT_MAINTAINER`

Every final record must identify the public decision actor, the authority basis, and the
decision timestamp.

The machine-checkable authority basis for this contract revision is exactly:

```text
challenge/ADJUDICATION-CONTRACT.md#decision-authority-versus-review-provenance
```

This prevents an arbitrary non-empty string from masquerading as a public authority
basis. The actor field identifies the project-asserted decision actor; it is not by itself
a cryptographic identity proof.

This is intentionally centralized and explicit. PROJECT ACCORD does not claim an
independent tribunal.

## Review classes

Every final record declares one review class:

- `PROJECT_ADJUDICATED`
- `EXTERNAL_INDEPENDENT`
- `MULTI_PARTY_REVIEWED`

`EXTERNAL_INDEPENDENT` requires at least one identified external reviewer and an explicit
public independence basis.

`MULTI_PARTY_REVIEWED` requires at least two distinct reviewers. It does not itself claim
independence.

Reviewer identifiers, relationship labels, and an independence basis are public
provenance assertions. They are not automatically proof of identity or independence and
must not be promoted into a stronger evidence claim without separate support.

Review class is provenance only and does not raise the implementation evidence or
reproduction level.

## Reviewer positions and dissent preservation

Each reviewer record must preserve that reviewer's own substantive position, rationale,
and any public evidence references used for that position.

Allowed reviewer positions are the five final disposition labels plus `ABSTAIN`.
`ABSTAIN` means the reviewer supplied no substantive disposition and is not treated as a
dissenting position.

A reviewer position is **not** decision authority. It does not itself change claim state,
confirm a falsification, or bind the project maintainer. Final publication authority
remains the `PROJECT_MAINTAINER` authority defined above.

If a non-abstaining reviewer position differs from the final disposition, the final
record must preserve that disagreement and include a non-empty maintainer response bound
to that exact reviewer identifier. Every dissenting reviewer must have exactly one such
response, and a response must not be recorded for an aligned or abstaining reviewer.

This means an adjudication may still end with a maintainer disposition that differs from
an independent reviewer's position, but the public record must not collapse or erase the
dissent while continuing to advertise the external review provenance.

Reviewer positions use the same challenge-type boundary as final dispositions:
`CONFIRMED_FALSIFICATION` is meaningful only for a `REGISTERED_FALSIFICATION`, and
`CONFIRMED_CONTRACT_GAP` only for a `NOVEL_FALSIFICATION_HYPOTHESIS`.

## Substantive dispositions

Completed adjudications use one of:

- `CONFIRMED_FALSIFICATION`
- `CONFIRMED_CONTRACT_GAP`
- `REJECTED_OUT_OF_SCOPE`
- `INSUFFICIENT_EVIDENCE`
- `NOT_CONFIRMED`

`CONFIRMED_CONTRACT_GAP` applies only to a `NOVEL_FALSIFICATION_HYPOTHESIS`: the public
claim is alleged to be contradicted in a way the registered falsification IDs cannot
faithfully express, and that incompleteness is confirmed.

## Claim-state consequence rule

`CONFIRMED_FALSIFICATION` and `CONFIRMED_CONTRACT_GAP` require exactly one public claim
consequence:

- `CLAIM_SUSPENDED`
- `CLAIM_WITHDRAWN`
- `CLAIM_SUPERSEDED`

The affected revision must not remain `PUBLISHED`.

For `CLAIM_SUPERSEDED`, the replacement revision must be named and publicly registered.

A non-confirmed disposition must not carry a claim consequence.

## Public versus confidential challenge material

Every final record declares challenge visibility:

- `PUBLIC`
- `CONFIDENTIAL_SECURITY`

A `PUBLIC` adjudication must bind to a public receipt and public locator.

A `CONFIDENTIAL_SECURITY` adjudication may bind only to a canonical digest and a
minimized public rationale. Sensitive source material is not made public merely to
support governance bookkeeping.

## Final-decision identity and correction

Adjudication IDs are globally unique in the public registry.

For one exact adjudication binding there may be only one active terminal final decision.

A later correction must not delete or silently rewrite the earlier decision. It creates a
new adjudication record with `supersedes` pointing to the previous adjudication ID.

Supersession must preserve the exact challenge and claim binding. Forked or cyclic
supersession is invalid.

The active final decision is the terminal record in the supersession chain.

A claim revision that was suspended, withdrawn, or superseded after a confirmed
falsification is not silently restored by deleting history. Any later publication uses an
explicit public revision/state transition.

## Decision detail requirements

`CONFIRMED_FALSIFICATION` requires public evidence references and falsification analysis.

`CONFIRMED_CONTRACT_GAP` requires public evidence references and analysis of why the
registered falsification surface was insufficient.

`REJECTED_OUT_OF_SCOPE` requires public rule references.

`INSUFFICIENT_EVIDENCE` requires a missing-evidence statement.

`NOT_CONFIRMED` requires falsification analysis.

Any reviewer/final-disposition divergence additionally requires the reviewer-specific
dissent response described above.

None of these dispositions may be represented as proof of universal correctness, safety,
or absence of unknown defects.

## No evidence inheritance

Adjudication does not create implementation evidence for unrelated claims.

A rejected or unconfirmed challenge does not raise R0/R1/R2.

## Disclosure boundary

Records use only the public semantic material needed to explain the disposition. They do
not disclose private repositories, commits, CI/job identifiers, private tests, private
red-team material, private architecture, or private identity representation merely to
justify a decision.

## Machine-checkable governance

`adjudication.py` validates lifecycle binding, authority/provenance structure, reviewer
position preservation, reviewer-specific dissent responses, adjudication identity,
supersession, conflict freedom, and claim consequences.

It does not decide whether the substantive challenge is true and performs no private
reference verification.
