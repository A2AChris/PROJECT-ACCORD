# PROJECT ACCORD — Public Evidence

This directory contains sanitized public evidence records.

## Current public reference

`ACCORD-RM01`

Evidence level: **R0 — PROJECT-ATTESTED**

The current record is attached to **ACCORD-C05 v0.2 only**.

## Challenge availability

The record attests that the structured challenge contract is present in the public-surface
artifact. It does not attest current repository visibility. **R1 — PUBLICLY CHALLENGEABLE**
applies only while that surface is actually publicly accessible.

C05 depends semantically on C03 and C04, but that dependency does not make the RM01
record independent evidence for C03 or C04 as general claims.

## Project-attested CI summary

The record attests:

| Environment family | Runtime family | Result |
|---|---|---:|
| Linux | Python 3.12 | 901 / 901 |
| Windows | Python 3.12 | 901 / 901 |
| Windows | Python 3.13 | 901 / 901 |

These are project attestations for the privately bound C05 reference profile. They are
not public reproduction and are not universal proof of C05.

## Reference commitment

The record contains an opaque SHA-256 commitment to privately retained reference-binding
material. The opening material is not in this repository.

## Public self-check

Run:

```bash
python evidence/verify_record.py
```

A successful self-check verifies the public record's digest and declared public
cross-field invariants only.

It intentionally reports:

```text
PRIVATE_REFERENCE_OPENING=NOT_PERFORMED
REFERENCE_VERIFICATION=NOT_PERFORMED
```
