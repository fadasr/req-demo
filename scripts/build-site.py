#!/usr/bin/env python3
"""Build the GitHub Pages site for the demo.

The data comes from the checked views, not from prose: `build/trace.json` (`req trace --format
json`), `build/satisfy.json` (`req satisfy --format json`), and the per-project graphs under
`docs/<project>/`. The generated pages are static; there is no runtime and no external asset.

    python3 scripts/build-site.py
"""
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
DOCS = ROOT / "docs"

PROJECTS = [
    {
        "slug": "basic",
        "title": "Basic Example",
        "icon": "🧰",
        "prefixes": ("basic-example",),
        "color": "slate",
        "description": (
            "The feature showcase: directives, filtering, imported needs and external needs. "
            "None of it is an obligation, so this project deliberately contributes zero claims."
        ),
        "shows": [
            "The importer drafts <code>EX_REQ_002</code> (“Some content”) and a human rejects it.",
            "<code>EX_REQ_001</code> has images and bold markup; it is skipped as <code>rst directive</code>, not stripped.",
            "External needs are not in a Sphinx-Needs export at all; imported needs have no content.",
        ],
    },
    {
        "slug": "coffee-machine",
        "title": "Coffee Machine",
        "icon": "☕️",
        "prefixes": ("coffee-machine",),
        "color": "amber",
        "description": (
            "A small end-to-end chain: system requirements → software requirements → components "
            "→ passing JUnit tests. The clearest example of the full V-model."
        ),
        "shows": [
            "8 claims: 4 system requirements and 4 software requirements.",
            "5 requirement relations and 4 design/code links; the coffee component satisfies 4 claims.",
            "7 JUnit links on 4 claims, all passing; the safety and temperature tests both prove the shutdown claim.",
        ],
    },
    {
        "slug": "automotive-adas",
        "title": "Automotive ADAS",
        "icon": "🚗",
        "prefixes": ("automotive-adas",),
        "color": "blue",
        "description": (
            "The V-model at scale: stakeholder needs → SYS.2 → SWE.1 → architecture and code, "
            "with the upstream's SYS.5 qualification evidence. The prose was re-worded into obligations."
        ),
        "shows": [
            "53 claims, 48 of them structured after the authoring pass; 44 requirement relations.",
            "9 software components satisfy the claims; the overlay shows all of them HOLD.",
            "9 claims are linked to the SYS.5 qualification report — three cases fail — so the gate says FAIL, not UNVERIFIABLE.",
            "The two turn-signal claims are the variant pair: <code>steering_side=left/right</code>.",
        ],
    },
    {
        "slug": "iso-26262",
        "title": "ISO 26262 Functional Safety",
        "icon": "🛡️",
        "prefixes": ("safety-example",),
        "color": "green",
        "description": (
            "HARA → safety goals → functional safety requirements → system requirements. The "
            "best-structured example and most of the corpus's relation edges."
        ),
        "shows": [
            "74 claims, 41 structured; the FSRs and system requirements are the remaining authoring work.",
            "171 requirement relations: <code>derives_from</code> carries the safety decomposition.",
            "No software components or tests: the upstream safety example stops at the requirement level.",
        ],
    },
]


def load(name, default):
    path = BUILD / name
    if not path.is_file():
        print(f"build-site: {path} is missing; run the req trace/satisfy commands first", file=sys.stderr)
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def esc(text):
    return html.escape(str(text), quote=True)


def one_line(text):
    return " ".join(str(text or "").split())


def short(text, limit):
    text = one_line(text)
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def element_name(path):
    return pathlib.Path(path).name


def test_name(test):
    parts = test.split("::")
    return "::".join(parts[-2:]) if len(parts) >= 2 else test


def in_project(area, prefixes):
    return bool(area) and any(area == p or area.startswith(p + "/") for p in prefixes)


def nodes_for(trace, project):
    return [n for n in trace["nodes"] if in_project(n.get("area"), project["prefixes"])]


def ids_for(nodes):
    return {n["claim_id"] for n in nodes}


