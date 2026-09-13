# PROJECT ACCORD — Semantic Dependency Contract

**Status:** Public-surface claim dependency contract
**Revision:** `v0.1`

## Purpose

This contract governs publication-state handling for claim revisions that explicitly
depend on other public claim revisions for semantic interpretation.

The canonical machine-readable registry is `public-semantic-dependencies.json`.

## Separation rule

A semantic dependency is not evidence inheritance.

Evidence attached to a dependency does not automatically evidence the dependent claim,
and evidence attached to the dependent claim does not independently evidence the
dependency.

A failure of a semantic dependency also does **not** automatically establish that the
dependent claim is falsified.

## Fail-closed propagation

A dependent claim revision must not remain unchanged in `PUBLISHED` state when one of its
declared semantic dependencies leaves `PUBLISHED` state.

If a declared dependency becomes `SUSPENDED`, `WITHDRAWN`, or `SUPERSEDED`, the dependent
claim revision requires explicit re-evaluation before it may again be represented as
`PUBLISHED`.

The fail-closed consequence is therefore a publication-state constraint, not a propagated
truth judgment. The dependent claim may be suspended, withdrawn, or superseded as
appropriate; it is not automatically assigned a falsification disposition merely because
a dependency changed state.

## Current registered dependencies

For the current public surface:

- `ACCORD-C05 v0.3` depends on `ACCORD-C03 v0.2` for semantic interpretation; and
- `ACCORD-C05 v0.3` depends on `ACCORD-C04 v0.2` for semantic interpretation.

These relations record semantics already stated by the public surface. They do not create
new implementation evidence for C03, C04, or C05.

## Machine-checkable governance

`dependency_guard.py` validates that registered claim revisions exist and rejects a state
in which a declared semantic dependency is not `PUBLISHED` while its dependent claim
revision remains `PUBLISHED`.

The guard does not decide whether any claim is true, whether a falsification is correct,
or whether a replacement revision is semantically equivalent. Those questions require
separate review and, where applicable, adjudication.
