# PROJECT ACCORD — Public Disclosure Model

**Status:** Publication candidate
**Revision:** v0.3 hardened through P8 claim red team

## Purpose

PROJECT ACCORD exposes enough information to identify, bound, and attempt to falsify
selected claims without publishing the private construction that makes those claims
hold.

The governing rule is:

> **Publish the claim, its boundary, the evidence class, and a meaningful falsification
> surface — not the proprietary mechanism that satisfies the claim.**

## Public layers

### 1. Claim surface

May expose:

- the proposition being asserted;
- the public subject concept;
- scope and assumptions;
- forbidden inferences; and
- falsification properties.

Must not expose private representation or implementation decomposition merely to make the
explanation more concrete.

### 2. Falsification surface

May expose:

- broad failure properties;
- a generic challenge format;
- a way to submit unanticipated counterexamples; and
- rules that prevent a mechanical validator from becoming an oracle.

Must not expose:

- the complete private red-team corpus;
- private defect history;
- a one-to-one taxonomy of internal failure modes;
- private test names; or
- mechanism-specific attack guidance unnecessary for falsification.

### 3. Evidence surface

May expose:

- an opaque public reference commitment;
- evidence classification;
- sanitized project-attested result summaries;
- explicit limitations; and
- public artifact integrity metadata.

Must not expose unless independently justified:

- raw private commit SHAs;
- private branch, tag, workflow, run, or job identifiers;
- private repository names;
- raw Git objects;
- raw CI logs;
- private author/committer metadata;
- private runner metadata; or
- private test corpus.

### 4. Reference architecture

Only concepts strictly necessary to understand a public claim belong here.

Private architecture remains outside the public surface, including implementation
structure, internal data and identity representation, storage and integrity design,
engineering-stage details, adversarial research material, and implementation code.

## Correlation-resistance rule

A detail can be unsafe even when it is not secret by itself.

Public material must be reviewed for whether multiple clues can be combined to infer:

- private implementation decomposition;
- private identity structure;
- internal roadmap structure;
- private persistence or integrity design;
- internal attack history; or
- identifiers that correlate the public project with private engineering records.

Raw private identifiers are therefore not considered "free" evidence merely because they
do not reveal source code.

## Clean-room rule

Public documents and tooling are created from public contracts.

They are not copied from private source files, private tests, private documentation, raw
CI output, or private repository history.

## Public vocabulary rule

Public semantic terms must be chosen for claim evaluation, not as renamed versions of
private implementation identifiers.

If a public concept requires the same *shape* as a private mechanism, the publication
must ask whether that shape is truly necessary for falsification.

## Cumulative disclosure

P7 review is performed over the assembled repository, not file by file.

A candidate fails this gate if the combination of individually acceptable details allows
a materially more precise reconstruction of private architecture than any public claim
requires.

## Reproduction levels

### R0 — PROJECT-ATTESTED

The project identifies a bounded evidence statement and commits to a private reference,
but independent public reproduction is not available.

### R1 — PUBLICLY CHALLENGEABLE

The public claim and challenge contract allow independently inspectable counterexamples.

### R2 — PUBLICLY REPRODUCIBLE

A public artifact is sufficient to independently execute the relevant verification
without private access.

R0, R1, and R2 must never be collapsed into one another.

## Publication prohibition

Do not publish material merely because:

- it helps explain the implementation;
- it exists in private documentation;
- it appears harmless in isolation;
- it is already represented by a private SHA or CI identifier; or
- a reviewer could theoretically infer it anyway.

Disclosure must be necessary for the public claim or deliberately approved for another
public purpose.

## Claim falsifiability rule

A public claim must not make its own success an assumption.

In particular, evidence sufficiency, consistency, uniqueness, successful validation, or
absence of contradiction may not be placed in assumptions when those are the properties
the positive assertion is supposed to establish.

## Claim evidence non-generalization

A public evidence record binds only the claim revision it explicitly identifies.

Semantic dependency between claims is not evidence inheritance.

## Mechanical challenge neutrality

Public challenge tooling validates syntax and identifier binding only.

Submitter assertions about scope, evidence, and falsification remain submitter assertions
until separately adjudicated.
