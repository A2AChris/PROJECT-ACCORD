# PROJECT ACCORD — Public Challenge Contract

**Status:** Public-surface challenge contract
**Revision:** `v0.4`

## Purpose

The public challenge surface accepts structured submissions that attempt to falsify a
published PROJECT ACCORD claim.

The standard harness checks only whether a submission is mechanically well formed against
published claim identifiers. It does not decide truth, scope, impact, authenticity, or
whether a claim has actually been falsified.

## Mechanical result semantics

A successful standard parse reports:

```text
status = WELL_FORMED_CHALLENGE_SUBMISSION
scope_position = <submitter-supplied position>
judgment = NOT_PERFORMED
```

The harness does not report `ADMISSIBLE`, `CONFIRMED`, `FALSIFIED`, `VERIFIED`, `SAFE`,
or `PASS` as a substantive judgment.

## Claim binding

A standard registered-falsification submission binds to:

- one public claim ID;
- one public claim revision; and
- one published falsification ID.

The canonical identifier registry is `../claims/public-claim-index.json`.

Free-text paraphrase does not replace the falsification ID.

## Novel falsification hypotheses

The standard harness intentionally remains bound to registered falsification IDs.

If a submitter alleges that the public claim is contradicted by a mechanism that no
published falsification ID faithfully expresses, the submitter may use the separate
`NOVEL_FALSIFICATION_HYPOTHESIS` lifecycle path defined by
`LIFECYCLE-CONTRACT.md`.

That path challenges the completeness of the public falsification contract. It does not
grant the submitter authority to invent a new normative falsification condition.

## Scope position

Scope is not mechanically adjudicated.

The submitter chooses one of:

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

If `OTHER` is used, `other_class` provides a short descriptive label.

## Public subject keys

The fixture requires canonical public semantic keys:

- C01: `boundary`
- C02: `boundary`
- C03: `subject`
- C04: `historical_subject`, `historical_boundary`
- C05: `historical_subject`, `historical_cutoff`

They are minimum required keys, not a closed ontology. Additional public subject fields
may be supplied within the mechanical limits of the fixture.

These keys define the public question without exposing private identity representation.

## Evidence and observations

Observations are submitter assertions linked to declared evidence entries.

Mechanical validation establishes only internal reference consistency.

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
