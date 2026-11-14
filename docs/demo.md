# A tour in nine commands

This is a transcript of the demo, with the interpretation each output is meant to carry. The
corpus is already built; `README.md` says how to rebuild it. Every command runs offline.

## 1. What came in

```console
$ python3 tools/needs_import.py --from build/needs.json \
    --origin https://github.com/useblocks/sphinx-needs-demo@3c602bf \
    --date 2026-11-14 --type req --type sysreq --type swreq --type fsr \
    --type safety_goal --type need --links --areas --area-depth 2
...
not carried: asil, constraints, ... status, tags, title, ...; typed links on 134 of 135
drafted needs (...) — carried as `relations`
links: 220 relation(s) on 101 of 135 drafted needs
       (derives_from 152, implements 19, links 44, reqs 5);
       119 target(s) not carried (self 2, target skipped 1, target type not selected 116)
needs 362 = drafted 135 + skipped 8 + not selected 219
           (by type: arch 10, ... test 69, ...)
```

Read the last line first. 362 needs in, 135 proposals out, 8 named skips, 219 not selected and
counted by type. The importer never says "ignored"; every need has an outcome. The 116 link
targets it cannot carry are mostly architecture and implementation needs — not requirements, so
no claim id exists to point at.

## 2. What the prose actually is

```console
$ req canon | tail -1
claims: 135 (80 unstructured); pins: 3 on 1 claim(s), 0 flagged; lints on 20 claim(s)
```

80 of 135 statements have no modality req can hold. That is the corpus, not the tool: it is
written as tasks and sentence clusters. The 20 lints are the first authoring work list.

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
$ req gate steering_side=left \
    --test-report upstream/docs/testsuites/coffee_machine_junit.xml
[PASS] pins_hold
[PASS] relations_resolve
[PASS] dependencies_decided
[PASS] rationale_present
[UNVERIFIABLE] tests_linked
  counts: 134 applying · 3 linked · 131 unlinked · 3 passed · 0 failed · 0 not in the report
...
verdict: UNVERIFIABLE — nothing is wrong, but something cannot be confirmed
```

`UNVERIFIABLE` is not a shy PASS and not a FAIL. The structural policies pass; the evidence policy
cannot be confirmed for 131 claims. The demo linked three coffee-machine claims by hand to show a
`passed` outcome. A CI step must go red on exit 3 (see req's own workflow template), which is how
"we could not tell" stays visible.

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
# req diff: HEAD~1 (51645d452996) -> working-tree
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
