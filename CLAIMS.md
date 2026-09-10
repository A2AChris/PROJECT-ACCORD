# PROJECT ACCORD — Public Claims

**Status:** Publication candidate
**Public contract revision:** `v0.2`

This document is the normative public prose contract for PROJECT ACCORD claims.

The companion [`claims/public-claim-index.json`](claims/public-claim-index.json) is
normative only for claim IDs, claim revisions, falsification IDs, and public evidence
status. It does not replace the prose meaning of this document.

A public claim is not made stronger by README language, examples, fixtures, CI counts,
or the existence of a private reference implementation.

---

## Public claim vocabulary

### Positive assertion

A **positive assertion** is a decision, record, relation, or conclusion that represents
the relevant proposition as established or supported, rather than unresolved,
unsupported, ambiguous, contradictory, or unknown.

The public contract does not require the private implementation to use these words as
runtime labels.

### Independent basis

An **independent basis** is evidence or authority support that does not derive solely
from the assertion, actor, action, or successor state whose legitimacy it is being used
to establish.

### Admitted evidence

**Admitted evidence** is evidence selected under a declared admission rule applicable to
the claim.

A result-dependent rule that excludes evidence merely because it weakens the desired
conclusion does not satisfy this definition.

### Material evidence

Evidence is **material to a public assertion** when accepting or rejecting it could
change at least one of:

- whether the assertion is supported;
- whether the asserted subject or lineage is unique enough for the claim;
- whether the assertion remains inside its declared boundary; or
- whether the asserted semantic conclusion is stronger than the evidence supports.

### Stronger or broader authority

For C02, authority is **stronger or broader** when it would positively permit a
consequential action, extent, or exercise that the applicable admitted authority basis,
under its applicable rule, would not permit.

This definition does not require publication of the private authority representation.

### Historical boundary

A **historical boundary** limits which historical events, states, or transitions may be
treated as part of the asserted history.

It does not automatically prohibit later-observed evidence used only to validate the
integrity, provenance, or continued identity of retained historical evidence, provided
that use is declared and does not import later state as a historical fact inside the
bounded proposition.

### Fail-closed claim discipline

Where a claim requires support that is missing, ambiguous, contradictory, inapplicable,
or otherwise unresolved — or stale where current applicability is part of the asserted
proposition — that uncertainty must not silently become the corresponding positive
assertion.

---

# ACCORD-C01 — Epistemic and Authority Separation

**Revision:** `v0.2`

### Claim

At a declared consequential-action boundary, PROJECT ACCORD must not make a positive
authority decision solely from actor-controlled assertion, interpretation, intent,
technical capability, confidence, or presentation/possession of an artifact.

A positive authority decision must depend on an independently admitted authority basis
and whatever validation the declared authority rule requires.

### Subject

One declared consequential-action boundary and the authority proposition evaluated
there.

### Scope

C01 concerns whether actor-controlled or actor-presented material is promoted into
authority.

It does not claim that every credential or artifact is non-authoritative. An artifact
may carry authority evidence when that authority originates outside the actor's
self-assertion and the required validation succeeds.

### Assumptions

The consequential boundary and the positive authority proposition being evaluated are
identifiable.

The existence or successful application of an authority-admission/validation rule is
**not** assumed.

### Required evidence

A positive C01 authority decision requires enough evidence to identify:

- what the actor supplied or controlled;
- the independent authority basis relied upon;
- the applicable validation rule; and
- that the validation required by that rule succeeded.

If a required authority basis or validation rule is absent or unresolved, that absence
must not silently become a positive authority decision.

### Forbidden inferences

None of these is sufficient merely because it is asserted, possessed, or technically
available:

- observation or claim;
- interpretation or model output;
- intent;
- capability;
- confidence;
- credential or token presentation; or
- technical privilege.

### Falsification conditions

**C01-F1 — Self-legitimation**

C01 is falsified by a valid in-scope trace in which actor-controlled or actor-presented
material is sufficient for a positive authority decision without an independent
authority basis required by the declared rule.

**C01-F2 — Validation-by-possession**

C01 is falsified by a valid in-scope trace in which presentation or possession of an
authority-bearing artifact is treated as sufficient even though validation required by
the declared rule failed, was absent, or was bypassed.

### Public evidence status

No C01-specific public reference-evidence record is attached in this candidate.

That is not a statement that private engineering evidence does not exist; it is a limit
on what this public repository presently evidences.

