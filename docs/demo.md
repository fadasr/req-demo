# A tour in nine commands

This is a transcript of the demo, with the interpretation each output is meant to carry. The
corpus is already built; `README.md` says how to rebuild it. Every command runs offline.

The upstream is four examples, and they land very differently: ISO 26262 Safety supplies 74
claims (41 structured, 171 edges), Automotive ADAS 53 (7 structured, 44 edges), Coffee Machine 8
(7 structured, 5 edges), and the Basic Example none — its objects are feature demos, imported
needs with no content, and external needs that an export does not contain. The Basic Example is
still part of the demo: it is what "reject the draft" looks like.

## 1. What came in

```console
$ python3 tools/needs_import.py --from build/needs.json \
    --origin https://github.com/useblocks/sphinx-needs-demo@3c602bf \
    --date 2026-11-14 --type req --type sysreq --type swreq --type fsr \
    --type safety_goal --type need --links --areas --area-depth 2 \
    --tests data/coffee_machine_junit.xml --tests data/adas_junit.xml \
    --test-type test --test-link specs --test-link links
...
not carried: asil, constraints, ... status, tags, title, ...; typed links on 134 of 135
drafted needs (...) — carried as `relations`
links: 220 relation(s) on 101 of 135 drafted needs
       (derives_from 152, implements 19, links 44, reqs 5);
       119 target(s) not carried (self 2, target skipped 1, target type not selected 116)
tests: 16 test link(s) on 13 of 135 drafted needs; 69 test need(s) (8 with a case, 61
       without); 10 test case(s) (6 passed, 3 failed, 1 skipped, ...); 1 target(s) not carried
needs 362 = drafted 135 + skipped 8 + not selected 219
           (by type: arch 10, ... test 69, ...)
```

Read the last line first. 362 needs in, 135 proposals out, 8 named skips, 219 not selected and
counted by type. The importer never says "ignored"; every need has an outcome. The 116 link
targets it cannot carry are mostly architecture and implementation needs — not requirements, so
no claim id exists to point at. Those are design elements, not claims; section 10 maps them with
`req-satisfies:` instead.

## 2. What the prose actually is

```console
$ req canon | tail -1
claims: 135 (39 unstructured); pins: 3 on 1 claim(s), 0 flagged; lints on 22 claim(s)
```

After the authoring pass, 39 of 135 statements have no modality req can hold (it was 80). The
remaining ones are honest: the ISO FSRs and system requirements are sentence clusters, and a few
ADAS qualifiers ("smooth", "robust") need a person to state a bound.

