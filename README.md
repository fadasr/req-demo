# req-demo: a real Sphinx-Needs corpus put through req

This repository is a **demonstration corpus**, not a product: it takes the
[`useblocks/sphinx-needs-demo`](https://github.com/useblocks/sphinx-needs-demo) documentation —
its four examples: Basic, Coffee Machine, Automotive ADAS, ISO 26262 Functional Safety — and runs
it through [`req`](https://github.com/autox-my/req): import, canonicalization, traceability, variants,
drift, gate, audit.

The point is to **pressure-test req on other people's prose** and turn what hurts into small
changes. The first such change is [PR #86](https://github.com/autox-my/req/pull/86): the importer
now carries typed links with `--links`, because without it this corpus had 220 trace edges and an
empty traceability matrix. See [`FINDINGS.md`](FINDINGS.md) for everything the demo exposed.

## What is here

| path | what |
| --- | --- |
| `claims/` | 135 req claims, drafted from the export and then edited (one rejection, two variant claims, three test links, one pin) |
| `.req/areas` | the reading layout, one area per source document |
| `.req/variants` | `steering_side=left` and `steering_side=right`, the upstream's vehicle variants as selectors |
| `.req/completeness` | the variant roots and the orphaned coffee-machine root, declared unrelated on purpose |
| `.req/projections` | the two committed views `req check` verifies |
| `docs/spec.md`, `docs/trace.md` | generated projections; never edited by hand |
| `tools/needs_import.py` | the importer from req, at the commit that added `--links` and `--tests` |
| `data/coffee_machine_junit.xml` | the upstream JUnit report, committed so the test links are reproducible |
| `scripts/` | rebuild, import, and the drift walkthrough |
| `upstream/` | the source checkout (ignored; pinned by `scripts/build-upstream.sh`) |
| `build/` | generated reports (`needs.json`, command captures; ignored) |

## The four upstream examples

The upstream documentation is four examples, and they behave very differently under import. The
counts below are this corpus; `structured` means `req canon` derived a modality (the rest are
`UNSTRUCTURED` and can only be reported as `not-judged` by `req diff`).

| upstream example | claims | structured | trace edges | notes |
| --- | ---: | ---: | ---: | --- |
| 🧰 Basic Example | 0 | — | — | feature showcase, not obligations: `EX_REQ_002` is "Some content"; `EX_REQ_001` contains images and bold markup and is skipped as `rst directive`; the imported needs have no content; external needs are not in a Sphinx-Needs export at all |
| ☕️ Coffee Machine | 8 | 7 | 5 | system requirements + software requirements; `SWREQ_BREW_STRENGTH` is skipped (multi-paragraph); 7 JUnit test links on 4 claims |
| 🚗 Automotive ADAS | 53 | 7 | 44 | stakeholder needs + SYS/SWE requirements + one authored right-hand-drive variant claim; the task-style prose ("Develop…", "Implement…") is mostly unstructured |
| 🛡️ ISO 26262 Safety | 74 | 41 | 171 | HARA → safety goals → FSR → system-requirement chain; the best-structured example, and most of the corpus's edges |
| **total** | **135** | **55** | **220** | |

The Basic Example is deliberately zero claims. Its Sphinx-Needs objects demonstrate directives,
filtering, imported needs and external needs; none of them is an obligation a person would
ratify. The importer drafts `EX_REQ_002` and a human rejects it — that rejection is part of the
demo, not a gap.

## The source, pinned

```
repo    https://github.com/useblocks/sphinx-needs-demo
commit  3c602bfedf710d2304d22a93049d7233bba93285
build   sphinx-build -b html docs _build/html   (Sphinx-Needs 8.3, 2026-11-14)
```

The Sphinx-Needs build needs `graphviz` (`dot`) and `java` for PlantUML. Dependencies are
installed with `uv` from the upstream's `pyproject.toml`.

```bash
scripts/build-upstream.sh                 # clone + build; writes build/needs.json
scripts/build-upstream.sh eu_right        # the right-hand-drive variant; writes build/needs-eu_right.json
```

## Reproduce the corpus

`req` must be on `PATH` (this demo was drafted with `req 0.1.0`, rules_v 9, built from `dd78c81`;
it was re-verified with `cc35d81` — latest `main` plus PR #86 — same rules_v 9, and no address or
projection moved. `req --version` is the provenance). The importer refuses to draft over an
existing corpus, so a fresh import means a fresh `claims/`:

```bash
req init                                  # only for a fresh corpus
scripts/build-upstream.sh
scripts/import.sh                         # types, --links, --areas; prints the accounting
req canon                                 # the parse each claim derives
```

The import report on this export:

```text
needs 362 = drafted 135 + skipped 8 + not selected 219
           (by type: arch 10, component 8, hazard 1, impl 64, interface 9, layer 4, need 8,
            person 6, release 3, seq_msg 16, spec 3, swarch 11, team 1, test 69, testfile 2,
            testrun 10, testsuite 2)
links: 220 relation(s) on 101 of 135 drafted needs
       (derives_from 152, implements 19, links 44, reqs 5);
       119 target(s) not carried (self 2, target skipped 1, target type not selected 116)
tests: 7 test link(s) on 4 of 135 drafted needs; 69 test need(s) (4 with a case, 65 without);
       6 test case(s) (6 passed, 0 failed, 0 skipped, 0 malformed, 0 naming no test need)
       in data/coffee_machine_junit.xml;
       1 target(s) not carried (target not drafted 1)
```

Eight selected needs are skipped, each named by reason by the importer: three reStructuredText
directives, two variant-templated requirements with `:variant:` roles, two empty imported needs,
and one multi-paragraph software requirement. That is the honest limit of "one plain paragraph",
not a bug: the skipped item is a decision for a person.

## What the corpus says

```bash
req canon                                  # 135 claims, 80 unstructured, 20 with lints
req trace | head -40                       # 220 stored edges, 66 targets receive one
req impact REQ-0038                        # 7 dependents, nearest first
req select steering_side=right             # REQ-0136 applies, REQ-0113 does not
req gate steering_side=left --test-report data/coffee_machine_junit.xml
req check                                  # both variants, both projections, completeness; one verdict
req audit                                  # coverage and provenance, unratified by design
```

The gate's flagship answer is **UNVERIFIABLE**, and that is the correct answer here: 131 of 134
applying claims have no linked test, so `tests_linked` cannot be confirmed even though every
structural policy passes. The demo links four coffee-machine claims to the upstream's real JUnit
report (`4 linked · 4 passed · 0 failed`) to show the other side of the same policy. The links can
be drafted automatically now: `needs_import.py --tests <junit.xml> --test-type test --test-link
specs` proposes them from the test need's own `specs` links.

`req diff` is in `scripts/demo-drift.sh`: it clones this repository into a temporary directory,
weakens the 100 ms over-temperature shutdown to 500 ms, and asks req what moved:

```bash
scripts/demo-drift.sh
```

## The authoring pass this demo argues for

The import is a draft, never a ratification (ADR 0004). In this corpus the useful next edits are:

1. **Re-word the 80 unstructured claims** so they carry a modality and a bound. "Develop
   functionality to…" is a task, not an obligation; `req canon` lints it but never invents a
   `shall`. The 20 lint findings are the work list (`untestable_qualifier`, `multiple_obligations`,
   `uncovered_content`, …).
2. **Pin the load-bearing bounds** (the demo pins REQ-0115 at `LE 0.1 s`).
3. **Link the proving tests.** The upstream already carries JUnit reports; the demo maps three by
   hand because the importer cannot infer `classname::name` from a Sphinx-Needs test need.
4. **Curate the subject registry.** `aliases/subjects.yml` still holds the `req init` starter; the
   VDC/WRDC/steering vocabulary is exactly what a registry is for.

## Licence and provenance

The requirements prose is from `sphinx-needs-demo` (MIT, see `upstream/LICENSE`); the claims here
keep the need id and the source commit in `rationale.source`. Everything generated from it is a
draft for a human to ratify. The demo repository itself adds only the scripts and notes.
