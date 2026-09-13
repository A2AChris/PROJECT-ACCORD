# PROJECT ACCORD — Challenge Surface

This directory contains the clean-room public challenge surface.

It is not a simulator or verifier for the private reference implementation.

## Mechanical submission validation

Run:

```bash
python challenge/harness.py challenge/fixtures/examples/ACCORD-C05-lineage-ambiguity.json
```

A mechanically valid registered-falsification file reports:

```text
status = WELL_FORMED_CHALLENGE_SUBMISSION
scope_position = SUBMITTER_ASSERTED_IN_SCOPE
judgment = NOT_PERFORMED
```

Those lines do not say the counterexample is true, in scope, or claim-falsifying.

See `ATTACK-CONTRACT.md`.

## Public intake and lifecycle

For a non-sensitive research challenge, the canonical public intake is a GitHub Issue in
this repository whose title begins with:

```text
[ACCORD CHALLENGE]
```

Public receipt and pending-state visibility are governed by
`LIFECYCLE-CONTRACT.md` and `receipts/`.

The lifecycle keeps these assertions separate:

```text
submission
≠ receipt
≠ mechanical validity
≠ review
≠ final adjudication
≠ claim consequence
```

There is no fixed substantive-decision SLA. Public receipt timestamps and status-change
timestamps make unresolved age externally observable.

Security-sensitive reports use the confidential path in `../SECURITY.md` instead.

## Novel falsification hypotheses

A submitter who identifies a plausible contradiction to a public claim that cannot be
faithfully expressed by any existing falsification ID may submit a
`NOVEL_FALSIFICATION_HYPOTHESIS` through the public lifecycle intake.

That path does not bypass the falsification contract. It challenges the completeness of
the published falsification surface itself.

## Substantive adjudication

Completed substantive dispositions are governed by `ADJUDICATION-CONTRACT.md` and
registered under `adjudications/`.

Review provenance and final decision authority are distinct. Under the current contract,
final public adjudication authority is explicitly project-maintainer authority and does
not claim an independent tribunal.

Corrections create superseding records; prior adjudications are not silently erased.

A confirmed falsification or confirmed contract gap requires a public consequence for
the affected claim revision. The same affected revision must not remain `PUBLISHED`.

Run the public governance self-check with:

```bash
python challenge/adjudication.py
```

The checker validates public bindings, lifecycle visibility, authority/provenance,
supersession, conflict freedom, and claim consequences only. It does not decide whether a
challenge is true and does not verify the private reference implementation.
