# PROJECT ACCORD — Public Challenge Adjudication Contract

**Status:** Public-surface challenge adjudication contract  
**Revision:** `v0.1`

## Purpose

The public challenge harness establishes mechanical well-formedness only. This contract
defines the separate public governance step for substantive disposition of a challenge.

It does not turn automation, a maintainer, or a reviewer into a truth oracle. It binds
substantive decisions to public claim semantics and makes the consequences of a confirmed
falsification externally inspectable.

## Separation rule

The following assertion classes are distinct and must not be silently collapsed:

1. a challenge was submitted;
2. a challenge is mechanically well formed;
3. a challenge is under substantive review;
4. a substantive disposition was recorded; and
5. a public claim revision changed publication state as a consequence.

In particular:

> `WELL_FORMED_CHALLENGE_SUBMISSION` is not admissibility, confirmation, falsification,
> verification, safety, or pass.

The existing challenge harness remains mechanically neutral and must continue to emit
`judgment = NOT_PERFORMED`.

## Substantive dispositions

A completed public adjudication uses exactly one of these dispositions:

- `CONFIRMED_FALSIFICATION`
- `REJECTED_OUT_OF_SCOPE`
- `INSUFFICIENT_EVIDENCE`
- `NOT_CONFIRMED`

`UNDER_REVIEW` is a process state, not a completed substantive disposition.

### `CONFIRMED_FALSIFICATION`

The adjudicator concludes that the bound public falsification condition is satisfied for
the bound claim revision.

A confirmed falsification requires public evidence references and a falsification analysis.
It also requires an immediate claim consequence under the rule below.

### `REJECTED_OUT_OF_SCOPE`

The adjudicator concludes that the challenge does not fall within the public subject,
scope, assumptions, or boundary of the bound claim revision.

The record must cite the public rule used for that conclusion. A bare label such as
"out of scope", "inapplicable", or "ambiguous" is insufficient.

### `INSUFFICIENT_EVIDENCE`

The submitted material is insufficient to establish the alleged falsification condition.

The record must identify the material evidence that is missing or unresolved. This
disposition must not be represented as verification of the claim.

### `NOT_CONFIRMED`

The challenge received substantive review, but the admitted public material does not
establish the alleged falsification condition.

The record must explain the falsification analysis. This disposition must not be
represented as verification, proof, or absence of unknown defects.

## Review classification

Every adjudication record declares one review class:

- `PROJECT_ADJUDICATED`
- `EXTERNAL_INDEPENDENT`
- `MULTI_PARTY_REVIEWED`

The review class describes provenance of the public adjudication only. It does not change
the evidence level of the underlying implementation and must not be promoted into a
stronger independence claim.

## Claim-state consequence rule

Public claim publication state is tracked separately from evidence status in
[`../claims/public-claim-state.json`](../claims/public-claim-state.json).

The allowed publication states are:

- `PUBLISHED`
- `SUSPENDED`
- `WITHDRAWN`
- `SUPERSEDED`

Publication state is not a truth value and is not an evidence level.

A `CONFIRMED_FALSIFICATION` must bind to exactly one consequence for the affected claim
revision:

- `CLAIM_SUSPENDED`
- `CLAIM_WITHDRAWN`
- `CLAIM_SUPERSEDED`

The public state registry must reflect that consequence.

The governing invariant is:

> **A confirmed falsification must not coexist with the same affected claim revision
> remaining `PUBLISHED`.**

For `CLAIM_SUPERSEDED`, the replacement revision must be named and must itself have a
public state entry.

A challenge may remain unresolved while substantive review continues. It must not be
closed as confirmed without the corresponding claim-state consequence.

## Decision binding

Every public adjudication record binds to:

- one adjudication ID;
- one canonical SHA-256 of the challenge material;
- one public claim ID;
- one claim revision;
- one published falsification ID;
- one review class;
- one substantive disposition;
- a public rationale and rule/evidence references appropriate to that disposition; and
- when confirmed, one claim consequence.

If a public challenge artifact is retained in this repository, the record may also name
its public path. The canonical SHA-256 remains the binding identifier.

## Founder / maintainer authority boundary

PROJECT ACCORD may currently issue `PROJECT_ADJUDICATED` decisions. That classification
does not claim independence.

Project control over repository maintenance does not authorize silent removal of the
consequence rule. A confirmed falsification recorded under this contract requires the
public claim-state transition defined above.

Rejection remains possible, but it must be represented as a rejection with public
rationale rather than as disappearance of the challenge.

## No evidence inheritance

Adjudication of a challenge does not create implementation evidence for unrelated claims.

Likewise, a rejected or unconfirmed challenge does not raise a claim's R0/R1/R2 evidence
or reproduction level.

## Disclosure boundary

Adjudication records must use only the public semantic surface necessary to evaluate the
challenge.

They must not disclose private repository identifiers, private commits, private CI/job
identifiers, private tests, private red-team material, private architecture, private data
or identity representation, or private implementation mechanisms merely to justify a
decision.

## Machine-checkable governance

[`adjudication.py`](adjudication.py) checks public governance invariants only. It does not
decide whether a challenge is true.

In particular it checks:

- claim/revision/falsification binding against the public revision-state registry;
- consistency between the current claim index and revision-state registry;
- disposition-specific rationale requirements;
- prohibition of a consequence on a non-confirmed disposition; and
- mandatory non-`PUBLISHED` state after a `CONFIRMED_FALSIFICATION`.

The checker intentionally reports no private-reference verification.