### Disclosure boundary

Private implementation structure and private authority representation remain outside the
public claim.

---

# ACCORD-C02 — Rooted and Conserved Authority

**Revision:** `v0.2`

### Claim

A positive authority decision at a declared consequential boundary must be supportable
by an admitted authority basis whose legitimacy does not depend on that same positive
decision or on a successor state created by the transition being justified.

Processing may preserve or constrain supported authority. It must not create unsupported
authority, revive no-longer-applicable authority without fresh support, or use a
successor rule/state to authorize the transition that creates that successor.

### Subject

The authority proposition positively accepted at one declared consequential-action
boundary.

### Scope

C02 concerns the relationship between:

- the applicable admitted authority basis;
- the declared rules under which authority support is evaluated; and
- the authority positively accepted at the boundary.

C02 does not claim universal legal, moral, or social legitimacy of the admitted basis.

### Assumptions

The consequential boundary and the positive authority proposition accepted there are
identifiable.

The existence, applicability, freshness, or sufficiency of an authority basis is **not**
assumed.

### Required evidence

A positive C02 authority decision requires evidence sufficient to identify:

- the admitted authority basis relied upon;
- the rule under which that basis supports the positive proposition;
- the basis/rule state applicable before the positive decision; and
- material invalidation, expiry, revocation, supersession, or successor changes relevant
  to that support.

Absent or unresolved support must not be promoted into positive authority.

### Forbidden inferences

C02 does not establish that:

- an admitted root is trustworthy merely because it is admitted;
- every delegation or transformation is valid;
- separate authority dimensions are globally fungible;
- removal of a restriction automatically restores authority;
- authorization proves execution or effect; or
- satisfying C02 proves system-wide safety.

### Falsification conditions

**C02-F1 — Unsupported expansion**

C02 is falsified by a valid in-scope trace in which the positive authority proposition
is materially stronger or broader than the applicable admitted basis supports.

**C02-F2 — Successor self-authorization**

C02 is falsified by a valid in-scope trace in which a new or successor authority
basis/rule/state participates in the authority proof for the transition that establishes
that same successor, without independently sufficient predecessor authority.

**C02-F3 — Unsupported restoration**

C02 is falsified by a valid in-scope trace in which expired, revoked, consumed,
superseded, stale, or otherwise inapplicable authority becomes positively exercisable
again solely because a restriction is removed or a prior artifact still exists.

### Public evidence status

No C02-specific public reference-evidence record is attached in this candidate.

### Disclosure boundary

The private authority representation and evaluation implementation remain undisclosed.

---

# ACCORD-C03 — Authorization / Execution / Effect Separation

**Revision:** `v0.2`

### Claim

Authorization, execution, real-world effect, observed state, and causal attribution are
distinct public assertion classes.

Evidence sufficient for one class must not automatically be treated as sufficient for a
stronger or different class.

### Subject

One declared consequential action, execution context, or causal assertion.

### Scope

C03 concerns semantic promotion among:

- authorization;
- execution or execution attempt;
- real-world effect;
- observed state/outcome;
- causal attribution; and
- historical evidence used to make a present-authority claim.

C03 does not require these propositions to have different truth values in every case. It
requires their **justification to remain distinct**.

### Assumptions

The asserted proposition class and the evidence relied upon for it are identifiable.

### Required evidence

A positive assertion in one semantic class requires evidence appropriate to that class.
A weaker or different assertion is not itself that evidence merely because it precedes
or correlates with the stronger assertion.

### Forbidden inferences

Without additional evidence appropriate to the asserted class:

- authorization does not establish execution;
- execution attempt does not establish real-world effect;
- observed state does not establish causal origin; and
- historical evidence does not establish present authority.

### Falsification conditions

**C03-F1 — Authorization promotion**

A positive execution/effect assertion is accepted merely from authorization evidence,
without evidence appropriate to the asserted execution/effect proposition.

**C03-F2 — Observation-to-cause promotion**

An observed state/outcome is positively attributed to a cause merely from observation
or temporal correlation without evidence appropriate to the causal claim.

**C03-F3 — Historical-to-present promotion**

Historical authority/assurance evidence is treated as sufficient for present authority
without evidence that the required present applicability/currentness conditions hold.

**C03-F4 — Semantic-class ambiguity**

