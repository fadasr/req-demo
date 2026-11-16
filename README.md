# req-demo: a real Sphinx-Needs corpus put through req

**Live demo:** https://fadasr.github.io/req-demo/

This repository is a **demonstration corpus**, not a product: it takes the
[`useblocks/sphinx-needs-demo`](https://github.com/useblocks/sphinx-needs-demo) documentation —
its four examples: Basic, Coffee Machine, Automotive ADAS, ISO 26262 Functional Safety — and runs
it through [`req`](https://github.com/autox-my/req): import, canonicalization, traceability, variants,
drift, gate, audit.

The point is to **pressure-test req on other people's prose** and turn what hurts into small
changes. The importer now carries typed links (`--links`) and JUnit evidence (`--tests`)
(released in `rev-3294a46`, PR [#86](https://github.com/autox-my/req/pull/86)), because without them
this corpus had 220 trace edges, an empty traceability matrix, and no test evidence. See
[`FINDINGS.md`](FINDINGS.md) for everything the demo exposed.

## What is here

| path | what |
| --- | --- |
| `claims/` | 135 req claims, drafted from the export and then edited (one rejection, two variant claims, 16 test links on 13 claims, one pin) |
| `.req/areas` | the reading layout, one area per source document |
| `.req/variants` | `steering_side=left` and `steering_side=right`, the upstream's vehicle variants as selectors |
| `.req/completeness` | the variant roots and the orphaned coffee-machine root, declared unrelated on purpose |
| `.req/projections` | the two committed views `req check` verifies |
| `.req/design`, `.req/satisfied` | the design roots and the recorded `req-satisfies:` links (ADR 0040) |
| `design/` | 26 architecture, component and code elements, each declaring what it satisfies |
| `docs/spec.md`, `docs/trace.md` | generated projections; never edited by hand |
| `docs/traceability.md` | the full V-model matrix: requirement ↔ design/code ↔ test |
| `docs/v-model.html` | a rendered architecture graph of the same three views (`archify`) |
| `docs/components.html` | the req-native component overlay: `arch_overlay.py` colors each software component by its satisfaction outcome |
| `docs/index.html`, `docs/matrix.html` | the GitHub Pages landing page and global matrix |
| `docs/explorer.html` | req's coverage explorer over the claim/design/test graph (ADR 0054) |
| `docs/variants.html` | req selectors vs Sphinx-Needs variant builds, including architecture/design/code |
| `docs/comparison.html` | the bounded req vs Sphinx-Needs evaluation |
| `docs/<project>/` | one page, requirement graph and (where it exists) component overlay per upstream example |
| `component-coverage.md` | the overlay's coverage matrix, one row per claim |
| `docs/components.archify.json` | the component diagram the overlay is built from |
| `docs/design.md` | how `design/` maps to `req satisfy`, and the token trap |
| `tools/needs_import.py` | the importer from req, at the commit that added `--links` and `--tests` |
| `tools/req-graph/` | req's graph converters, copied at the same release |
| `tools/explorer/` | req's coverage-explorer builder, adapted to this site |
| `data/` | the two upstream JUnit reports, committed so the test links are reproducible |
| `scripts/` | rebuild, import, design build, satisfaction record, trace matrix, project graphs, site, drift |

## The site

The demonstration is a static GitHub Pages site: **https://fadasr.github.io/req-demo/**. It is
built from the checked JSON views, not from prose:

```bash
req trace --format json > build/trace.json
req satisfy --format json > build/satisfy.json
scripts/fetch-archify.sh                  # archify 7e45f36, the pin req's graph tools name
python3 scripts/build-project-graphs.py   # docs/<project>/graph.html + components.html
scripts/fetch-req.sh                      # req rev-3294a46 (macOS arm64 pin)
python3 tools/explorer/build.py --req build/req-release/req --out docs/explorer.html
python3 scripts/build-site.py             # docs/index.html, docs/matrix.html, project pages
```

`.github/workflows/pages.yml` deploys `docs/` on every push to `main`.
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
| 🚗 Automotive ADAS | 53 | 48 | 44 | stakeholder needs + SYS/SWE requirements + one authored right-hand-drive variant claim; the task-style prose was re-worded into obligations; 9 qualification test links, 3 failing |
| 🛡️ ISO 26262 Safety | 74 | 41 | 171 | HARA → safety goals → FSR → system-requirement chain; the best-structured example, and most of the corpus's edges |
| **total** | **135** | **96** | **220** | |

The Basic Example is deliberately zero claims. Its Sphinx-Needs objects demonstrate directives,
filtering, imported needs and external needs; none of them is an obligation a person would
ratify. The importer drafts `EX_REQ_002` and a human rejects it — that rejection is part of the
demo, not a gap.

## The V-model, as req can express it

The upstream's traceability page links requirements to architecture, design, code and tests.
req keeps those as three separate, checkable views rather than one graph:

| edge | req mechanism | this corpus |
| --- | --- | --- |
| requirement ↔ requirement | claim `relations` | 220 edges (`req trace`) |
| requirement ↔ architecture / design / code | `req-satisfies:` in a design file | 28 elements, 58 links (`req satisfy`) |
| requirement ↔ test | claim `tests:`, a JUnit `classname::name` | 16 links on 13 claims |

`design/` holds the translation: one file per upstream `arch`, `swarch` and `component` need, plus
the two annotated C files, each declaring the claims it satisfies ([details](docs/design.md)).
`scripts/record-satisfaction.sh` is the human act (`req satisfy --record`) that writes
`.req/satisfied`; all 58 links **HOLD**.

```bash
scripts/build-design.py --write           # (re)write design/ from the export
scripts/record-satisfaction.sh            # record every req-satisfies: link
req satisfy                               # 58 links declared, verdict PASS
scripts/build-trace-matrix.py --out docs/traceability.md
```

`docs/traceability.md` joins the three views into the matrix a reader expects: per area, each
claim's design/code elements, linked tests and derived requirements, plus the coverage gaps.
`docs/explorer.html` is req's coverage explorer: one claim across source, design and tests, with
area/outcome filters, search and the gaps named (ADR 0054).
`docs/v-model.html` is the same shape as a rendered architecture graph, built with
[`archify`](https://github.com/tt-a1i/archify) from `docs/v-model.archify.json`; it is a reader's
view, not a req projection.

The req-native version is `docs/components.html`, produced by req's own
[`tools/graph/arch_overlay.py`](https://github.com/autox-my/req/blob/main/tools/graph/arch_overlay.py)
from `docs/components.archify.json`, `req satisfy --format json` and `req trace --format json`.
Each of the 11 software components cites the design files it is built from; the overlay sets its
status to the worst satisfaction outcome and lists the claims. All 10 are **HOLDS**, with 1–5
claims each; `component-coverage.md` is the tool's claim-by-claim matrix. It was validated,
delivered and browser-checked by archify **7e45f36** (the version req pins).

There is one honest limit: **design ↔ design is not a req edge.** The upstream chain
`ARCH_001 → SWARCH_001 → IMPL_LKA_*` is flattened — the arch file, the swarch file and the C file
all satisfy the same requirement, and the matrix shows them side by side. A design-to-design
relation would make the architecture needs claims, which they are not.

The tests are real, and so is the failure: 4 Coffee Machine claims pass their unit tests, while
9 ADAS claims are linked to the SYS.5 qualification report, whose three failing cases and one
skipped case make `req gate` **FAIL**:

```bash
req gate steering_side=left \
  --test-report data/coffee_machine_junit.xml --test-report data/adas_junit.xml
# counts: 134 applying · 13 linked · 121 unlinked · 4 passed · 9 failed · 0 not in the report
# verdict: FAIL — a defect in a claim this variant includes
```

With no report (the default `req check`), those links are **UNVERIFIABLE**, not a pass: the
evidence cannot be judged, so the gate says so.

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

`req` must be on `PATH` (this demo was drafted with `req 0.1.0`, rules_v 9, and is now built and
re-verified with the `rev-3294a46` release; same rules_v 9, and no address or projection moved.
`req --version` is the provenance). The importer refuses to draft over an
existing corpus, so a fresh import means a fresh `claims/`:

```bash
req init                                  # only for a fresh corpus
scripts/build-upstream.sh
scripts/import.sh                         # types, --links, --tests, --areas; prints the accounting
req canon                                 # the parse each claim derives
scripts/build-design.py --write           # design/ from the arch/swarch/component/impl needs
scripts/record-satisfaction.sh            # record the req-satisfies: links
scripts/build-trace-matrix.py --out docs/traceability.md
req trace --format json > build/trace.json
req satisfy --format json > build/satisfy.json
scripts/fetch-archify.sh                  # only to regenerate the graph pages
python3 scripts/build-project-graphs.py
python3 scripts/build-site.py
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
tests: 16 test link(s) on 13 of 135 drafted needs; 69 test need(s) (8 with a case, 61 without);
       10 test case(s) (6 passed, 3 failed, 1 skipped, 0 malformed, 0 naming no test need)
       in data/coffee_machine_junit.xml, data/adas_junit.xml;
       1 target(s) not carried (target not drafted 1)
```

Eight selected needs are skipped, each named by reason by the importer: three reStructuredText
directives, two variant-templated requirements with `:variant:` roles, two empty imported needs,
and one multi-paragraph software requirement. That is the honest limit of "one plain paragraph",
not a bug: the skipped item is a decision for a person.

## What the corpus says

```bash
req canon                                  # 135 claims, 39 unstructured, 22 with lints
req canon --by-area                        # the work list: ISO FSR 13/36 structured
req trace | head -40                       # 220 stored edges, 66 targets receive one
req impact REQ-0038                        # 7 dependents, nearest first
req satisfy                                # 58 design/code links, all HOLD
req select steering_side=right             # REQ-0136 applies, REQ-0113 does not
req gate steering_side=left --test-report data/coffee_machine_junit.xml \
    --test-report data/adas_junit.xml      # FAIL: 4 passed, 9 failed
req check                                  # both variants, both projections, completeness
req audit                                  # coverage and provenance, unratified by design
```

Without a test report the gate's flagship answer is **UNVERIFIABLE**, and that is correct: 121
of 134 applying claims have no linked test, so `tests_linked` cannot be confirmed even though
every structural policy passes and all 58 design/code links HOLD. With the two real reports the
answer becomes **FAIL** — nine ADAS claims are linked to three failing qualification cases — which
is the policy doing its job, not a demo defect. The links can be drafted automatically:
`needs_import.py --tests <junit.xml> --test-type test --test-link specs` proposes them from the
test need's own links.

`req diff` is in `scripts/demo-drift.sh`: it clones this repository into a temporary directory,
weakens the 100 ms over-temperature shutdown to 500 ms, and asks req what moved:

```bash
scripts/demo-drift.sh
```

## The authoring pass: what is done, what remains

The import is a draft, never a ratification (ADR 0004).

**Done**
- **The ADAS prose** was re-worded into obligations: 48 of 53 structured, up from 7.
- **The subject registry** is curated: 30 subjects, `version: 2`; abbreviations and spelled-out
  controller names resolve to one subject.
- **The bounded pin** is demonstrated on `REQ-0115` (`LE 0.1 s`), and `req gate` holds it.
- **The test evidence** is carried by `--tests`; 13 claims are linked (4 Coffee pass, 9 ADAS fail
  on the real SYS.5 report).

**Remaining**
1. **Re-word the 39 unstructured claims** — ISO FSR 23/36 and ISO system requirements 10/18 are
   the work list, plus five ADAS qualifiers (`smooth`, `robust`, `multiple_obligations`). Lints on
   22 claims are the first edits; `req canon --by-area` is the plan.
2. **Pin more load-bearing bounds** — one pin is a demonstration, not a ratified set.
3. **Link the 121 claims with no test** — not every upstream test need has a JUnit report, so some
   of this is a test-authoring task, not a link task.

The variant comparison is written up in [`docs/variants.html`](docs/variants.html); the tool-level
list is [`FINDINGS.md`](FINDINGS.md#what-i-would-change-next-in-order).

## Licence and provenance

The requirements prose is from `sphinx-needs-demo` (MIT, see `upstream/LICENSE`); the claims here
keep the need id and the source commit in `rationale.source`. Everything generated from it is a
draft for a human to ratify. The demo repository itself adds only the scripts and notes.