def edges_for(trace, ids):
    return [e for e in trace["edges"] if e["from"] in ids and e["to"] in ids]


def links_for(satisfy, ids):
    return [l for l in satisfy["links"] if l["claim_id"] in ids]


def stats(trace, satisfy, project):
    nodes = nodes_for(trace, project)
    ids = ids_for(nodes)
    edges = edges_for(trace, ids)
    links = links_for(satisfy, ids)
    return {
        "nodes": nodes,
        "ids": ids,
        "edges": edges,
        "links": links,
        "claims": len(nodes),
        "structured": sum(1 for n in nodes if n.get("modality") != "UNSTRUCTURED"),
        "design": len(links),
        "tests": sum(len(n.get("tests") or []) for n in nodes),
        "areas": sorted({n.get("area") for n in nodes if n.get("area")}),
    }


def page(title, body, active, depth=0):
    prefix = "../" * depth
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · req-demo</title>
<link rel="stylesheet" href="{prefix}assets/site.css">
</head>
<body class="page-{esc(active)}">
<header class="top">
  <a class="brand" href="{prefix}index.html"><span class="mark">req</span><span>demo</span></a>
  <nav>
    <a href="{prefix}index.html#projects">Projects</a>
    <a href="{prefix}matrix.html">Matrix</a>
    <a href="{prefix}v-model.html">V-model</a>
    <a href="{prefix}components.html">Components</a>
    <a href="https://github.com/fadasr/req-demo/blob/main/FINDINGS.md">Findings</a>
  </nav>
</header>
<main>
{body}
</main>
<footer>
  <p>Source: <a href="https://github.com/fadasr/req-demo">fadasr/req-demo</a>.
  Requirements prose from <a href="https://github.com/useblocks/sphinx-needs-demo">useblocks/sphinx-needs-demo</a>
  at <code>3c602bf</code> (MIT); claims, views and pages generated with <a href="https://github.com/autox-my/req">req</a>.
  No signed Baseline: everything here is a draft for a human to ratify.</p>
</footer>
</body>
</html>
"""


def stat_block(value, label, accent=""):
    return f'<div class="stat {accent}"><strong>{value}</strong><span>{esc(label)}</span></div>'


def project_card(trace, satisfy, project):
    s = stats(trace, satisfy, project)
    links = []
    if (DOCS / project["slug"] / "graph.html").is_file():
        links.append(f'<a class="button" href="{project["slug"]}/graph.html">Graph</a>')
    if (DOCS / project["slug"] / "components.html").is_file():
        links.append(f'<a class="button" href="{project["slug"]}/components.html">Components</a>')
    links.append(f'<a class="button ghost" href="{project["slug"]}/index.html">Coverage</a>')
    return f"""
<article class="project-card accent-{project['color']}">
  <div class="card-head"><span class="icon">{project['icon']}</span><h3>{esc(project['title'])}</h3></div>
  <p>{esc(project['description'])}</p>
  <div class="mini-stats">
    <span><strong>{s['claims']}</strong> claims</span>
    <span><strong>{s['structured']}</strong> structured</span>
    <span><strong>{len(s['edges'])}</strong> relations</span>
    <span><strong>{s['tests']}</strong> test links</span>
  </div>
  <div class="card-links">{''.join(links)}</div>
</article>"""


def coverage_table(nodes, edges, links):
    if not nodes:
        return '<p class="empty">No claims in this project. That is the finding, not a missing import.</p>'
    by_claim = {}
    for link in links:
        by_claim.setdefault(link["claim_id"], []).append(link)
    outgoing = {}
    for edge in edges:
        outgoing.setdefault(edge["from"], []).append(edge)
    rows = []
    for node in sorted(nodes, key=lambda n: (n.get("area") or "", n["claim_id"])):
        design = "<br>".join(
            f'<code title="{esc(link["outcome"])}">{esc(element_name(link["element"]))}</code>'
            for link in by_claim.get(node["claim_id"], [])
        ) or "—"
        tests = "<br>".join(f"<code>{esc(test_name(t))}</code>" for t in node.get("tests") or []) or "—"
        relations = "<br>".join(
            f"{esc(edge['relation'])} → <a href=\"#{esc(edge['to'])}\">{esc(edge['to'])}</a>"
            for edge in outgoing.get(node["claim_id"], [])
        ) or "—"
        rows.append(
            f"<tr id=\"{esc(node['claim_id'])}\"><td><code>{esc(node['claim_id'])}</code></td>"
            f"<td>{esc(short(node.get('statement'), 120))}</td>"
            f"<td>{design}</td><td>{tests}</td><td class=\"rel\">{relations}</td></tr>"
        )
    return f"""<div class="table-wrap"><table class="coverage">
