# design/ (documented here, outside the design root)

req models a design element as a **file** that declares `req-satisfies: <claim-id>` (ADR 0040).
The upstream models architecture, software architecture, components and code as Sphinx-Needs
objects with typed links. This directory is the translation:

| upstream need type | here | link becomes |
| --- | --- | --- |
| `arch` | `architecture/<ID>.md` | the requirements the arch need links to |
| `swarch` | `architecture/<ID>.md` | the software requirements the swarch need links to |
| `component` | `components/<ID>.md` | the requirements the component implements |
| `impl` (the annotated C files) | `code/lane_keeping.c`, `code/acc.c` | the software requirements the file implements |

Each file carries one `<!-- req-satisfies: REQ-NNNN -->` (or `//` in C) per link. The ids are the
claims the importer drafted for the upstream need; `scripts/build-design.py` maps them by the
need id in each claim's `rationale.source`. `scripts/record-satisfaction.sh` then records every
declaration with `req satisfy --record`, which is the human act; `.req/satisfied` is the
committed record.

## What this shows, and what it does not

- **Requirement ↔ design/code** is a `req-satisfies:` link: `req satisfy` judges it by the
  direction of the claim's change since it was recorded. All 56 links HOLD here.
- **Requirement ↔ test** is the claim's `tests:`, a JUnit `classname::name`; 13 claims are
  linked (4 Coffee Machine passing, 9 ADAS qualification with three failures).
- **Design ↔ design** is **not** a req edge. The upstream's `ARCH_001 -> SWARCH_001 -> IMPL_LKA_*`
  chain is flattened: the arch element, the swarch element and the code file all satisfy the
  same requirement, and the matrix shows them side by side. A design-to-design relation would
  need a claim (a design obligation), and this demo does not pretend the architecture needs are
  requirements.
- Components with no requirement target (`COMP_ADC_DRV`, `COMP_GPIO_DRV`, `COMP_PWM_DRV`,
  `COMP_SPI_DRV`) and `COMP_BREW_CTRL` (whose requirement was skipped as multi-paragraph) are
  not written: a design element with no link would be noise, and a guessed link would be worse.
  `scripts/build-design.py` names them when it runs.

## A token trap

`req` reads the token, not the file format, and it reads **every** file under a design root. This
note lives in `docs/`, not `design/`, because its prose spells the token out: under `design/` it
would be read as a declaration with `<claim-id>` as the target and make `req satisfy`
UNVERIFIABLE (UNKNOWN CLAIM). Keep documentation that quotes the token outside the roots in
`.req/design`.
