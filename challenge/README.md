# PROJECT ACCORD — Challenge Surface

This directory contains the clean-room public challenge-submission format.

It is not a simulator or verifier for the private reference implementation.

## Mechanical submission validation

Run:

```bash
python challenge/harness.py challenge/fixtures/examples/ACCORD-C05-lineage-ambiguity.json
```

A mechanically valid file reports:

```text
status = WELL_FORMED_CHALLENGE_SUBMISSION
scope_position = SUBMITTER_ASSERTED_IN_SCOPE
judgment = NOT_PERFORMED
```

Those lines do not say the counterexample is true or that an ACCORD claim has been
falsified.

See [`ATTACK-CONTRACT.md`](ATTACK-CONTRACT.md).

## Substantive adjudication

Mechanical validation is deliberately not the end of the public governance chain.

Completed substantive dispositions are governed by
[`ADJUDICATION-CONTRACT.md`](ADJUDICATION-CONTRACT.md) and registered under
[`adjudications/`](adjudications/).

A confirmed falsification requires a public consequence for the affected claim revision.
The same affected revision must not remain `PUBLISHED`.

Run the public governance self-check with:

```bash
python challenge/adjudication.py
```

The checker validates public bindings and consequence invariants only. It does not decide
whether a challenge is true and does not verify the private reference implementation.
