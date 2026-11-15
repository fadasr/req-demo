#!/usr/bin/env python3
"""Cut the demo's one trace graph and component overlay into one per upstream example.

The corpus is one model, but the demonstration is four projects (Basic, Coffee Machine,
Automotive ADAS, ISO 26262 Safety). This script filters the `req.trace/1` and
`req.satisfy/1` documents by area prefix, then runs req's own converters:

  tools/graph/trace_to_archify.py   claim graph, grouped by area
  tools/graph/arch_overlay.py       component overlay, with the claims each component satisfies

The archify pin is the one req's examples/graph/README.md names (7e45f36); install it with
scripts/fetch-archify.sh. Output pages are committed to docs/<project>/; they are as current
as this run, so regenerate after a corpus change.

    python3 scripts/build-project-graphs.py
"""
import json
import os
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
DOCS = ROOT / "docs"
ARCHIFY = BUILD / "archify" / "archify" / "bin" / "archify.mjs"
REQ_TOOLS = ROOT / "tools" / "req-graph"

PROJECTS = [
    {
        "slug": "basic",
        "title": "Basic Example",
        "prefixes": ("basic-example",),
        "components": [],
    },
    {
        "slug": "coffee-machine",
        "title": "Coffee Machine",
        "prefixes": ("coffee-machine",),
        "components": ["coffee"],
    },
    {
        "slug": "automotive-adas",
        "title": "Automotive ADAS",
        "prefixes": ("automotive-adas",),
        "components": ["lane", "acc", "collision", "pedestrian", "alerting",
                       "traffic", "blind", "drowsy", "parking"],
    },
    {
        "slug": "iso-26262",
        "title": "ISO 26262 Functional Safety",
        "prefixes": ("safety-example",),
        "components": [],
    },
]


def run(args, env=None, cwd=ROOT):
    merged = dict(os.environ)
    merged.update(env or {})
    completed = subprocess.run(args, cwd=cwd, env=merged, capture_output=True, text=True)
    if completed.returncode != 0:
        raise SystemExit(
            f"{' '.join(str(a) for a in args)} exited {completed.returncode}:\n"
            f"{completed.stderr.strip() or completed.stdout.strip()}"
        )
    return completed.stdout


def in_project(area, prefixes):
    return bool(area) and any(area == p or area.startswith(p + "/") for p in prefixes)


def filter_trace(trace, prefixes):
    nodes = [node for node in trace["nodes"] if in_project(node.get("area"), prefixes)]
    ids = {node["claim_id"] for node in nodes}
    edges = [edge for edge in trace["edges"] if edge["from"] in ids and edge["to"] in ids]
    incoming = [
        edge for edge in trace["derived_incoming"]
        if edge["from"] in ids and edge["to"] in ids
    ]
    areas = [area for area in trace["areas"] if any(node.get("area") == area["path"] for node in nodes)]
    return {
        **{key: trace[key] for key in ("schema", "generator", "rules_v", "selection")},
        "nodes": nodes,
        "areas": areas,
        "edges": edges,
        "derived_incoming": incoming,
        "findings": {
            "dangling": [
                item for item in trace["findings"].get("dangling", [])
                if item.get("from") in ids or item.get("to") in ids
            ],
            "undecided_edges": [
                item for item in trace["findings"].get("undecided_edges", [])
                if item.get("from") in ids or item.get("to") in ids
            ],
        },
    }


def filter_satisfy(satisfy, ids):
    return {
        **{key: satisfy[key] for key in ("schema", "generator", "rules_v", "verdict")},
        "links": [link for link in satisfy["links"] if link["claim_id"] in ids],
        "mentions": [item for item in satisfy["mentions"] if item.get("claim") in ids],
        "unreadable": satisfy.get("unreadable", []),
    }