`req canon --by-area` (landing in [`req#89`](https://github.com/autox-my/req/pull/89)) showed the
work in order: ADAS software requirements **0 of 29** structured, ADAS SYS.2 **0 of 16**, ISO FSRs
**13 of 36** — and after the pass: **27 of 29**, **14 of 16**, ISO still **13 of 36**. The work
list now points at the ISO examples.

## 3. The traceability matrix

```console
$ req trace | sed -n '/## Edges/,+6p'
## Edges
- REQ-0002 -derives_from-> REQ-0080
- REQ-0002 -derives_from-> REQ-0081
...
```

`REQ-0002` is an FSR; its `derives_from` edges point at the safety goals it decomposes. Before
`--links` this section said `(none)` — the export had the edges, the importer did not write them.

## 4. What a change touches

```console
$ req impact REQ-0038
# Impact: REQ-0038
7 dependent(s), nearest first:
- REQ-0046  distance 1  applies
...
```

`REQ-0038` is the stakeholder need "The system shall detect lane markings…"; the traversal is the
incoming side of the same edges, which req derives rather than stores.

## 5. Two vehicles, one model

```console
$ req select steering_side=right
...
REQ-0136  applies
applies 135, does not apply 1, unknown 0

$ req select steering_side=left
REQ-0113  applies
applies 135, does not apply 1, unknown 0
```

The upstream builds a different document per variant. Here the two turn-signal claims are the
same corpus, selected by a context; neither is a branch. `unknown 0` is the interesting number:
every claim is decided for both contexts. If a claim had a selector the context does not mention,
it would be `UNKNOWN`, not excluded.

## 6. The gate, and its honest answer

```console
$ req gate steering_side=left --test-report data/coffee_machine_junit.xml
...
[PASS] design_satisfied
  ... (counts: 57 link(s) judged · 57 holding · 0 weakened)
[UNVERIFIABLE] tests_linked
  counts: 134 applying · 13 linked · 121 unlinked · 4 passed · 0 failed · 9 not in the report
verdict: UNVERIFIABLE — nothing is wrong, but something cannot be confirmed
```

```console
$ req gate steering_side=left \
    --test-report data/coffee_machine_junit.xml --test-report data/adas_junit.xml
...
[FAIL] tests_linked
  - REQ-0046: linked test failed: com.example.tests.ExampleTest::TEST_SYS_QUAL_001
  counts: 134 applying · 13 linked · 121 unlinked · 4 passed · 9 failed · 0 not in the report
verdict: FAIL — a defect in a claim this variant includes
```

`UNVERIFIABLE` is not a shy PASS and not a FAIL. With one report, four claims pass and nine cannot
be confirmed because their report was not supplied. With both, nine claims are linked to three
failing qualification cases, and the gate says **FAIL** — the policy doing its job. `req check`
runs no report by default, so it stays UNVERIFIABLE; a CI step must go red on exit 3 (see req's
own workflow template), which is how "we could not tell" stays visible.

## 7. The whole repository in one verdict

```console
$ req check
[UNVERIFIABLE] gate steering_side=left (exit 3)
[UNVERIFIABLE] gate steering_side=right (exit 3)
[UNVERIFIABLE] completeness structural omissions (4 checks) (exit 3)
    no signed Baseline under baselines/: nothing in this repository is ratified
[PASS] render docs/spec.md (exit 0)
[PASS] trace docs/trace.md (exit 0)
...
verdict: UNVERIFIABLE
```

Both declared variants ran, both committed projections are current, and completeness ran once over
the union. The absent Baseline is the expected answer for a demo without a signing key: `req`
never signs, a human does. `docs/spec.md` and `docs/trace.md` are generated deliverables, not
caches: `req check` fails if either was hand-edited or left stale.

## 8. A meaning change, not an edit

```console
$ scripts/demo-drift.sh
...
== req diff --base HEAD~1 (the weakening is a change in meaning, not an edit)
# req diff: HEAD~1 -> working-tree
registry: unchanged
weakened REQ-0115 numeric_loosening pin-flagged
counts: added 0, removed 0, weakened 1, tightened 0, reshaped 0, not-judged 0,
        reworded 0, metadata 0, unchanged 134
```

The script clones the corpus into a temporary directory, changes `100ms` to `500ms`, and asks
`req diff`. The class is `weakened` because `LE` with a larger bound is a looser obligation. The
pin still says `0.1 s`, so the change is also `pin-flagged`: the authored intent did not move, the
statement did, and the next gate fails `pins_hold` (`pin value 0.1 contradicts the parse (0.5)`)
until a person decides which one is right.

## 9. What is still a proposal

```console
$ req audit | head -8
# Audit packet
selection: (none)
claims: 133 applying, 2 undecided, 0 excluded
baseline: none supplied — nothing in this packet is ratified, and this is a manifest
          of intent, not an audit of authority
```

Every claim is a draft. The importer wrote statements and provenance; a human still has to
re-word the unstructured ones, link the tests, and sign a Baseline. That is the adoption loop, and
the demo is designed to make the size of that work visible rather than to hide it.

## 10. The V-model: requirement ↔ design/code ↔ test

The upstream's traceability page links requirements to architecture, design, code and tests. req
keeps three views, and the demo now fills all three. The bridge is `req-satisfies:` in a design
file, read by `req satisfy` (ADR 0040):

```console
$ req satisfy
# req satisfy: 58 link(s) declared
[HOLDS] design/architecture/ARCH_001.md -> REQ-0046
[HOLDS] design/architecture/ARCH_001.md -> REQ-0047
...
[HOLDS] design/code/lane_keeping.c -> REQ-0088
[HOLDS] design/components/COMP_SAFETY_MON.md -> REQ-0115
verdict: PASS — every declared link holds
```

`design/` has one file per upstream `arch`, `swarch` and `component` need plus the two annotated C
files; each declares what it satisfies. `scripts/build-design.py` writes them from the export,
`scripts/record-satisfaction.sh` performs the human `--record` act, and `.req/satisfied` is the
committed record. A change to a claim's meaning re-opens the link: a loosening of an admitted
class is `HOLDS (weakened)`, anything else is `SUSPECT`.

```console
$ scripts/build-trace-matrix.py --out docs/traceability.md
135 claims · 45 with a design/code element · 13 with a linked test (16 test link(s)) ·
28 design element(s) · 220 requirement relation(s).
```

`docs/traceability.md` joins the three views: per area, each claim's design/code elements, its
linked tests and its derived requirements, then the coverage gaps. `docs/v-model.html` renders the
same shape as an architecture graph (`archify` from `docs/v-model.archify.json`), for the reader
who wants the picture rather than the table. `docs/components.html` is req's own
`arch_overlay.py` over a 10-component software map: every component is **HOLDS**, and
`component-coverage.md` is its claim-by-claim matrix. It is generated, not a req
projection, because req has no single command that merges external elements with claims.

One limit is stated rather than hidden: **design ↔ design is not a req edge.** The upstream chain
`ARCH_001 → SWARCH_001 → IMPL_LKA_*` is flattened — all three satisfy the same requirement — because
a design-to-design relation would turn architecture needs into claims.
