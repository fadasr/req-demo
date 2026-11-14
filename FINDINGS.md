# What this demo found

One corpus, measured on 2026-11-14 with `req 0.1.0` (rules_v 9, built from `dd78c81`), then
re-verified on 2026-11-15 with `cc35d81` (latest `main` plus PR #86), same rules_v 9 and no
address moved, and the Sphinx-Needs demo at `3c602bf`. These are observations from **one** real
project, not a benchmark; where a number is a count, the command that produced it is named.

## Fixed: typed links were dropped, so traceability was empty

**Observation.** 134 of the 135 drafted needs carried typed links in the export; the importer
wrote `relations: []` for every one. `req trace` on the imported corpus said:

```text
## Edges
(none)
## Incoming (derived)
(none)
```

The `not carried` report line named the link fields (`derives_from`, `implements`, `links`,
`reqs`, …) and counted the needs, but an adopter had to rebuild 220 edges by hand.

**Change.** [`req#86`](https://github.com/autox-my/req/pull/86) adds `--links`: an edge whose
target is also drafted in the same run becomes a `relations:` entry (`type` = source link field,
`to` = the target's claim id). Backlinks are not duplicated (req stores an edge once), link
filters (`<id>[version==1]`) are stripped, and every target that cannot be carried is counted by
reason instead of vanishing.

**After.** `req trace` stores 220 edges, 66 targets receive one, and `req impact REQ-0038`
(the lane-marking stakeholder need) walks the chain:

```text
7 dependent(s), nearest first:
- REQ-0046  distance 1  applies
- REQ-0047  distance 1  applies
- REQ-0086  distance 2  applies
...
```

## Fixed: test evidence was dropped from the import

**Observation.** The upstream has 69 test needs with real JUnit reports; the tests link to the
requirements they prove (`specs`/`links`) and to test runs. The importer correctly does not draft
test needs as requirements, but the **evidence links** were lost with them. After a plain import,
all 134 applying claims had no linked test, so `req gate --test-report` answered:

```text
[UNVERIFIABLE] tests_linked
  counts: 134 applying · 0 linked · 134 unlinked · 0 passed · 0 failed
```

**Change.** `--tests <junit.xml> --test-type test --test-link specs --test-link links` joins a
JUnit `<testcase>` to the test need it names (Sphinx-Test-Reports writes the test need's id as
`name`) and the test need to the draft its link field points at, writing `classname::name` into
the draft's `tests:`. The report counts cases that are malformed, cases that name no test need,
test needs with no case, and targets that are not drafts. A failing case is linked all the same —
the gate is what reports it.

**After.** The demo's 13 linked claims use both committed reports — 4 Coffee Machine claims whose
unit tests pass, and 9 ADAS claims whose SYS.5 qualification has three failures and one skip:

```text
counts: 134 applying · 13 linked · 121 unlinked · 4 passed · 9 failed · 0 not in the report
verdict: FAIL — a defect in a claim this variant includes
```

With no report (the default `req check`), the same links are **UNVERIFIABLE**: the evidence
cannot be judged, which is the honest answer, not a pass.

**This is the adoption cost, not a req defect.** A claim with no proven test is exactly what
`UNVERIFIABLE` is for, and a claim whose test fails is exactly what `FAIL` is for. The limit is
the namespace: `name` must be the test need id, and a case that does not match is counted, never
guessed at.

## Worked: the V-model as three req views

The upstream puts requirements, architecture/design, code and tests on one traceability page.
req keeps three checkable views, and the demo now populates all three:

| edge | req mechanism | this corpus |
| --- | --- | --- |
| requirement ↔ requirement | claim `relations` | 220 edges |
| requirement ↔ architecture/design/code | `req-satisfies:` + `req satisfy` | 26 elements, 56 links, all HOLD |
| requirement ↔ test | claim `tests:` | 16 links on 13 claims |

`scripts/build-design.py` turns the upstream `arch`, `swarch`, `component` and two annotated C
files into design elements; `scripts/record-satisfaction.sh` records the links; and
`scripts/build-trace-matrix.py` joins the three views into `docs/traceability.md`. The matrix
shows, per area, each claim's design/code elements, tests and derived requirements, plus the
coverage gaps.

The matrix is `docs/traceability.md`; the same shape as a rendered architecture graph is
`docs/v-model.html`, built with archify from `docs/v-model.archify.json` (delivery and automated
browser checks pass at 1440×900 and 2048×1320).

The one honest limit: **design ↔ design is not a req edge.** `ARCH_001 → SWARCH_001 → IMPL_LKA_*`
is flattened — all three satisfy the same requirement — because a design-to-design relation
would make architecture needs into claims, which they are not.

## Open: the variant requirements are the ones the importer skips

**Observation.** The upstream's variant showcase is `REQ_017` (maximum speed, field
`max_speed: 130` vs `75`) and `REQ_018` (warning side). Both are skipped as `rst role`, because
their content keeps the template text:

```text
The adaptive cruise control shall not exceed the configured maximum speed
of <{ var.region.speed_limit_highway }> :variant:`region.speed_unit` ...
```

The *resolved* values are in custom fields (`max_speed`, `speed_unit`, `driver_side`), not in the
content, and the export does not declare which template variable produced which field. Expanding
them would be a guess about the project's convention, so the importer names and skips them.

**What the demo does instead.** The left/right turn-signal pair is modeled as two claims with
authored applicability (`steering_side == left` / `== right`), and `.req/variants` gates both
contexts. `REQ-0136` was authored from the `eu_right` build, where the upstream's conditional
block includes it. This is the intended req workflow: variants are selectors, not forks, and the
person writes the selector.

`req select` decides every claim in both contexts, and `req check` runs both gates in one verdict.
A claim a context cannot decide would be **UNKNOWN**, never silently excluded; this corpus has
none because the two variant claims are the only selectors.

## The authoring pass: 80 unstructured → 39

**Observation.** The upstream's requirements are written as tasks ("Develop a lane detection
algorithm…", "Implement turn signal logic…") or as sentence clusters with two obligations. On the
first import `req canon` read **80 of 135 unstructured** (59%), and the split was by example: ISO
26262 Safety 41/74, Coffee Machine 7/8, Automotive ADAS **7/53**. The ADAS prose was the problem,
and it is the example with the most requirements.

**Change.** The 45 ADAS task statements were re-worded as obligations ("Develop software to process
camera inputs…" → "The lane detection software shall process camera inputs…"), without inventing
bounds; the two variant claims kept their `steering_side` selectors. `req canon` now reads **39
unstructured** (29%), and ADAS is **48/53 structured**. The 39 that remain are honest: ISO FSR
23/36, ISO system requirements 10/18, Coffee Machine one multi-paragraph gap, and five ADAS
statements whose lints (`untestable_qualifier` on "smooth"/"robust", `uncovered_content`,
`multiple_obligations`) need a person to decide a bound or a split.

**Consequence.** Drift-and-direction now applies to 96 claims instead of 55. The demo's drift case
uses `REQ-0115`, which was already structured:

```text
The software shall continuously monitor water temperature and trigger an emergency
shutdown within 100ms if temperature exceeds 100°C ...
```

Weakening `100ms` to `500ms` is classified **weakened** (a larger `LE` bound). The remaining 39
are `not-judged`, which is the honest answer; `req canon --by-area` names their areas.

## The subject registry: one subject per thing

`aliases/subjects.yml` starts as the `req init` starter (one `API` subject). The demo replaces it
with 30 domain subjects: the vehicle controllers (`VDC`/`the vdc`/`the vehicle dynamics
controller`, `WRDC`, brake, steering, drive), the software subsystems (lane detection, pedestrian
detection, parking, drowsiness, …), and the coffee machine. Registered surfaces become the subject
id — `the VDC` and `the vehicle dynamics controller` now parse as one subject — while an
unregistered surface stays literal.

This is a **registry version bump** (`version: 2`) and moves the addresses of the claims whose
subject resolved, exactly as a rules bump does. There is no signed Baseline in this demo, so there
is no re-ratification to run; a real corpus would see the movement as drift against its manifest.

## Not a defect: source statuses are deliberately not carried

The export has `open` / `in progress` / `closed`, authors, releases, ASIL, tags and Jira ids. The
importer writes none of them: a source status is not a ratification, and req's authority is a
signed Decision or a signed Baseline. `req check` therefore says `no signed Baseline under
baselines/: nothing in this repository is ratified`, which is true. The demo leaves it that way;
signing needs a maintainer's key, not a demo script.

## Worked: the importer's accounting is auditable

`needs 362 = drafted 135 + skipped 8 + not selected 219` is a line you can check against the
export by hand. The eight skips are named one per reason, and the 219 are broken down by type.
The demo deletes one of the 135 drafts (`EX_REQ_002`, "Some content" — a documentation example,
not an obligation), which is the point of a draft.

`--areas` filed the drafts under 9 source documents, and `req check` reads the registry: the
demo's only completeness edits are the three declared roots in `.req/completeness` — the two
variant claims, and `REQ-0062` (the coffee machine's top-level "brew coffee" requirement, whose
only downstream requirement upstream is `SWREQ_BREW_STRENGTH`, one of the eight skipped needs).
Without the roots, `req check` names them as unrelated; it reports, it does not judge.

The two committed projections (`docs/spec.md`, `docs/trace.md`) load and verify as current in
`req check`, which is the cheap way to keep a deliverable honest: regenerate, never hand-edit.

## What I would change next, in order

1. **A design-element view** — `req satisfy` lists links, but design elements are not nodes in
   `req trace`; the demo's matrix joins them outside req. If adopters need the upstream's
   design ↔ design graph, that is a new view and an ADR, not a patch.
2. **A documented variant-expansion recipe** — not a flag. The export has the resolved fields;
   the missing piece is the project's convention, which belongs in a project-local script like
   `adopt.py`, not in req's core.
3. **A test-report reader for other generators** — the `--tests` join assumes Sphinx-Test-Reports
   (`name` = test need id). Another generator's report is deliberately counted, not converted;
   a mapping flag would be the next step if an adopter needs it.

The canon work list suggested here is now [`req#89`](https://github.com/autox-my/req/pull/89):
`req canon --by-area` put the authoring pass in order (ADAS software requirements 0/29 structured,
ADAS SYS.2 0/16, ISO FSR 13/36) and now shows the result: ADAS software requirements 27/29, ADAS
SYS.2 14/16, ISO FSR 13/36 — the remaining work is the ISO examples.
