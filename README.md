# PROJECT ACCORD

**Authority-Constrained Coordination of Autonomous Actors**

[English](#english) · [Deutsch](#deutsch)

> **Publication status:** Claim-hardened public-surface artifact. Repository visibility is controlled separately from this content.

This README is descriptive and non-normative. Public claim meaning is governed by
[`CLAIMS.md`](CLAIMS.md). Claim IDs, revisions, falsification IDs, and public evidence
status are indexed in
[`claims/public-claim-index.json`](claims/public-claim-index.json).

---

# English

## What is PROJECT ACCORD?

PROJECT ACCORD is a research and assurance project for consequential action by autonomous
and semi-autonomous actors.

Its central question is:

> **How can a system keep observation, interpretation, authority, authorization,
> execution, effect, observed state, and causal attribution from being silently collapsed
> into stronger claims than the available evidence supports?**

The public repository is a **claim, falsification, and evidence surface**. It is not a
source release or architectural blueprint of the private reference implementation.

## Current research maturity and evidence posture

PROJECT ACCORD is an **early public research artifact**. It is not presented as a
standard, a production-ready system, or an independently validated implementation.

The current public evidence posture is deliberately asymmetric:

- C01 and C02 currently have no claim-specific public reference evidence attached;
- C03 and C04 are semantic dependencies of RM01 but are not independently evidenced by
  RM01;
- C05 currently has **R0 — PROJECT-ATTESTED** evidence via `ACCORD-RM01`; and
- R1 public challengeability does not raise those implementation-evidence levels. R2
  independent public reproduction of the private reference is not claimed.

The purpose of this public surface is to expose claim meaning, falsifiers, evidence
limits, and challenge/adjudication rules to scrutiny without representing unevidenced
claims as established implementation results.

## Public claims

| Claim | Public subject | Current public evidence status |
|---|---|---|
| `ACCORD-C01 v0.2` | Epistemic and Authority Separation | no C01-specific public reference evidence attached |
| `ACCORD-C02 v0.2` | Rooted and Conserved Authority | no C02-specific public reference evidence attached |
| `ACCORD-C03 v0.2` | Authorization / Execution / Effect Separation | semantic dependency of RM01, not independently evidenced by RM01 |
| `ACCORD-C04 v0.2` | Bounded Historical Reconstruction Discipline | semantic dependency of RM01, not independently evidenced by RM01 |
| `ACCORD-C05 v0.3` | Bounded Historical Execution Lineage | **R0 — PROJECT-ATTESTED via ACCORD-RM01** |

The complete claim contract is [`CLAIMS.md`](CLAIMS.md).

### No evidence inheritance

Evidence attached to one claim does not automatically evidence another claim.

In particular, C05 depends on C03 and C04 for semantic interpretation, but the current
RM01 evidence record is attached to **C05 only**.

## Fail-closed public claim discipline

The public claims use a common rule:

> Missing, ambiguous, contradictory, stale, inapplicable, or otherwise unresolved support
> must not silently become the corresponding positive assertion.

For historical reconstruction claims this means that evidence sufficiency is something a
positive result must **earn**. It is not assumed in advance.

## Current public reference

The current private reference profile is represented publicly only by:

`ACCORD-RM01`

Status: **PROVISIONALLY FROZEN**

Evidence level: **R0 — PROJECT-ATTESTED**

The current evidence record is bound to **ACCORD-C05 v0.3**. The evidence package
intentionally does not claim public reproduction of the private implementation.

See [`evidence/`](evidence/).

## Challenge ACCORD

The clean-room challenge format is under [`challenge/`](challenge/).

A standard registered-falsification challenge binds to:

- one claim;
- one claim revision; and
- one published falsification ID.

A separate `NOVEL_FALSIFICATION_HYPOTHESIS` lifecycle path exists for a plausible claim
contradiction that no currently published falsification ID can faithfully express. That
path challenges the completeness of the public falsification surface. An unforeseen
mechanism is not, by itself, a new normative condition: it remains eligible when it
alleges a contradiction with normative content already present in the published claim
revision. What the path does not permit is adding a requirement that the published claim
revision never made.

The canonical public intake for a non-sensitive research challenge is a GitHub Issue in
this repository whose title begins with `[ACCORD CHALLENGE]`. Public receipt and pending
status are governed by [`challenge/LIFECYCLE-CONTRACT.md`](challenge/LIFECYCLE-CONTRACT.md)
and [`challenge/receipts/`](challenge/receipts/). No fixed substantive-decision SLA is
claimed; receipt and status-change timestamps make unresolved age externally observable.

A successful standard harness run means only:

```text
status = WELL_FORMED_CHALLENGE_SUBMISSION
scope_position = <submitter position>
judgment = NOT_PERFORMED
```

The harness does not decide whether the submitter is correct, whether the challenge is
actually in scope, or whether a claim has been falsified.

Generic attack tags are organizational metadata. They do not restrict which mechanism may
be used to challenge a claim.

Completed substantive challenge decisions are governed by
[`challenge/ADJUDICATION-CONTRACT.md`](challenge/ADJUDICATION-CONTRACT.md) and registered
under [`challenge/adjudications/`](challenge/adjudications/). Review provenance and final
decision authority are distinct. The current final decision-authority class is explicitly
`PROJECT_MAINTAINER`; PROJECT ACCORD does not claim an independent tribunal. Corrections
create superseding records rather than silently rewriting prior adjudications. A
`CONFIRMED_FALSIFICATION` or `CONFIRMED_CONTRACT_GAP` requires a public consequence for
the affected claim revision; the same affected revision must not remain `PUBLISHED`.

## Reproduction levels

- **R0 — PROJECT-ATTESTED:** bounded project attestation to a private reference.
- **R1 — PUBLICLY CHALLENGEABLE:** public claim and challenge surface permit structured
  external counterexamples and contract-gap hypotheses.
- **R2 — PUBLICLY REPRODUCIBLE:** the relevant verification can be independently executed
  without private access.

The current public claim, intake, lifecycle, and adjudication surface satisfies the R1
publication condition while those artifacts remain publicly accessible. R1 does **not**
imply public execution access to, simulation of, public trace generation from, or
independent reproduction of the private reference implementation. External empirical
generation of private-reference traces is not currently claimed.

These levels must not be collapsed.

## What ACCORD-RM01 does not prove

The current record does not by itself establish:

- present authority;
- successful target invocation;
- real-world effect;
- outcome confirmation;
- universal causal completeness;
- formal verification;
- production readiness;
- absence of unknown defects; or
- C01–C04 as general independently evidenced claims.

## Disclosure boundary

PROJECT ACCORD follows this rule:

> **Publish what must hold, where it must hold, and how it may be falsified — not the
> private mechanism that makes it hold.**

See:

- [`docs/PUBLIC-DISCLOSURE-MODEL.md`](docs/PUBLIC-DISCLOSURE-MODEL.md)
- [`docs/MINIMUM-DISCLOSURE.md`](docs/MINIMUM-DISCLOSURE.md)

## Research method

**condense → attack → implement → re-attack → freeze**

Local test success is not freeze-grade evidence. Publication freeze requires an exact
committed public-candidate revision and exact CI evidence.

## Repository map

```text
PROJECT-ACCORD/
├── README.md
├── CLAIMS.md
├── SECURITY.md
├── CONTRIBUTING.md
├── claims/
│   ├── public-claim-index.json
│   ├── public-claim-index.schema.json
│   ├── public-claim-state.json
│   └── public-claim-state.schema.json
├── docs/
├── challenge/
│   ├── ATTACK-CONTRACT.md
│   ├── LIFECYCLE-CONTRACT.md
│   ├── ADJUDICATION-CONTRACT.md
│   ├── receipts/
│   └── adjudications/
├── evidence/
└── tests/
```

The public-surface repository is licensed under the Apache License 2.0 (`Apache-2.0`).
The license applies to the files in this repository; separate private or unpublished
PROJECT ACCORD material is outside that licensed Work unless expressly distributed under
Apache-2.0 or another stated license. See [`LICENSE`](LICENSE) and
[`LICENSE-SCOPE.md`](LICENSE-SCOPE.md).

General external code/document contributions remain closed until explicitly opened under
the contribution rules in [`CONTRIBUTING.md`](CONTRIBUTING.md).

Confidential security reports may be sent to `project_accord@proton.me`. Repository-native
private vulnerability reporting is intended as an additional channel after public release.

---

# Deutsch

## Was ist PROJECT ACCORD?

PROJECT ACCORD ist ein Forschungs- und Assurance-Projekt für folgenreiche Handlungen
autonomer und teilautonomer Akteure.

Die zentrale Frage lautet:

> **Wie verhindert ein System, dass Observation, Interpretation, Authority,
> Authorization, Execution, Effect, beobachteter State und Causal Attribution still zu
> stärkeren Aussagen zusammengezogen werden, als die vorhandene Evidence trägt?**

Das öffentliche Repository ist eine **Claim-, Falsification- und Evidence-Oberfläche**.
Es ist weder Source Release noch Architekturplan der privaten Referenzimplementierung.

## Aktueller Forschungsreife- und Evidence-Stand

PROJECT ACCORD ist ein **frühes öffentliches Forschungsartefakt**. Es wird nicht als
Standard, produktionsreifes System oder unabhängig validierte Implementierung dargestellt.

Der aktuelle öffentliche Evidence-Stand ist bewusst asymmetrisch:

- C01 und C02 besitzen derzeit keine claim-spezifische Public Reference Evidence;
- C03 und C04 sind semantische Abhängigkeiten von RM01, werden durch RM01 aber nicht
  unabhängig evidenziert;
- C05 besitzt derzeit **R0 — PROJECT-ATTESTED** Evidence über `ACCORD-RM01`; und
- die öffentliche R1-Challengeability hebt diese Implementation-Evidence-Level nicht an.
  Eine unabhängige öffentliche R2-Reproduktion der privaten Referenz wird nicht behauptet.

Zweck dieser Public Surface ist es, Claim-Bedeutung, Falsifier, Evidence-Grenzen sowie
Challenge-/Adjudication-Regeln der Prüfung auszusetzen, ohne nicht evidenzierte Claims als
nachgewiesene Implementierungsergebnisse darzustellen.

## Öffentliche Claims

| Claim | Öffentlicher Gegenstand | Aktueller Public-Evidence-Status |
|---|---|---|
| `ACCORD-C01 v0.2` | Epistemic and Authority Separation | keine C01-spezifische Public Reference Evidence |
| `ACCORD-C02 v0.2` | Rooted and Conserved Authority | keine C02-spezifische Public Reference Evidence |
| `ACCORD-C03 v0.2` | Authorization / Execution / Effect Separation | semantische RM01-Abhängigkeit, durch RM01 nicht eigenständig evidenziert |
| `ACCORD-C04 v0.2` | Bounded Historical Reconstruction Discipline | semantische RM01-Abhängigkeit, durch RM01 nicht eigenständig evidenziert |
| `ACCORD-C05 v0.3` | Bounded Historical Execution Lineage | **R0 — PROJECT-ATTESTED via ACCORD-RM01** |

Der vollständige Claim Contract steht in [`CLAIMS.md`](CLAIMS.md).

### Keine Evidence-Vererbung

Evidence für einen Claim beweist nicht automatisch einen anderen Claim.

C05 benötigt C03 und C04 zur semantischen Interpretation. Der aktuelle RM01 Evidence
Record ist trotzdem ausschließlich **C05** zugeordnet.

## Fail-closed Claim-Disziplin

Für die öffentlichen Claims gilt gemeinsam:

> Fehlende, mehrdeutige, widersprüchliche, veraltete, nicht anwendbare oder sonst
> ungeklärte Unterstützung darf nicht still zur entsprechenden positiven Aussage werden.

Bei historischen Reconstruction Claims muss ein positives Resultat Evidence-Sufficiency
also **verdienen**. Sie wird nicht als Assumption vorausgesetzt.

## Aktuelle öffentliche Referenz

Die private Referenz wird öffentlich nur über den Alias

`ACCORD-RM01`

bezeichnet.

Status: **PROVISIONALLY FROZEN**

Evidence Level: **R0 — PROJECT-ATTESTED**

Der aktuelle Evidence Record ist an **ACCORD-C05 v0.3** gebunden. Das Evidence Package
behauptet ausdrücklich keine öffentliche Reproduktion der privaten Implementierung.

Siehe [`evidence/`](evidence/).

## Challenge ACCORD

Das Clean-Room-Challenge-Format liegt unter [`challenge/`](challenge/).

Eine standardisierte Registered-Falsification-Challenge bindet an:

- einen Claim;
- eine Claim Revision; und
- eine veröffentlichte Falsification ID.

Für einen plausiblen Claim-Widerspruch, der durch keine bestehende Falsification ID
sauber ausdrückbar ist, gibt es zusätzlich den Lifecycle-Pfad
`NOVEL_FALSIFICATION_HYPOTHESIS`. Dieser greift die Vollständigkeit der öffentlichen
Falsification Surface an. Ein unvorhergesehener Mechanismus ist für sich genommen keine
neue normative Bedingung: Er bleibt zulässig, wenn er einen Widerspruch zu bereits
vorhandenem normativem Inhalt der veröffentlichten Claim Revision behauptet. Nicht
zulässig ist dagegen, über diesen Pfad eine Anforderung hinzuzufügen, die die
veröffentlichte Claim Revision nie aufgestellt hat.

Der kanonische öffentliche Intake für nicht-sensitive Research Challenges ist ein
GitHub Issue in diesem Repository, dessen Titel mit `[ACCORD CHALLENGE]` beginnt. Public
Receipt und Pending Status werden durch
[`challenge/LIFECYCLE-CONTRACT.md`](challenge/LIFECYCLE-CONTRACT.md) und
[`challenge/receipts/`](challenge/receipts/) geregelt. Es wird keine feste
Adjudication-SLA behauptet; Receipt- und Status-Zeitstempel machen das Alter offener
Challenges extern sichtbar.

Ein erfolgreicher Standard-Harness-Lauf bedeutet ausschließlich:

```text
status = WELL_FORMED_CHALLENGE_SUBMISSION
scope_position = <Position des Einreichers>
judgment = NOT_PERFORMED
```

Der Harness entscheidet weder, ob der Einreicher recht hat, noch ob die Challenge
tatsächlich im Scope liegt oder ein Claim falsifiziert wurde.

Generische Attack Tags sind nur Ordnungsmetadaten. Sie beschränken nicht, mit welchem
Mechanismus ein Claim angegriffen werden darf.

Abgeschlossene inhaltliche Challenge-Entscheidungen werden durch
[`challenge/ADJUDICATION-CONTRACT.md`](challenge/ADJUDICATION-CONTRACT.md) geregelt und
unter [`challenge/adjudications/`](challenge/adjudications/) registriert. Review
Provenance und finale Decision Authority bleiben getrennt. Die aktuelle finale
Authority-Klasse ist ausdrücklich `PROJECT_MAINTAINER`; PROJECT ACCORD behauptet kein
unabhängiges Tribunal. Korrekturen erzeugen superseding Records, statt frühere
Adjudications still umzuschreiben. Eine `CONFIRMED_FALSIFICATION` oder ein
`CONFIRMED_CONTRACT_GAP` erfordert eine öffentliche Konsequenz für die betroffene Claim
Revision; dieselbe betroffene Revision darf nicht `PUBLISHED` bleiben.

## Reproduction Levels

- **R0 — PROJECT-ATTESTED:** begrenzte Projekt-Attestation auf eine private Referenz.
- **R1 — PUBLICLY CHALLENGEABLE:** öffentliche Claims und Challenge Surface erlauben
  strukturierte externe Gegenbeispiele und Contract-Gap-Hypothesen.
- **R2 — PUBLICLY REPRODUCIBLE:** die relevante Verification kann ohne privaten Zugriff
  unabhängig ausgeführt werden.

Der aktuelle öffentliche Claim-, Intake-, Lifecycle- und Adjudication-Surface erfüllt die
R1-Publication-Bedingung, solange diese Artefakte öffentlich zugänglich bleiben. R1
bedeutet **nicht** öffentlichen Execution-Zugriff auf, Simulation von, öffentliche
Trace-Erzeugung aus oder unabhängige Reproduktion der privaten Referenzimplementierung.
Eine externe empirische Erzeugung von Private-Reference-Traces wird derzeit nicht
behauptet.

Diese Ebenen dürfen nicht miteinander verschmolzen werden.

## Was ACCORD-RM01 nicht beweist

Der aktuelle Record beweist für sich genommen nicht:

- present Authority;
- erfolgreiche Target Invocation;
- realen Effect;
- Outcome Confirmation;
- universelle kausale Vollständigkeit;
- Formal Verification;
- Production Readiness;
- die Abwesenheit unbekannter Defekte; oder
- C01–C04 als allgemein eigenständig evidenzierte Claims.

## Disclosure Boundary

PROJECT ACCORD folgt dieser Regel:

> **Veröffentliche, was gelten muss, wo es gelten muss und wie es falsifiziert werden kann
> — nicht den privaten Mechanismus, der es wahr macht.**

Siehe:

- [`docs/PUBLIC-DISCLOSURE-MODEL.md`](docs/PUBLIC-DISCLOSURE-MODEL.md)
- [`docs/MINIMUM-DISCLOSURE.md`](docs/MINIMUM-DISCLOSURE.md)

## Forschungsmethode

**verdichten → angreifen → implementieren → erneut angreifen → freeze**

Lokale Tests sind allein keine freeze-grade Evidence. Der Publication Freeze benötigt
eine exakte committed Public-Candidate-Revision und dazugehörige CI Evidence.

## Repository-Struktur

```text
PROJECT-ACCORD/
├── README.md
├── CLAIMS.md
├── SECURITY.md
├── CONTRIBUTING.md
├── claims/
│   ├── public-claim-index.json
│   ├── public-claim-index.schema.json
│   ├── public-claim-state.json
│   └── public-claim-state.schema.json
├── docs/
├── challenge/
│   ├── ATTACK-CONTRACT.md
│   ├── LIFECYCLE-CONTRACT.md
│   ├── ADJUDICATION-CONTRACT.md
│   ├── receipts/
│   └── adjudications/
├── evidence/
└── tests/
```

Das Public-Surface-Repository steht unter der Apache License 2.0 (`Apache-2.0`). Die
Lizenz gilt für die Dateien dieses Repositories; getrennte private oder unveröffentlichte
PROJECT-ACCORD-Materialien gehören nicht zum lizenzierten Work, sofern sie nicht
ausdrücklich unter Apache-2.0 oder einer anderen angegebenen Lizenz verteilt werden.
Siehe [`LICENSE`](LICENSE) und [`LICENSE-SCOPE.md`](LICENSE-SCOPE.md).

Allgemeine externe Code-/Dokument-Contributions bleiben geschlossen, bis sie nach den
Regeln in [`CONTRIBUTING.md`](CONTRIBUTING.md) ausdrücklich geöffnet werden.

Vertrauliche Security-Reports können an `project_accord@proton.me` gesendet werden.
Repository-natives Private Vulnerability Reporting ist nach dem Public Release als
zusätzlicher Kanal vorgesehen.
