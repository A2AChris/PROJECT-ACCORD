# PROJECT ACCORD — Public Challenge Contract

**Status:** Publication candidate
**Revision:** `v0.3`

## Purpose

The public challenge surface accepts structured submissions that attempt to falsify a
published PROJECT ACCORD claim.

The harness checks only whether the submission is mechanically well formed against the
published claim identifiers. It does not decide truth, scope, impact, authenticity, or
whether a claim has actually been falsified.

## Mechanical result semantics

A successful parse reports:

```text
status = WELL_FORMED_CHALLENGE_SUBMISSION
scope_position = <submitter-supplied position>
judgment = NOT_PERFORMED
```

The phrase **well formed** is intentional.

The harness does not report `ADMISSIBLE`, `CONFIRMED`, `FALSIFIED`, `VERIFIED`, `SAFE`,
or `PASS` as a substantive judgment.

## Claim binding

Each submission binds to:

- one public claim ID;
- one public claim revision; and
- one published falsification ID.

The canonical identifier registry is
[`../claims/public-claim-index.json`](../claims/public-claim-index.json).

Free-text paraphrase does not replace the falsification ID.

## Scope position

Scope is not mechanically adjudicated.

The submitter must choose one of:

- `SUBMITTER_ASSERTED_IN_SCOPE`
- `SUBMITTER_UNCERTAIN`
- `SUBMITTER_ASSERTED_OUT_OF_SCOPE`

The harness echoes that position without promoting it to an ACCORD conclusion.

## Generic attack tags

A submission may use any of these broad tags:

- `EPISTEMIC_PROMOTION`
- `AUTHORITY_EXPANSION`
- `BOUNDARY_COLLAPSE`
- `LINEAGE_AMBIGUITY`
- `EVIDENCE_INCONSISTENCY`
- `SCOPE_ESCAPE`
- `SEMANTIC_OVERCLAIM`
- `OTHER`

Attack tags are organizational metadata, not claim-specific permission.

The harness does not reject a well-formed challenge because its tag was unexpected for
the selected claim.

If `OTHER` is used, `other_class` provides a short descriptive label.

## Public subject keys

The fixture uses canonical public semantic keys only:

- C01: `boundary`
- C02: `boundary`
- C03: `subject`
- C04: `historical_subject`, `historical_boundary`
- C05: `historical_subject`, `historical_cutoff`

These keys define the public question. They do not reveal the private reference
implementation's identity representation.

## Evidence and observations

Observations are **submitter assertions** linked to declared evidence entries.

Mechanical validation establishes only that references are internally consistent.

The harness does not:

- fetch or authenticate external references;
- decide whether evidence is genuine;
- decide whether an observation is true;
- remove contradictions;
- rank competing observations; or
- adjudicate the public claim.

## Security boundary

The challenge contract authorizes testing of published public artifacts only.

It does not authorize access to private repositories, credentials, infrastructure,
third-party systems, or unrelated data.