<thead><tr><th>Claim</th><th>Requirement</th><th>Design / code</th><th>Tests</th><th>Derives from</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>"""


def index_page(trace, satisfy):
    total = {
        "claims": len(trace["nodes"]),
        "edges": len(trace["edges"]),
        "design": len(satisfy["links"]),
        "tests": sum(len(n.get("tests") or []) for n in trace["nodes"]),
        "structured": sum(1 for n in trace["nodes"] if n.get("modality") != "UNSTRUCTURED"),
    }
    cards = "".join(project_card(trace, satisfy, p) for p in PROJECTS)
    body = f"""
<section class="hero">
  <p class="eyebrow">a real corpus, four projects, one claim model</p>
  <h1>Requirements that keep their meaning<br><span>and their links.</span></h1>
  <p class="lede">The four examples of <a href="https://sphinx-needs-demo.readthedocs.io/en/latest/">sphinx-needs-demo</a>
  put through <a href="https://github.com/autox-my/req">req</a>: imported, canonicalized, linked to
  architecture, code and tests, and gated. The spec, the matrix and this site are compiled views; the
  obligations are the source.</p>
  <div class="stats">
    {stat_block(total['claims'], 'claims')}
    {stat_block(total['edges'], 'requirement relations')}
    {stat_block(total['design'], 'design / code links')}
    {stat_block(total['tests'], 'test links')}
    {stat_block(total['structured'], 'structured', 'good')}
  </div>
</section>

<section id="projects" class="section">
  <div class="section-head"><h2>The four projects</h2><p>Each page has its own graph and coverage; the counts are this corpus.</p></div>
  <div class="grid">{cards}</div>
</section>

<section class="section split">
  <div>
    <h2>The three views</h2>
    <p>A claim is an obligation with a stable id and a content-addressed meaning. Everything else is a view over it.</p>
    <ul class="links">
      <li><a href="v-model.html">The V-model</a><span>The layer map: needs → system → software → architecture → code, with tests and ISO safety.</span></li>
      <li><a href="components.html">Component overlay</a><span>req's own <code>arch_overlay.py</code>: each component colored by the worst satisfaction outcome.</span></li>
      <li><a href="matrix.html">Coverage matrix</a><span>Every claim, its design/code elements, its linked tests and its derived requirements.</span></li>
      <li><a href="https://github.com/fadasr/req-demo/blob/main/docs/spec.md">Spec projection</a><span><code>req render</code>: the human-readable selection, regenerated, never hand-edited.</span></li>
    </ul>
  </div>
  <div class="panel">
    <h3>What the gate says</h3>
    <p><span class="badge warn">UNVERIFIABLE</span> no signed Baseline, and 121 claims have no linked test. The projections are current.</p>
    <p><span class="badge bad">FAIL</span> with both JUnit reports, nine ADAS claims are linked to three failing SYS.5 cases.</p>
    <p class="small">The policy is not “green at any cost”: “we could not tell” and “a test failed” are different answers.</p>
  </div>
</section>

<section class="section method">
  <h2>How it is made</h2>
  <ol>
    <li><strong>Import</strong> the pinned export with <code>--links --tests --areas</code>: 362 needs in, 135 claims out, 8 named skips, 219 not selected by type.</li>
    <li><strong>Author</strong>: 39 claims remain unstructured; the ADAS pass is done. Pins hold where a bound is load-bearing.</li>
    <li><strong>Link</strong>: 220 claim relations, 58 <code>req-satisfies</code> links to architecture/components/code, 16 JUnit links.</li>
    <li><strong>Gate</strong>: <code>req check</code> runs both variants, both projections and completeness; <code>req gate --test-report</code> judges the evidence.</li>
    <li><strong>Render</strong>: the graph and this site are regenerated from the JSON views, never edited by hand.</li>
  </ol>