A materially consequential positive result is represented so ambiguously that the public
assertion class — authorization, execution, effect, observed state/outcome, or causal
attribution — cannot be distinguished, while downstream use treats the ambiguity as the
stronger class.

### Public evidence status

`ACCORD-RM01` depends on C03's semantic separation when interpreting C05, but the RM01
record is **not independent public evidence of C03 as a general claim**.

### Disclosure boundary

Private execution architecture and implementation structure remain outside the public
claim.

---

# ACCORD-C04 — Bounded Historical Reconstruction Discipline

**Revision:** `v0.2`

### Claim

For a reconstruction profile explicitly claimed under C04, PROJECT ACCORD may make a
positive bounded historical causal/execution assertion only when admitted retained
evidence supports that assertion for the declared subject and historical boundary.

Material missing evidence, ambiguity, contradiction, or boundary uncertainty must not be
silently converted into a stronger positive historical assertion.

Mutable present-day projection state must not substitute for the retained historical
provenance required by the claim.

### Subject

A declared historical subject and a declared historical boundary.

The private representation used to identify either is not public claim material.

### Scope

C04 applies only to a reconstruction profile explicitly bound to C04 and to the coverage
declared by that profile.

It is not a universal assertion about every historical question PROJECT ACCORD may ever
support.

The reconstruction question identifies:

- the historical subject;
- the historical boundary;
- the semantic proposition requested; and
- the evidence-admission rule relevant to that proposition.

### Assumptions

The public question identifies its subject, boundary, proposition, and evidence-admission
rule sufficiently to evaluate the claimed result.

These are inputs to the claim. **Evidence sufficiency is not an assumption.**

### Required evidence

A positive C04 assertion requires admitted retained evidence sufficient for the actual
semantic strength of that assertion.

Where uniqueness is part of the asserted proposition, the evidence must support that
uniqueness.

Material evidence must not be discarded merely because it creates a gap, ambiguity, or
contradiction.

### Forbidden inferences

A positive C04 reconstruction does not by itself establish:

- present authority;
- present currentness;
- real-world effect unless that effect is itself the evidenced proposition;
- production readiness;
- formal correctness; or
- historical semantic truth beyond the declared evidence and coverage.

### Falsification conditions

**C04-F1 — Unsupported positive reconstruction**

A positive historical assertion is emitted despite missing support required for the
asserted proposition.

**C04-F2 — Material inconsistency suppression**

Material ambiguity or contradiction is omitted, neutralized, or hidden while a stronger
positive assertion is emitted.

**C04-F3 — Projection substitution**

The positive historical assertion depends on mutable present-day projection state in
place of the retained historical provenance required by the claim.

**C04-F4 — Boundary escape**

The positive assertion treats an event/state outside the declared historical boundary as
part of the bounded historical proposition, or uses later verification evidence to
supply a historical fact it does not merely validate, without explicitly changing the
claim boundary.

**C04-F5 — Result-dependent evidence admission**

Evidence material to the assertion is excluded or admitted because doing so produces the
desired result rather than because of the declared evidence-admission rule.

**C04-F6 — Semantic overclaim**

The positive conclusion is stronger than the admitted evidence and declared coverage
support.

### Public evidence status

`ACCORD-RM01` uses C04 as a semantic reconstruction discipline for C05, but RM01 does
**not** independently evidence C04 across other reconstruction profiles.

### Disclosure boundary

Private representation, reconstruction, persistence, and integrity design remain
undisclosed.

---

# ACCORD-C05 — Bounded Historical Execution Lineage

**Revision:** `v0.2`

### Claim

For the C05 reference profile, PROJECT ACCORD may make a positive assertion that one
specific committed authority-to-execution lineage belongs to the declared historical
execution subject **only if** admitted retained evidence uniquely supports that positive
lineage assertion within the declared historical cutoff.

Uniqueness concerns the lineage asserted for the declared subject, not uniqueness of the
evidentiary representation or proof path.

If support is missing, the subject is under-specified, material alternatives remain,
material evidence conflicts, or the declared cutoff cannot be respected, PROJECT ACCORD
must not emit the stronger positive unique-lineage assertion.

Relevant unresolved limitations, ambiguity, or contradiction must remain visible at the
public claim level even though the private representation of those conditions is not
public.

### Subject

A public selector sufficiently specific to ask about one concrete historical execution
instance within its consequential-action context, plus an explicit historical cutoff.

The private identity representation is not public claim material.

### Scope

