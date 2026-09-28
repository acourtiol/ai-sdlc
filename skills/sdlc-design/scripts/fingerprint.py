#!/usr/bin/env python3
"""Canonical content fingerprints for standalone SDLC artifact approvals.

The digest is ``sha256:`` plus SHA-256 over UTF-8 canonical JSON with sorted
frontmatter keys (excluding only ``status`` and ``approved_digest``) and the
artifact body. JSON keys are sorted and separators are compact. Line endings
are normalized to LF. Body whitespace is preserved. In ``plan.md`` only, the
checkbox state in task entries under ``## Order of work`` is normalized to an
unchecked box, so ticking work and changing artifact status are bookkeeping;
task wording, approval attribution, dependencies, base commit, and all other
artifact content remain bound to the approval.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Dict, Tuple
import hashlib


class ArtifactError(ValueError):
    pass


KEY_RE = re.compile(r"^[a-z][a-z0-9_]*$")
PLAN_TASK_RE = re.compile(r"^(- \[)[ xX](\].*)$")


def _parse_scalar(raw: str, path: Path, line_number: int) -> str:
    value = raw.strip()
    if not value:
        raise ArtifactError(f"{path}:{line_number}: empty frontmatter value")
    if value.startswith('"'):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError as error:
            raise ArtifactError(f"{path}:{line_number}: malformed quoted scalar") from error
        if not isinstance(parsed, str):
            raise ArtifactError(f"{path}:{line_number}: frontmatter values must be scalars")
        return parsed
    if value.startswith("'"):
        if len(value) < 2 or not value.endswith("'"):
            raise ArtifactError(f"{path}:{line_number}: malformed quoted scalar")
        return value[1:-1].replace("''", "'")
    if any(char in value for char in "{}[]"):
        raise ArtifactError(f"{path}:{line_number}: collections are not supported in frontmatter")
    if " #" in value:
        value = value.split(" #", 1)[0].rstrip()
    if not value:
        raise ArtifactError(f"{path}:{line_number}: empty frontmatter value")
    return value


def read_artifact(path: Path) -> Tuple[Dict[str, str], str]:
    """Read the deliberately small, top-level scalar frontmatter grammar."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise ArtifactError(f"cannot read UTF-8 artifact: {error}") from error
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].rstrip("\n") != "---":
        raise ArtifactError(f"{path}: frontmatter must start on the first line")
    fields: Dict[str, str] = {}
    close = None
    for index, line in enumerate(lines[1:], start=2):
        content = line.rstrip("\n")
        if content == "---":
            close = index
            break
        match = re.fullmatch(r"([a-z][a-z0-9_]*):[ \t]*(.*)", content)
        if not match:
            raise ArtifactError(f"{path}:{index}: expected a top-level scalar key: value")
        key, raw = match.groups()
        if not KEY_RE.fullmatch(key):
            raise ArtifactError(f"{path}:{index}: invalid frontmatter key {key!r}")
        if key in fields:
            raise ArtifactError(f"{path}:{index}: duplicate frontmatter key {key!r}")
        fields[key] = _parse_scalar(raw, path, index)
    if close is None:
        raise ArtifactError(f"{path}: frontmatter has no closing ---")
    body = "".join(lines[close:])
    # Reject a second frontmatter-looking delimiter before the first heading. This
    # catches a block placed after body text instead of treating it as metadata.
    if re.search(r"(?m)^---[ \t]*$", body):
        raise ArtifactError(f"{path}: unexpected frontmatter delimiter in body")
    return fields, body


def canonical_digest(path: Path) -> str:
    fields, body = read_artifact(path)
    normalized_fields = {key: value for key, value in fields.items() if key not in {"status", "approved_digest"}}
    body_lines = body.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    if path.name == "plan.md":
        in_order = False
        for index, line in enumerate(body_lines):
            if re.fullmatch(r"## Order of work[ \t]*", line):
                in_order = True
                continue
            if in_order and re.match(r"^## ", line):
                in_order = False
            if in_order and (match := PLAN_TASK_RE.fullmatch(line)):
                body_lines[index] = f"{match.group(1)} {match.group(2)}"
    canonical = json.dumps(
        {"frontmatter": normalized_fields, "body": "\n".join(body_lines)},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def main(argv: list[str]) -> int:
    if len(argv) not in {2, 3}:
        print("usage: fingerprint.py ARTIFACT [ROOT]", file=sys.stderr)
        return 2
    artifact = Path(argv[1])
    root = Path(argv[2]) if len(argv) == 3 else Path.cwd()
    path = artifact if artifact.is_absolute() else root / artifact
    try:
        print(canonical_digest(path))
    except ArtifactError as error:
        print(f"fingerprint: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
