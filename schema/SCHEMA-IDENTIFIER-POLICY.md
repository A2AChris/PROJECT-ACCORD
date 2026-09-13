# PROJECT ACCORD — Public Schema Identifier Policy

**Status:** Public-surface schema identifier policy
**Revision:** `v0.1`

## Purpose

This policy makes the meaning of public JSON Schema `$id` values explicit.

A schema `$id` is a canonical identifier. PROJECT ACCORD does **not** claim that every
identifier using an `https:` URI is a network locator, schema registry endpoint, or
dereferenceable URL.

## Legacy `.example` identifiers

A bounded set of already-published schemas uses identifiers under:

```text
https://project-accord.example/schema/
```

Those identifiers are intentionally classified as:

```text
NON_DEREFERENCEABLE_LEGACY_IDENTIFIER
```

The `.example` namespace is not presented as a live PROJECT ACCORD service or public
schema registry. External tooling must not infer network retrievability from those
historical `$id` values.

The exact legacy set and canonical repository paths are registered in
`schema/schema-id-registry.json`. Existing schema bytes and identifiers are preserved;
this policy does not silently rewrite historical or already-published schema identity.

## Canonical public access

For the current public repository, schema content is obtained from the registered
repository path at an exact Git revision. The repository path and Git revision provide
the public retrieval binding; `$id` provides schema identity.

A consumer that requires immutable retrieval should bind both:

1. the exact repository Git revision; and
2. the registered schema path.

## Identifier rule for new schema identities

New PROJECT ACCORD public schema identities introduced after this policy must use the
non-locator namespace:

```text
urn:project-accord:schema:
```

A new schema revision must not introduce another `http:` or `https:` `$id` merely to
suggest a network registry that PROJECT ACCORD does not operate.

If PROJECT ACCORD later operates a real stable schema registry, adopting its network
namespace requires an explicit future policy/schema revision. It does not retroactively
change existing identifiers.

## Machine-checkable boundary

Public validation enforces that:

- every checked `*.schema.json` has a unique non-empty `$id`;
- every `https://project-accord.example/schema/...` identifier is one of the exact
  registered legacy identifiers;
- all non-legacy public schema identifiers use `urn:project-accord:schema:`; and
- every registered legacy entry binds the exact schema path and declares
  `dereferenceable: false`.

This policy is about identifier and retrieval semantics only. It does not change the
meaning of any claim, evidence record, challenge contract, or adjudication.