</section>
"""
    return page("Requirements that keep their meaning", body, "home")


def project_page(trace, satisfy, project):
    s = stats(trace, satisfy, project)
    graph = f'<a class="button" href="graph.html">Requirement graph</a>' if (DOCS / project["slug"] / "graph.html").is_file() else ""
    components = f'<a class="button" href="components.html">Component overlay</a>' if (DOCS / project["slug"] / "components.html").is_file() else ""
    coverage = coverage_table(s["nodes"], s["edges"], links_for(satisfy, s["ids"]))
    shows = "".join(f"<li>{item}</li>" for item in project["shows"])
    body = f"""
<section class="project-hero accent-{project['color']}">
  <p class="eyebrow"><a href="../index.html">req-demo</a> / {esc(project['title'])}</p>
  <h1><span class="icon">{project['icon']}</span> {esc(project['title'])}</h1>
  <p class="lede">{esc(project['description'])}</p>
  <div class="stats">
    {stat_block(s['claims'], 'claims')}
    {stat_block(s['structured'], 'structured', 'good')}
    {stat_block(len(s['edges']), 'relations')}
    {stat_block(s['design'], 'design / code links')}
    {stat_block(s['tests'], 'test links')}
  </div>
  <div class="actions">{graph}{components}<a class="button ghost" href="../matrix.html">Full matrix</a></div>
</section>

<section class="section">
  <h2>What this project shows</h2>
  <ul class="shows">{shows}</ul>
</section>

<section class="section">
  <div class="section-head"><h2>Coverage</h2><p>{len(s['nodes'])} claims · {len(s['areas'])} area(s). Design cells are the files that declare <code>req-satisfies</code>; test cells are JUnit <code>classname::name</code>.</p></div>
  {coverage}
</section>
"""
    return page(project["title"], body, project["slug"], depth=1)


def matrix_page(trace, satisfy):
    sections = []
    for project in PROJECTS:
        s = stats(trace, satisfy, project)
        sections.append(f"""
<section class="section">
  <div class="section-head"><h2><span class="icon">{project['icon']}</span> {esc(project['title'])}</h2>
  <p>{s['claims']} claims · {len(s['edges'])} relations · {s['design']} design/code links · {s['tests']} test links</p></div>
  {coverage_table(s['nodes'], s['edges'], links_for(satisfy, s['ids']))}
</section>""")
    body = f"""
<section class="project-hero">
  <p class="eyebrow">one row per claim</p>
  <h1>Coverage matrix</h1>
  <p class="lede">The union of the four project views. A claim with no design element and no test is visible here on purpose; it is the adoption work list, not a silent exclusion.</p>
</section>
{''.join(sections)}
"""
    return page("Coverage matrix", body, "matrix")


def main():
    trace = load("trace.json", {"nodes": [], "edges": [], "areas": [], "rules_v": 0})
    satisfy = load("satisfy.json", {"links": []})
    if not trace["nodes"]:
        print("build-site: build/trace.json is empty", file=sys.stderr)
        return 3
    (DOCS / "assets").mkdir(parents=True, exist_ok=True)
    (DOCS / "index.html").write_text(index_page(trace, satisfy), encoding="utf-8")
    (DOCS / "matrix.html").write_text(matrix_page(trace, satisfy), encoding="utf-8")
    for project in PROJECTS:
        target = DOCS / project["slug"]
        target.mkdir(parents=True, exist_ok=True)
        (target / "index.html").write_text(project_page(trace, satisfy, project), encoding="utf-8")
        print(f"site: docs/{project['slug']}/index.html")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    print("site: docs/index.html, docs/matrix.html")
    return 0


if __name__ == "__main__":
    sys.exit(main())