def component_diagram(project, revision):
    source = json.loads((DOCS / "components.archify.json").read_text(encoding="utf-8"))
    keep = set(project["components"])
    diagram = json.loads(json.dumps(source))
    diagram["components"] = [c for c in diagram["components"] if c["id"] in keep]
    diagram["boundaries"] = [
        b for b in diagram.get("boundaries", []) if all(c in keep for c in b["wraps"])
    ]
    diagram["connections"] = [
        c for c in diagram.get("connections", []) if c["from"] in keep and c["to"] in keep
    ]
    diagram["meta"]["title"] = f"req-demo — {project['title']} components"
    diagram["meta"]["output"] = "components.html"
    diagram["meta"]["repository"] = {
        "url": "https://github.com/fadasr/req-demo",
        "provider": "github",
        "link_mode": "local-only",
        "revision": revision,
    }
    return diagram


def finalize(spec, output, repo_root=False):
    args = [
        "node", str(ARCHIFY), "finalize", "architecture", str(spec), str(output),
        "--quality", "standard", "--json",
    ]
    if repo_root:
        args += ["--repo-root", str(ROOT)]
    raw = run(args, env={"ARCHIFY_UPDATE_CHECK_DISABLED": "1"})
    receipt = json.loads(raw)
    if not receipt.get("ok"):
        raise SystemExit(f"archify finalize failed for {output}: {raw}")


def main():
    if not ARCHIFY.is_file():
        print("build-project-graphs: archify is missing; run scripts/fetch-archify.sh", file=sys.stderr)
        return 3
    trace = json.loads((BUILD / "trace.json").read_text(encoding="utf-8"))
    satisfy = json.loads((BUILD / "satisfy.json").read_text(encoding="utf-8"))
    revision = run(["git", "rev-parse", "HEAD"]).strip()

    for project in PROJECTS:
        slug = project["slug"]
        out = BUILD / "projects" / slug
        shutil.rmtree(out, ignore_errors=True)
        out.mkdir(parents=True)
        doc = filter_trace(trace, project["prefixes"])
        ids = {node["claim_id"] for node in doc["nodes"]}
        target = DOCS / slug
        target.mkdir(parents=True, exist_ok=True)
        if not doc["nodes"]:
            print(f"{slug}: 0 claims, no graph")
            continue
        (out / "trace.json").write_text(json.dumps(doc, indent=1), encoding="utf-8")
        graph_dir = out / "graph"
        run(["python3", "-I", str(REQ_TOOLS / "trace_to_archify.py"), str(out / "trace.json"), str(graph_dir)])
        page = next(graph_dir.glob("*.json"))
        # The converter names a page "Requirement graph" and says "all claims" for the document it
        # was given; on a per-project page say which slice this is. Metadata only: no node or edge
        # is touched (examples/graph/README.md, rule 1).
        page_data = json.loads(page.read_text(encoding="utf-8"))
        page_data["meta"]["title"] = f"{project['title']} — requirement graph"
        page_data["meta"]["subtitle"] = (
            f"{project['title']} · {len(doc['nodes'])} claims · {len(doc['edges'])} relations · "
            f"rules_v {doc['rules_v']} · archify 7e45f36"
        )
        page.write_text(json.dumps(page_data, indent=1), encoding="utf-8")
        for stale in target.glob("graph.*.json"):
            stale.unlink()
        finalize(page, target / "graph.html")
        print(f"{slug}: graph {len(doc['nodes'])} claims, {len(doc['edges'])} edges -> {target / 'graph.html'}")

        if project["components"]:
            (out / "satisfy.json").write_text(
                json.dumps(filter_satisfy(satisfy, ids), indent=1), encoding="utf-8"
            )
            (out / "components.archify.json").write_text(
                json.dumps(component_diagram(project, revision), indent=2), encoding="utf-8"
            )
            overlay = out / "overlay"
            run([
                "python3", "-I", str(REQ_TOOLS / "arch_overlay.py"), "--root", str(ROOT),
                "--page", f"{slug}/components.html",
                str(out / "components.archify.json"), str(out / "satisfy.json"),
                str(out / "trace.json"), str(overlay),
            ])
            for stale in target.glob("components.*.json"):
                stale.unlink()
            finalize(overlay / "overlay.json", target / "components.html", repo_root=True)
            print(f"{slug}: components -> {target / 'components.html'}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
