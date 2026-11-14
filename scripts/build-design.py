#!/usr/bin/env python3
"""Build req design elements from the Sphinx-Needs architecture/design/code needs.

req models a design element as a file under a `.req/design` root that declares
`req-satisfies: <claim-id>` (ADR 0040). The upstream models architecture, software
architecture and components as needs with typed links. This script translates one into the
other: one design file per need, one `req-satisfies:` line per requirement the need links to.

    scripts/build-design.py --write

Reads `build/needs.json` and the corpus's claims (need id is the fragment of
`rationale.source`). Writes `design/architecture/<ID>.md`, `design/components/<ID>.md`, and
copies the two annotated C files to `design/code/` with their `req-satisfies:` header.

Nothing is invented: a target need that has no claim (a skipped requirement) is counted and
named, and a design need with no mapped target is skipped, not given a guessed link.
"""
import argparse
import json
import pathlib
import re
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
UPSTREAM = ROOT / "upstream"
EXPORT = ROOT / "build" / "needs.json"
CLAIMS = ROOT / "claims"
DESIGN = ROOT / "design"
PIN = "3c602bfedf710d2304d22a93049d7233bba93285"
ORIGIN = f"https://github.com/useblocks/sphinx-needs-demo@{PIN}"

# The two annotated C files, and the SWREQ ids each covers (read from the export's `impl`
# needs: IMPL_LKA_* in lane_keeping.c, IMPL_ACC_* in acc.c).
CODE = {
    "design/code/lane_keeping.c": "src/c/lane_keeping.c",
    "design/code/acc.c": "src/c/acc.c",
}


def one_line(value):
    return " ".join(str(value or "").split())


def unquote(value):
    text = value.strip()
    if len(text) >= 2 and text[0] == '"' and text[-1] == '"':
        return text[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    return text


def claim_map():
    """need id -> claim id, from each claim's rationale.source fragment."""
    mapping = {}
    for path in sorted(CLAIMS.glob("*.yml")):
        text = path.read_text(encoding="utf-8")
        claim = re.search(r"^claim_id:\s*(\S+)\s*$", text, re.MULTILINE)
        source = re.search(r"^\s+source:\s*(.+)$", text, re.MULTILINE)
        if not claim or not source:
            continue
        need = unquote(source.group(1)).rsplit("#", 1)[-1]
        mapping[need] = claim.group(1)
    return mapping


def target_of(need, fields):
    for field in fields:
        for value in need.get(field) or []:
            yield value.split("[", 1)[0].strip()


def write(path, text, write_mode):
    rel = path.relative_to(ROOT)
    if not write_mode:
        print(f"would write {rel}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(f"wrote {rel}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write the files (default: dry run)")
    args = parser.parse_args()

    if not EXPORT.is_file():
        print("build-design: build/needs.json is missing; run scripts/build-upstream.sh", file=sys.stderr)
        return 3
    export = json.loads(EXPORT.read_text(encoding="utf-8"))
    version = export["current_version"]
    needs = export["versions"][version]["needs"]
    claims = claim_map()

    kinds = {"arch": ("architecture", ("links",)),
             "swarch": ("architecture", ("links",)),
             "component": ("components", ("implements",))}
    mapped = 0
    skipped = []
    for need_id, need in needs.items():
        kind = kinds.get(need.get("type"))
        if not kind:
            continue
        folder, fields = kind
        targets, missing = [], []
        for target in target_of(need, fields):
            if target in claims:
                targets.append(claims[target])
            elif target in needs:
                missing.append(target)
        if not targets:
            skipped.append((need_id, missing))
            continue
        targets = sorted(set(targets))
        body = one_line(need.get("content"))
        # The upstream content mixes RST directives and PlantUML; the element's prose ends at the
        # first directive. Keep the sentence(s), not the markup.
        if ".." in body:
            body = body.split("..", 1)[0].strip()
        if len(body) > 400:
            body = body[:397].rstrip() + "..."
        lines = [
            f"# {one_line(need.get('title') or need_id)}",
            "",
            f"<!-- Sphinx-Needs {need.get('type')} {need_id} from "
            f"{need.get('docname')}:{need.get('lineno')}; source {ORIGIN}#{need_id}. -->",
            "",
        ]
        if body:
            lines += [body, ""]
        lines.append("## Satisfies")
        lines.append("")
        for claim in targets:
            lines.append(f"<!-- req-satisfies: {claim} -->")
        if missing:
            lines += ["", "Not linked: " + ", ".join(sorted(set(missing))) +
                      " (no claim in this corpus)."]
        lines.append("")
        write(DESIGN / folder / f"{need_id}.md", "\n".join(lines), args.write)
        mapped += len(targets)

    # The two code files are design elements too: copy them and put the requirement links in a
    # comment header. The upstream's own `// @ ... [SWREQ_...]` comments are kept.
    code_targets = {
        "design/code/lane_keeping.c": ["SWREQ_001", "SWREQ_002", "SWREQ_003"],
        "design/code/acc.c": ["SWREQ_004", "SWREQ_005", "SWREQ_006", "SWREQ_007", "SWREQ_013"],
    }
    for rel, source in CODE.items():
        source_path = UPSTREAM / source
        if not source_path.is_file():
            print(f"build-design: {source_path} is missing; run scripts/build-upstream.sh", file=sys.stderr)
            return 3
        links = [
            f"// req-satisfies: {claims[need]}"
            for need in code_targets[rel]
            if need in claims
        ]
        header = links + [
            f"// Sphinx-Needs source {ORIGIN}/{source}; the req links above are the SWREQ ids",
            "// this file implements, mapped to their claim ids.",
            "",
        ]
        text = "\n".join(header) + source_path.read_text(encoding="utf-8")
        write(ROOT / rel, text, args.write)
        mapped += len(links)

    print(f"design: {mapped} req-satisfies link(s)")
    if skipped:
        print("skipped (no drafted requirement):")
        for need_id, missing in skipped:
            print(f"  {need_id}  (targets: {', '.join(missing) or 'none'})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
