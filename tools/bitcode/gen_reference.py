#!/usr/bin/env python3
"""Generate the bitcode type reference from `schema.rs`.

`SPEC_RUMOCA_BITCODE.md` is a good narrative and was a non-existent reference:
51 of the schema's 56 types had never appeared in it by name, and six fields of
`RbcModel` were absent entirely. Nothing kept it honest, so it tracked the
schema for exactly as long as somebody remembered to.

This derives the reference from the source of truth instead. `--check` fails
when the committed reference is stale or when a type or field carries no doc
comment, which is what makes the documentation a build product rather than a
good intention.

    tools/bitcode/gen_reference.py             # write docs/bitcode-reference.md
    tools/bitcode/gen_reference.py --check     # fail if it is stale
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "crates/rumoca-bitcode/src/schema.rs"
OUT = ROOT / "docs/bitcode-reference.md"

#: Types the container defines rather than the model: documented first, because
#: a reader opening an artifact meets them before anything else.
CONTAINER = ("RbcArtifact", "RbcModel", "RbcSummary")


@dataclass
class Member:
    name: str
    type_name: str
    doc: str = ""
    optional: bool = False
    defaulted: bool = False

    @property
    def compatibility(self) -> str:
        """What a reader of an older artifact does with this member.

        The distinction a consumer needs and the schema states in serde
        attributes: a defaulted field may be absent from an artifact written
        before it existed, so adding one is additive; adding a required field
        is a version break.
        """
        if self.defaulted or self.optional:
            return "additive"
        return "required"


@dataclass
class Item:
    name: str
    kind: str
    doc: str = ""
    members: list[Member] = field(default_factory=list)
    variants: list[Member] = field(default_factory=list)


def _doc(lines: list[str]) -> str:
    text = " ".join(line.strip().removeprefix("///").strip() for line in lines)
    return re.sub(r"\s+", " ", text).strip()


def parse(source: str) -> list[Item]:
    """Read the `Rbc*` declarations. A narrow parser with one owner.

    Deliberately not a full Rust parser: it reads the declaration forms this
    file actually uses, and `--check` fails loudly if a type goes missing,
    which is the failure mode that matters.
    """
    items: list[Item] = []
    lines = source.splitlines()
    pending: list[str] = []
    attributes: list[str] = []
    index = 0

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()

        if stripped.startswith("///"):
            pending.append(line)
            index += 1
            continue
        if stripped.startswith("#["):
            attributes.append(stripped)
            index += 1
            continue

        match = re.match(r"pub (struct|enum) (Rbc\w+)", stripped)
        if not match:
            if stripped and not stripped.startswith("//"):
                pending, attributes = [], []
            index += 1
            continue

        kind, name = match.group(1), match.group(2)
        item = Item(name=name, kind=kind, doc=_doc(pending))
        pending, attributes = [], []

        if stripped.endswith(";"):          # a unit struct
            items.append(item)
            index += 1
            continue

        depth = line.count("{") - line.count("}")
        index += 1
        member_doc: list[str] = []
        member_attrs: list[str] = []
        while index < len(lines) and depth > 0:
            body = lines[index]
            inner = body.strip()
            depth += body.count("{") - body.count("}")
            if depth <= 0:
                break
            if inner.startswith("///"):
                member_doc.append(body)
            elif inner.startswith("#["):
                member_attrs.append(inner)
            elif inner and not inner.startswith("//"):
                joined = " ".join(member_attrs)
                optional = False
                type_name = ""
                if kind == "struct":
                    hit = re.match(r"pub (\w+): (.+?),?$", inner)
                    if hit:
                        type_name = hit.group(2).rstrip(",")
                        optional = type_name.startswith("Option<")
                        item.members.append(Member(
                            name=hit.group(1), type_name=type_name,
                            doc=_doc(member_doc), optional=optional,
                            defaulted="serde(default" in joined))
                else:
                    hit = re.match(r"(\w+)\s*(\{|\(|,|$)", inner)
                    if hit and hit.group(1)[:1].isupper():
                        item.variants.append(Member(
                            name=hit.group(1), type_name="",
                            doc=_doc(member_doc)))
                member_doc, member_attrs = [], []
            index += 1
        items.append(item)
        index += 1
    return items


def render(items: list[Item]) -> str:
    by_name = {item.name: item for item in items}
    ordered = ([by_name[name] for name in CONTAINER if name in by_name]
               + sorted((item for item in items if item.name not in CONTAINER),
                        key=lambda item: item.name))

    out = [
        "# Rumoca Bitcode: type reference", "",
        "<!-- Generated by tools/bitcode/gen_reference.py. Do not edit: run",
        "     `tools/bitcode/gen_reference.py` after changing schema.rs, and",
        "     `--check` in CI fails when this file is stale. -->", "",
        "The narrative — container, encodings, versioning, identity, "
        "provenance, validation — is in "
        "[SPEC_RUMOCA_BITCODE.md](SPEC_RUMOCA_BITCODE.md). This is the "
        "reference for what an artifact contains, derived from "
        "`crates/rumoca-bitcode/src/schema.rs` so that it cannot fall behind "
        "it.", "",
        "**Compatibility** is per member. `additive` means a reader of an "
        "artifact written before the member existed still works, because the "
        "member is optional or defaulted; `required` means adding it is a "
        "version break.", "",
        f"{len(items)} types.", "",
        "| Type | Kind | Members |", "|---|---|---:|",
    ]
    for item in ordered:
        count = len(item.members) + len(item.variants)
        out.append(f"| [`{item.name}`](#{item.name.lower()}) | {item.kind} "
                   f"| {count} |")
    out.append("")

    for item in ordered:
        out += [f"## {item.name}", "", item.doc or "_No description._", ""]
        if item.members:
            out += ["| Member | Type | Compatibility | Meaning |",
                    "|---|---|---|---|"]
            for member in item.members:
                out.append(
                    f"| `{member.name}` | `{_escape(member.type_name)}` "
                    f"| {member.compatibility} "
                    f"| {member.doc or '—'} |")
            out.append("")
        if item.variants:
            out += ["| Variant | Meaning |", "|---|---|"]
            for variant in item.variants:
                out.append(f"| `{variant.name}` | {variant.doc or '—'} |")
            out.append("")
    return "\n".join(out) + "\n"


def _escape(text: str) -> str:
    return text.replace("|", "\\|")


def undocumented(items: list[Item]) -> list[str]:
    """Types and members carrying no doc comment.

    A reference generated from missing comments is a table of names, so the
    gap is reported rather than rendered as an empty cell nobody notices.
    """
    found = []
    for item in items:
        if not item.doc:
            found.append(item.name)
        for member in item.members + item.variants:
            if not member.doc:
                found.append(f"{item.name}.{member.name}")
    return found


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true",
                        help="fail if the committed reference is stale")
    parser.add_argument("--require-docs", action="store_true",
                        help="fail if any type or member has no doc comment")
    args = parser.parse_args()

    items = parse(SCHEMA.read_text())
    text = render(items)

    if args.check:
        current = OUT.read_text() if OUT.exists() else ""
        if current != text:
            print(f"{OUT.relative_to(ROOT)} is stale; run "
                  f"tools/bitcode/gen_reference.py", file=sys.stderr)
            return 1
        print(f"{OUT.relative_to(ROOT)} is current ({len(items)} types)")
    else:
        OUT.write_text(text)
        print(f"wrote {OUT.relative_to(ROOT)} ({len(items)} types)")

    missing = undocumented(items)
    if missing:
        print(f"{len(missing)} undocumented:", file=sys.stderr)
        for name in missing[:40]:
            print(f"  {name}", file=sys.stderr)
        if args.require_docs:
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
