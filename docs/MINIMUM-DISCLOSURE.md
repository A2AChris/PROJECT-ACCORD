# PROJECT ACCORD — Minimum Disclosure Contract

**Status:** Publication candidate
**Revision:** v0.3 hardened through P8 claim red team

## Minimum public record

A published ACCORD claim requires no more than:

**claim + public subject concept + scope + assumptions + required evidence class +
forbidden inferences + falsification properties + evidence level + disclosure boundary**

It does **not** require publication of the private mechanism.

## Public subject rule

The public subject definition states only the specificity necessary to make the claim
meaningful.

It must not disclose the private subject representation unless a detail is independently
necessary to falsify the claim.

For C05, it is sufficient to state:

> A historical execution subject must be specific enough to distinguish the concrete
> execution instance being questioned within its consequential-action context.

No public two-field formula is required.

## Public lineage rule

A public historical-lineage claim may identify the semantic endpoints necessary to state
the claim.

It must not enumerate private implementation decomposition when the same claim can be
falsified using a boundary-level description.

For C05, the public contract therefore speaks of a **bounded committed
authority-to-execution lineage** rather than a private stage sequence.

## Public attack rule

A challenge surface needs broad failure properties, not a copy of the private red-team
taxonomy.

Minimum generic challenge classes are:

- `EPISTEMIC_PROMOTION`
- `AUTHORITY_EXPANSION`
- `BOUNDARY_COLLAPSE`
- `LINEAGE_AMBIGUITY`
- `EVIDENCE_INCONSISTENCY`
- `SCOPE_ESCAPE`
- `SEMANTIC_OVERCLAIM`
- `OTHER`

`OTHER` is mandatory so the public vocabulary never defines the universe of possible
attacks.

Mechanism-specific attack detail should be expressed in the counterexample narrative when
relevant rather than canonized as public architecture.

## Public evidence rule

R0 evidence may publish:

- a public evidence record identifier;
- a public milestone alias;
- an opaque commitment to the private reference;
- project-attested result summaries;
- evidence classification;
- forbidden inferences; and
- integrity metadata for the public record.

R0 evidence does not need to publish:

- internal milestone names;
- raw private commit SHA;
- private branch or tag names;
- CI provider run IDs;
- CI job IDs;
- raw logs;
- runner IDs;
- repository names; or
- private author/committer metadata.

These identifiers do not make a private implementation publicly reproducible.

## C01 minimum

Publish:

- the non-promotion rule;
- public scope;
- required evidence class;
- forbidden inferences;
- falsification property.

Do not publish private authority implementation structure.

## C02 minimum

Publish:

- rooted/conserved authority principle;
- public boundary;
- unsupported expansion falsifier.

Do not publish the private representation or implementation used to evaluate the claim.

## C03 minimum

Publish:

- semantic non-equivalence among authorization, execution, effect, observed state, and
  causal attribution;
- the public boundary;
- a semantic-promotion falsifier.

Do not publish private execution architecture or implementation decomposition.

## C04 minimum

Publish:

- historical subject concept;
- historical cutoff concept;
- retained-evidence requirement;
- projection/provenance separation;
- broad ambiguity, contradiction, consistency, scope, and overclaim falsifiers.

Do not publish private reconstruction, storage, identity, or integrity design.

## C05 minimum

Publish:

- a sufficiently specific historical execution subject concept;
- a bounded historical cutoff;
- a committed authority-to-execution lineage claim;
- required provenance/ambiguity preservation;
- broad falsification properties;
- explicit non-claims.

Do not publish private identity structure, implementation decomposition, persistence or
integrity design, internal attack taxonomy, or private engineering mechanisms.

## Correlation test

Before publishing any technical detail, ask:

1. Is it necessary to identify the public proposition?
2. Is it necessary to make the public subject sufficiently specific?
3. Is it necessary to bound the claim?
4. Is it necessary for an external party to construct a meaningful counterexample?
5. Does it reveal private structure when combined with other already-public facts?
6. Does it provide independent public verification value?

If the answer to 1–4 and 6 is "no" while 5 is "yes", the detail must remain private.

## Evidence statement discipline

Every public evidence statement must classify itself as one of:

- independently public evidence;
- project-attested evidence; or
- not claimed / not verified.

Successful public artifact validation must not be described as verification of the
private reference implementation.

## Minimum falsifiability discipline

A claim record must expose stable falsification identifiers.

A challenge submission binds to one claim revision and one falsification identifier.
Free-text paraphrase is supplementary only.

Assumptions may establish the question and evaluation boundary; they may not assume the
property the claim is intended to demonstrate.

## Minimum evidence-binding discipline

Every public evidence record names exactly which public claim revision it evidences.

Dependencies on other claims are separately labeled and do not inherit the evidence
status of the evidenced claim.

## Historical-boundary discipline

A historical cutoff constrains the historical proposition, not necessarily the
wall-clock time at which all verification evidence is observed.

Later evidence may validate integrity/provenance of retained historical material when
that use is declared. It must not silently import later state into the bounded historical
proposition.
