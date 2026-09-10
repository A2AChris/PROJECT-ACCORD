# PROJECT ACCORD — Challenge Surface

This directory contains the clean-room public challenge-submission format.

It is not a simulator or verifier for the private reference implementation.

## Run

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