C05 covers only the bounded historical authority-to-execution lineage asserted for the
declared subject and cutoff.

It does not automatically extend to:

- later target interaction;
- real-world effect;
- outcome confirmation;
- authoritative current state; or
- present authority.

### Assumptions

- the public subject selector and cutoff are declared;
- the requested proposition is the C05 unique-lineage proposition; and
- the evidence-admission rule to be applied to the question is declared.

**The existence, sufficiency, consistency, uniqueness, or correct historical
classification of evidence is not assumed.** Those are conditions the positive assertion
must earn.

### Required evidence

A positive C05 assertion requires admitted retained evidence sufficient to:

- support the declared subject-to-lineage binding;
- support the claimed committed historical provenance;
- establish that material alternative lineages for the declared subject are not left
  unresolved;
- remain within the declared cutoff;
- distinguish material retained historical provenance from mutable present-day
  projection where that distinction affects the assertion; and
- preserve material contradictory evidence or limitations rather than laundering them
  away.

### Relationship to C03 and C04

C05 is a narrower reference-profile claim.

It relies on:

- C03 to prevent a historical execution lineage from being silently promoted into
  real-world effect or present authority; and
- C04 for fail-closed bounded reconstruction discipline.

Evidence for C05 does **not** thereby establish C03 or C04 universally.

### Forbidden inferences

A positive C05 assertion does not by itself establish:

- current authority;
- new execution power;
- currentness;
- successful target invocation;
- real-world effect;
- outcome confirmation;
- authoritative current state;
- system-wide causal completeness;
- production readiness; or
- formal correctness.

### Falsification conditions

**C05-F1 — Unsupported unique-lineage assertion**

A positive unique-lineage assertion is emitted without sufficient admitted retained
evidence for the declared subject and cutoff.

**C05-F2 — Subject ambiguity**

The public subject selector is insufficient to distinguish the claimed execution
instance, yet a positive unique-lineage assertion is emitted.

**C05-F3 — Cross-subject evidence**

Material evidence belonging to a materially different historical subject is used to
support the positive lineage assertion.

**C05-F4 — Material alternative/contradiction suppression**

A material alternative lineage, ambiguity, or contradiction remains unresolved but is
suppressed while a positive unique-lineage assertion is emitted.

**C05-F5 — Boundary escape or historical contamination**

The positive assertion incorporates post-cutoff event/state as part of the claimed
bounded history, or later verification evidence is used to inject a historical fact
rather than only validate retained historical evidence under the declared admission
rule.

**C05-F6 — Projection or irrelevant-history dependence**

The positive historical assertion changes solely because mutable present-day projection
or history irrelevant to the declared subject/boundary changes.

**C05-F7 — Semantic overclaim**

The reconstructed historical lineage is represented as proving a stronger proposition
such as present authority, real-world effect, outcome confirmation, or system-wide causal
completeness without evidence for that stronger proposition.

**C05-F8 — Result-dependent evidence admission**

Evidence material to the C05 assertion is excluded, included, or reclassified because
doing so produces the desired unique lineage rather than because of the declared
evidence-admission rule.

### Reference evidence

The current candidate attaches the R0 project-attested record `ACCORD-RM01` to **C05
only**.

The record's mention of C03/C04 describes semantic dependencies of C05, not independent
evidence for those broader claims.

### Reproduction level

- C05 private reference evidence: **R0 — PROJECT-ATTESTED**;
- public challengeability: not upgraded until the challenge surface is actually public;
- public reproduction of the private reference implementation: **not claimed**.

### Disclosure boundary

Private identity representation, implementation decomposition, persistence/integrity
design, internal assurance machinery, engineering history, adversarial research corpus,
and implementation code remain outside the public claim.

---

# Cross-claim non-generalization rule

Evidence attached to one public claim does not automatically evidence another claim.

A dependency relation among claims is not an evidence relation.

A successful challenge-harness parse is not evidence that a counterexample is true.

A successful evidence-record self-check is not evidence that the private reference
implementation satisfies a claim.

A passing private CI summary is bounded project-attested evidence; it is not a universal
proof of any claim.

---

# Public claim-change rule

Any material change to:

- claim meaning;
- public subject;
- scope;
- assumptions;
- evidence-admission rule;
- required evidence;
- forbidden inference;
- falsification condition;
- evidence status; or
- disclosure boundary

requires a new claim revision and adversarial review.

A wording change must not silently expand the quantifier or applicability of a claim.
