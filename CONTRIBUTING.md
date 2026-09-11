# Contributing to PROJECT ACCORD

**Status:** Public-surface contribution policy

PROJECT ACCORD is designed to accept scrutiny before it accepts trust.

The most valuable contribution is a precise counterexample to a published claim within
that claim's declared boundary.

## Read before contributing

The README is descriptive. Public claim meaning is governed by:

- [`CLAIMS.md`](CLAIMS.md)
- [`docs/PUBLIC-DISCLOSURE-MODEL.md`](docs/PUBLIC-DISCLOSURE-MODEL.md)
- [`docs/MINIMUM-DISCLOSURE.md`](docs/MINIMUM-DISCLOSURE.md)
- [`challenge/ATTACK-CONTRACT.md`](challenge/ATTACK-CONTRACT.md)

Do not infer private architecture from public challenge vocabulary.

## Current contribution status

General external code and documentation contributions are **not yet open**.

The repository license is Apache License 2.0 (`Apache-2.0`); see [`LICENSE`](LICENSE) and
[`LICENSE-SCOPE.md`](LICENSE-SCOPE.md). The license covers this repository's public-surface
files only and does not place separate private or unpublished PROJECT ACCORD material
under Apache-2.0.

General external code and documentation contributions are still closed. Do not submit
implementation code, documentation rewrites, or pull requests intended for incorporation
into the repository unless PROJECT ACCORD explicitly opens that contribution path.

Security reports and research challenges submitted through those review channels are
designated **Not a Contribution** for purposes of Apache-2.0 unless the copyright owner
separately and explicitly submits the material for inclusion in the Work. If contribution
intake is later explicitly opened, a Contribution intentionally submitted for inclusion in
the Work is governed by Apache-2.0 Section 5 unless a separate written agreement expressly
states otherwise.

This restriction prevents ambiguous ownership, incorporation, or licensing from being
created before a contribution path is deliberately opened.

## Counterexamples and research challenges

The public challenge format is intended for concrete attempts to falsify ACCORD claims.

A useful counterexample should identify:

- the public claim and revision;
- the exact subject;
- the declared scope and why the challenge is in scope;
- the observation or trace relied upon;
- the evidence supporting each relevant observation;
- the published falsification ID allegedly satisfied; and
- the reasoning that connects the evidence to that condition.

The clean-room fixture format under [`challenge/`](challenge/) exists to make those
elements inspectable and deterministic.

Mechanical well-formedness is not substantive acceptance.

`WELL_FORMED_CHALLENGE_SUBMISSION` means only that the fixture satisfies the public
mechanical submission contract. The accompanying `scope_position` is the submitter's
position, not an ACCORD finding. `judgment = NOT_PERFORMED` remains mandatory.

## Unexpected attacks are welcome

Named attack classes are convenience categories, not a closed attack catalogue.

A valid counterexample does not become invalid merely because PROJECT ACCORD failed to
anticipate its attack class. Use the public `OTHER` category when necessary and describe
the attack plainly.

## Evidence minimization

Provide the minimum evidence necessary to evaluate the challenge.

Do not submit:

- credentials or secrets;
- unrelated personal data;
- private repository material;
- proprietary third-party material you are not permitted to disclose;
- bulk datasets when a minimized reproducer is sufficient; or
- material obtained through unauthorized access.

If a report is security-sensitive, follow [`SECURITY.md`](SECURITY.md) rather than
publishing it through a public contribution path.

## Claim changes

A proposed change that alters any of the following is not an editorial change:

- claim;
- subject;
- scope;
- assumptions;
- required evidence;
- forbidden inferences;
- falsification conditions;
- evidence classification;
- reproduction level; or
- disclosure boundary.

Such a change requires an explicit public claim revision and adversarial review. It must
not silently strengthen an existing claim.

## Evidence changes

A public evidence update must remain sanitized and must distinguish provider-observed
metadata from project-attested facts.

Do not copy raw private logs, Git objects, private tests, private repository history, or
private implementation identifiers into a public evidence update.

A digest or manifest provides artifact integrity. It is not an authenticity proof for
the private implementation.

## Disclosure discipline

A contribution must not reveal private implementation detail merely because the detail
would make an explanation easier.

Before proposing new technical detail, ask whether it is necessary to identify, bound,
or meaningfully attempt to falsify the public claim. If an abstract semantic description
is sufficient, prefer the abstract description.

Cumulative disclosure matters: individually harmless details can reconstruct private
architecture when combined.

## Conduct of technical review

PROJECT ACCORD reviews should distinguish:

- a confirmed defect;
- a plausible but unconfirmed attack hypothesis;
- an out-of-scope observation;
- insufficient evidence; and
- a rejected hypothesis.

Agreement is not the goal. Reproducible falsification is more valuable than rhetorical
consensus.

## Publication governance

Publication of this public surface is governed by the following release requirements:

- IP red-team review;
- claim red-team review;
- repository history and secret scan; and
- publication-candidate freeze on an exact committed revision.

The confidential security-reporting path is declared in [`SECURITY.md`](SECURITY.md) and
is not an open contribution channel.

These release requirements do not open general external contribution intake. General
external code and documentation contributions remain closed until PROJECT ACCORD
explicitly opens that path.
