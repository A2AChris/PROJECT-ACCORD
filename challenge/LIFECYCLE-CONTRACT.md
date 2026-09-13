# PROJECT ACCORD — Public Challenge Lifecycle Contract

**Status:** Public-surface challenge lifecycle contract
**Revision:** `v0.1`

## Purpose

This contract defines how a public research challenge becomes externally observable before
substantive adjudication. It exists so that submission, receipt, mechanical validity,
review, adjudication, and claim consequence cannot be silently collapsed.

The lifecycle does not make a submitted challenge true and does not impose a fixed
substantive-decision deadline.

## Canonical public intake

The canonical public intake for a non-sensitive research challenge is a GitHub Issue in
this repository whose title begins with:

```text
[ACCORD CHALLENGE]
```

The issue must identify the public claim and revision and must contain either the
challenge JSON or a stable public locator for it together with its canonical SHA-256.

A public issue is an intake artifact, not a contribution of implementation code and not
a substantive ACCORD judgment.

Security-sensitive material must use the confidential channel in `SECURITY.md` instead
and must not be forced into the public receipt registry.

## Public receipt

The public GitHub issue is itself an externally visible intake artifact. Once PROJECT
ACCORD acknowledges a public intake as mechanically valid or places it under substantive
review, that challenge **must** be represented in `challenge/receipts/index.json` before
a completed substantive disposition may be published for it.

A project decision not to register or review an intake is not an adjudication and must
not be represented as `INVALID_SUBMISSION`, `NOT_CONFIRMED`, or another substantive
disposition. The public issue remains independently observable even before project
acknowledgement.

A receipt records:

- a stable receipt ID;
- the canonical SHA-256 of the challenge material;
- the public intake locator;
- the claim and revision;
- the challenge type;
- the current lifecycle state;
- `received_at`; and
- `last_status_change_at`.

Public receipt means only that the identified submission is publicly observable through
the declared intake surface. It is not admissibility, truth, scope acceptance,
falsification, or verification.

## Challenge types

Two challenge types are recognized.

### `REGISTERED_FALSIFICATION`

The submitter alleges that one already-published falsification ID is satisfied.

### `NOVEL_FALSIFICATION_HYPOTHESIS`

The submitter alleges that the public claim is contradicted in a way not faithfully
expressible by any currently registered falsification ID.

A novel hypothesis must identify:

- the alleged contradiction with the public claim; and
- why no registered falsification ID faithfully captures it.

A novel hypothesis does not bypass the published falsification contract. It attacks the
completeness of that contract itself.

## Lifecycle states

The public lifecycle states are:

- `RECEIVED`
- `MECHANICALLY_VALID`
- `UNDER_REVIEW`
- `COMPLETED`
- `INVALID_SUBMISSION`

These states are process states only.

`MECHANICALLY_VALID` is not substantive admissibility or confirmation.
`UNDER_REVIEW` may remain unresolved while substantive review continues.
`COMPLETED` requires a completed public adjudication record for the receipt.

No fixed adjudication SLA is claimed. Instead, receipt time and last status-change time
remain public so unresolved age is externally observable.

## Deduplication and visibility

The canonical SHA-256 binds challenge content. Multiple intake messages carrying the same
canonical challenge content do not create multiple truths or multiple adjudication
subjects.

The public receipt registry covers public challenges only. Confidential security reports
may be adjudicated with a confidential visibility classification without publishing
sensitive source material.

## Separation invariant

The following must remain distinct:

```text
submission
≠ receipt
≠ mechanical validity
≠ review
≠ final adjudication
≠ claim consequence
```

A public receipt may exist without a final adjudication. A final public adjudication may
not pretend that an unregistered or invisible public challenge was publicly received.
