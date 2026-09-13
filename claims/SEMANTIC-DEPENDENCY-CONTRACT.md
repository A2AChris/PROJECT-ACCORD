# PROJECT ACCORD — Semantic Dependency Failure-Propagation Contract

**Status:** Public-surface semantic dependency governance contract
**Revision:** `v0.1`

## Purpose

This contract governs what must happen when a published claim revision explicitly relies
on another published claim revision for semantic interpretation and that exact dependency
later receives an active confirmed negative adjudication.

It does not create evidence inheritance and it does not turn a finding against one claim
into an automatic falsification of another claim.

## Canonical dependency registry

Current machine-readable semantic dependency bindings are registered in
`public-semantic-dependencies.json`.

Each binding names:

- one exact dependent claim revision;
- one or more exact dependency claim revisions;
- the dependency relation; and
- the public rule text that already declares the relationship.

The registry records existing public claim semantics. It does not silently add a new
claim requirement.

## Failure-propagation trigger

A semantic dependency becomes **adversely active** for this contract only when an active
final adjudication targets that exact dependency claim revision with one of:

- `CONFIRMED_FALSIFICATION`; or
- `CONFIRMED_CONTRACT_GAP`.

Only the terminal active adjudication in a valid supersession chain counts.

The following do **not** by themselves trigger dependency failure propagation:

- absence of claim-specific public evidence;
- an `INSUFFICIENT_EVIDENCE` or `NOT_CONFIRMED` disposition;
- an unresolved or merely submitted challenge;
- ordinary claim revision or supersession without an active confirmed negative finding;
  or
- the existence of a semantic dependency itself.

## Fail-closed dependent-state rule

While an adversely active dependency finding exists, a registered dependent claim
revision **must not remain `PUBLISHED`**.

At minimum it must be `SUSPENDED` while the semantic dependency is reassessed. A claim
that is explicitly `WITHDRAWN` or validly `SUPERSEDED` is also not `PUBLISHED`.

This rule is deliberately weaker than automatic falsification: a confirmed finding
against a dependency does not prove that the dependent claim is itself false. It proves
that the project may no longer leave the dependent claim positively published without an
explicit reassessment of the dependency impact.

## Exact-revision discipline

Dependency bindings are revision-specific.

A replacement revision of a dependency does not silently retarget an existing dependent
claim. If the dependent claim is to rely on different dependency semantics, that change
must be made explicitly in the public claim/dependency surface under the applicable
claim-change rules.

A later adjudication that supersedes an earlier confirmed finding does not silently
restore a suspended dependent claim. Any restoration to `PUBLISHED` remains an explicit
public state decision after reassessment.

## Current binding

The current registry records the already-public relationship for `ACCORD-C05 v0.3`:

- `ACCORD-C03 v0.2` — semantic interpretation dependency; and
- `ACCORD-C04 v0.2` — semantic interpretation dependency.

This machine-readable binding does not attach C05 evidence to C03 or C04 and does not
raise the evidence level of any claim.

## Machine-checkable enforcement

`dependency_guard.py` validates the registry against the public claim/state registries and
active adjudication records.

The public validation workflow must fail if an active confirmed negative finding targets
an exact registered dependency revision while its dependent revision remains
`PUBLISHED`.

The guard operates only on public governance artifacts. It performs no private reference
verification.
