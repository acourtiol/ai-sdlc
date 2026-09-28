#!/usr/bin/env python3
"""Fail-closed validator and status router for product-repo intent artifacts."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

from fingerprint import ArtifactError, canonical_digest, read_artifact


SHA_RE = re.compile(r"^[0-9a-f]{40}$")
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
SLUG_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
TASK_RE = re.compile(r"^- \[( |x|X)\] ([0-9]+(?:\.[0-9]+)*\.?) (.+?) — verify: (\S.*)$")
ANY_BOX_RE = re.compile(r"\[[ xX]\]")
PLACEHOLDER_RE = re.compile(
    r"(?i)(\bTODO\b|\bTBD\b|"
    r"what cannot be done today|what shows the problem is real|what better looks like|"
    r"people and systems this touches|auth, PII, APIs|explicitly not this change|"
    r"what must be answered before spec|requirement: short name|scenario: short name|"
    r"what the system must do|the system SHALL do the observable thing|"
    r"how it fits the existing codebase|list only applicable failure cases|"
    r"unresolved items from intent\.md|exact paths\. new vs edit|build and verify order|"
    r"carry each applicable spec gotcha|the end-to-end evidence|name the fresh verifier subagent|"
    r"what the change actually|describe the behavior present in the reviewed diff|"
    r"tbd: where the implementation departed|which checks you skipped|list each skipped check|"
    r"every box in `plan\.md`|every plan task and every spec requirement|"
    r"each scenario: what you ran|review the full change range|if no separate challenge was available|"
    r"for autonomous approval only|what changes — verify: command, test, or observable behavior|"
    r"next step in this area|first step in the next area|"
    r"where relevant, list rollout prerequisites)"
)
CHECK_RE = re.compile(
    r"^- (PASS|FAIL|BLOCKED) \| action: (\S.+?) \| observed: (\S.+?) \| evidence: (\S.+)$"
)
ALLOWED_ISOLATION = {
    "subagent",
    "subagent-different-model",
    "subagent-same-model",
    "separate-session",
    "fresh-session",
}

SECTIONS = {
    "intent": [
        "Problem", "Evidence", "Proposed outcome", "Affected users and systems",
        "Constraints", "Out of scope", "Open questions",
    ],
    "spec": ["Requirements", "Design", "Gotchas / policy flags", "Open questions carried forward"],
    "plan": ["Files that change", "Order of work", "Risks", "Proof", "Review route"],
    "report": [
        "Change inspected", "What shipped", "Deviations from plan", "Verification",
        "Independent challenge", "Findings", "Not checked", "Release handoff", "Verdict",
    ],
}


@dataclass
class Document:
    path: Path
    fields: Dict[str, str]
    body: str
    kind: str

    def section(self, title: str) -> str:
        heading = re.compile(rf"(?m)^## {re.escape(title)}[ \t]*\n")
        matches = list(heading.finditer(self.body))
        if not matches:
            raise ArtifactError(f"{self.path}: missing required section '## {title}'")
        if len(matches) != 1:
            raise ArtifactError(f"{self.path}: duplicate required section '## {title}'")
        match = matches[0]
        start = match.end()
        next_heading = re.search(r"(?m)^## ", self.body[start:])
        end = start + next_heading.start() if next_heading else len(self.body)
        content = self.body[start:end].strip("\n")
        if not content.strip() and not (self.kind == "plan" and title == "Order of work"):
            raise ArtifactError(f"{self.path}: section '## {title}' is empty")
        return content

    def subsection(self, title: str) -> str:
        heading = re.compile(rf"(?m)^### {re.escape(title)}[ \t]*\n")
        matches = list(heading.finditer(self.body))
        if not matches:
            raise ArtifactError(f"{self.path}: missing required subsection '### {title}'")
        if len(matches) != 1:
            raise ArtifactError(f"{self.path}: duplicate required subsection '### {title}'")
        match = matches[0]
        start = match.end()
        next_heading = re.search(r"(?m)^#{2,3} ", self.body[start:])
        end = start + next_heading.start() if next_heading else len(self.body)
        content = self.body[start:end].strip("\n")
        if not content.strip():
            raise ArtifactError(f"{self.path}: subsection '### {title}' is empty")
        return content


def load_document(root: Path, slug: str, name: str, kind: str, required: bool = True) -> Optional[Document]:
    path = root / "intent" / slug / name
    if not path.exists():
        if required:
            raise ArtifactError(f"missing {name}")
        return None
    fields, body = read_artifact(path)
    if "status" in fields and fields["status"] not in {"draft", "accepted", "specified", "planned", "done"}:
        if kind != "report":
            raise ArtifactError(f"invalid {kind} status ({fields['status']})")
    if "slug" in fields and fields["slug"] != slug:
        raise ArtifactError(f"{name}: slug does not match directory '{slug}'")
    doc = Document(path=path, fields=fields, body=body, kind=kind)
    if kind == "report" and fields.get("verdict", "").lower() == "blocked":
        doc.section("Not checked")
    else:
        for title in SECTIONS[kind]:
            doc.section(title)
    if "slug" not in fields or fields["slug"] != slug:
        raise ArtifactError(f"{name}: slug is missing or does not match directory '{slug}'")
    return doc


def check_substantive(doc: Document, sections: Sequence[str]) -> None:
    allow_none = {
        "Constraints", "Out of scope", "Open questions", "Gotchas / policy flags",
        "Open questions carried forward", "Risks", "Deviations from plan", "Not checked", "Release handoff",
    }
    for title in sections:
        content = doc.subsection(title) if title in {"Completeness", "Correctness", "Coherence"} else doc.section(title)
        if PLACEHOLDER_RE.search(content):
            raise ArtifactError(f"{doc.path}: section '## {title}' still contains template guidance")
        if title in allow_none and content.strip().lower() == "none.":
            continue
        if len(re.sub(r"\s+", "", content)) < 8:
            raise ArtifactError(f"{doc.path}: section '## {title}' is not substantive")


def check_task_list(plan: Document) -> Tuple[int, int]:
    text = plan.section("Order of work")
    total = ticked = 0
    for line_number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        match = TASK_RE.fullmatch(line)
        if match:
            if PLACEHOLDER_RE.search(line) or match.group(4).strip() == "...":
                raise ArtifactError(f"{plan.path}: task entry still contains template guidance at line {line_number}")
            total += 1
            if match.group(1).lower() == "x":
                ticked += 1
            continue
        if ANY_BOX_RE.search(line) or stripped.startswith(("-", "*", "+")) or re.match(r"^\d+\.\s", stripped):
            raise ArtifactError(f"{plan.path}: malformed or indented task entry in Order of work at line {line_number}")
        raise ArtifactError(f"{plan.path}: unexpected non-task content in Order of work at line {line_number}")
    return ticked, total


def check_spec_structure(spec: Document) -> Tuple[List[str], List[str]]:
    requirements = spec.section("Requirements")
    for heading in re.findall(r"(?m)^### (.+)$", requirements):
        if not heading.startswith("Requirement: "):
            raise ArtifactError(f"{spec.path}: unsupported heading in Requirements: ### {heading}")
    for heading in re.findall(r"(?m)^#### (.+)$", requirements):
        if not heading.startswith("Scenario: "):
            raise ArtifactError(f"{spec.path}: unsupported heading in Requirements: #### {heading}")
    requirement_matches = list(re.finditer(r"(?m)^### Requirement: ([^\n]+)$", requirements))
    if not requirement_matches:
        raise ArtifactError(f"{spec.path}: Requirements needs a named ### Requirement: block")
    requirement_names: List[str] = []
    scenario_names: List[str] = []
    for index, match in enumerate(requirement_matches):
        name = match.group(1).strip()
        if not name or PLACEHOLDER_RE.search(name):
            raise ArtifactError(f"{spec.path}: requirement name is missing or a placeholder")
        if name in requirement_names:
            raise ArtifactError(f"{spec.path}: duplicate requirement name '{name}'")
        block_end = requirement_matches[index + 1].start() if index + 1 < len(requirement_matches) else len(requirements)
        block = requirements[match.end():block_end]
        scenarios = list(re.finditer(r"(?m)^#### Scenario: ([^\n]+)$", block))
        if not scenarios:
            raise ArtifactError(f"{spec.path}: requirement '{name}' has no Scenario")
        if not re.search(r"\bSHALL\b", block[:scenarios[0].start()]):
            raise ArtifactError(f"{spec.path}: requirement '{name}' has no SHALL statement before its scenarios")
        requirement_names.append(name)
        for scenario_index, scenario in enumerate(scenarios):
            scenario_name = scenario.group(1).strip()
            scenario_end = scenarios[scenario_index + 1].start() if scenario_index + 1 < len(scenarios) else len(block)
            scenario_body = block[scenario.end():scenario_end]
            if not scenario_name or PLACEHOLDER_RE.search(scenario_name):
                raise ArtifactError(f"{spec.path}: scenario name is missing or a placeholder")
            if scenario_name in scenario_names:
                raise ArtifactError(f"{spec.path}: duplicate scenario name '{scenario_name}'")
            if not re.search(r"(?m)^- \*\*WHEN\*\* \S", scenario_body) or not re.search(r"(?m)^- \*\*THEN\*\* \S", scenario_body):
                raise ArtifactError(f"{spec.path}: scenario '{scenario_name}' needs WHEN and THEN")
            scenario_names.append(scenario_name)
    return requirement_names, scenario_names


def verify_approval(doc: Document, expected_status: Sequence[str], dependency: Optional[Tuple[str, str]] = None) -> str:
    status = doc.fields.get("status", "")
    if status not in expected_status:
        raise ArtifactError(f"invalid {doc.kind} status ({status or 'missing'})")
    approved_by = doc.fields.get("approved_by", "")
    if approved_by not in {"human", "autonomous"}:
        raise ArtifactError(f"{doc.kind} approval is missing valid approved_by metadata")
    stored = doc.fields.get("approved_digest", "")
    if not DIGEST_RE.fullmatch(stored):
        raise ArtifactError(f"{doc.kind} approval is missing a valid approved_digest")
    if dependency:
        field_name, expected = dependency
        recorded = doc.fields.get(field_name, "")
        if not DIGEST_RE.fullmatch(recorded) or recorded != expected:
            raise ArtifactError(f"{doc.kind} has a stale or missing {field_name}")
    try:
        calculated = canonical_digest(doc.path)
    except ArtifactError:
        raise
    if stored != calculated:
        raise ArtifactError(f"{doc.kind} approval digest is stale; reapprove the current content")
    if approved_by == "autonomous":
        review = doc.section("Decision review")
        if PLACEHOLDER_RE.search(review) or len(re.sub(r"\s+", "", review)) < 8:
            raise ArtifactError(f"{doc.kind} autonomous approval has no substantive Decision review")
    return stored


def run_git(root: Path, *args: str, check: bool = True) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as error:
        raise ArtifactError(f"cannot run git: {error}") from error
    if check and result.returncode:
        raise ArtifactError(result.stderr.strip() or "git command failed")
    return result.stdout.strip()


def require_commit(root: Path, value: str, label: str) -> str:
    if not SHA_RE.fullmatch(value):
        raise ArtifactError(f"{label} must be a full 40-character commit SHA")
    verify = subprocess.run(
        ["git", "-C", str(root), "cat-file", "-e", f"{value}^{{commit}}"],
        capture_output=True,
    )
    if verify.returncode:
        raise ArtifactError(f"{label} does not name a commit")
    return value


def is_ancestor(root: Path, ancestor: str, descendant: str, label: str) -> None:
    result = subprocess.run(
        ["git", "-C", str(root), "merge-base", "--is-ancestor", ancestor, descendant],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        raise ArtifactError(f"{label} is not an ancestor of current HEAD")


def current_head(root: Path) -> str:
    head = run_git(root, "rev-parse", "HEAD")
    if not SHA_RE.fullmatch(head):
        raise ArtifactError("repository HEAD is unavailable")
    return head


def require_clean_tree(root: Path) -> None:
    status = run_git(root, "status", "--porcelain", "--untracked-files=all")
    if status:
        raise ArtifactError("working tree is dirty or contains untracked files; resolve them before archiving")


def commit_path_changes(root: Path, reviewed_head: str) -> List[Tuple[str, List[str]]]:
    commits = run_git(root, "rev-list", "--reverse", f"{reviewed_head}..HEAD").splitlines()
    changes: List[Tuple[str, List[str]]] = []
    for commit in commits:
        parents = run_git(root, "rev-list", "--parents", "-n", "1", commit).split()
        if len(parents) < 2:
            raise ArtifactError(f"could not inspect parents for commit {commit}")
        result = subprocess.run(
            ["git", "-C", str(root), "diff", "--name-only", parents[1], commit],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode:
            raise ArtifactError(f"could not inspect files changed by commit {commit}")
        paths = sorted({line.strip() for line in result.stdout.splitlines() if line.strip()})
        changes.append((commit, paths))
    return changes


def check_report_freshness(root: Path, slug: str, intent: Document, spec: Document, plan: Document, report: Document) -> None:
    reviewed = report.fields.get("reviewed_head", "")
    require_commit(root, reviewed, "report reviewed_head")
    head = current_head(root)
    is_ancestor(root, reviewed, head, "report reviewed_head")
    is_ancestor(root, plan.fields["base_commit"], reviewed, "plan base_commit")
    # The approved artifacts named by the report must already have existed at
    # the reviewed commit. Later reapproval cannot retroactively become part of
    # a review of an earlier implementation snapshot.
    for document in (intent, spec, plan):
        relative = f"intent/{slug}/{document.path.name}"
        result = subprocess.run(
            ["git", "-C", str(root), "show", f"{reviewed}:{relative}"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode:
            raise ArtifactError(f"{relative} was absent at reviewed_head")
        with tempfile.TemporaryDirectory() as temporary:
            historical = Path(temporary) / document.path.name
            historical.write_text(result.stdout, encoding="utf-8")
            historical_fields, _ = read_artifact(historical)
            approved = document.fields["approved_digest"]
            if historical_fields.get("approved_digest") != approved or canonical_digest(historical) != approved:
                raise ArtifactError(f"{relative} approval changed after reviewed_head")
    allowed = {
        f"intent/{slug}/intent.md",
        f"intent/{slug}/spec.md",
        f"intent/{slug}/plan.md",
        f"intent/{slug}/report.md",
    }
    changes = commit_path_changes(root, reviewed)
    changed = {path for _, paths in changes for path in paths}
    unexpected = sorted(changed - allowed)
    if unexpected:
        raise ArtifactError("implementation changed after verification: " + ", ".join(unexpected))
    report_path = f"intent/{slug}/report.md"
    report_commits = [paths for _, paths in changes if report_path in paths]
    if len(report_commits) != 1 or set(report_commits[0]) != {report_path}:
        raise ArtifactError("report must be committed once, separately, after reviewed_head")
    require_clean_tree(root)


def parse_findings(report: Document) -> Tuple[bool, str]:
    try:
        content = report.section("Findings")
    except ArtifactError:
        if report.fields.get("verdict", "").lower() == "blocked":
            return False, ""
        raise
    meaningful = [line.strip() for line in content.splitlines() if line.strip()]
    if len(meaningful) == 1 and meaningful[0].lower() == "none.":
        return False, content
    critical = False
    previous_finding = False
    for line_number, line in enumerate(content.splitlines(), start=1):
        if not line.strip() or line[:1].isspace():
            if not line.strip():
                continue
            stripped = line.lstrip()
            nested_match = re.match(r"^(?:[-*]|\d+\.)\s+(?:\*\*)?(CRITICAL|WARNING|SUGGESTION)(?:\*\*)?(?=\s|:|—|-|$)", stripped)
            if nested_match:
                if not re.search(r"[A-Za-z0-9_./-]+:[0-9]+\b", stripped):
                    raise ArtifactError(f"{report.path}: finding at line {line_number} needs file:line")
                if nested_match.group(1) == "CRITICAL":
                    critical = True
                previous_finding = True
                continue
            if "CRITICAL" in line or "WARNING" in line or "SUGGESTION" in line:
                raise ArtifactError(f"{report.path}: ambiguous indented severity at Findings line {line_number}")
            if previous_finding:
                continue
            raise ArtifactError(f"{report.path}: orphan indented text in Findings at line {line_number}")
        match = re.match(r"^(?:[-*]|\d+\.)\s+(?:\*\*)?(CRITICAL|WARNING|SUGGESTION)(?:\*\*)?(?=\s|:|—|-|$)", line)
        if not match:
            raise ArtifactError(f"{report.path}: ambiguous finding entry at Findings line {line_number}")
        if not re.search(r"[A-Za-z0-9_./-]+:[0-9]+\b", line):
            raise ArtifactError(f"{report.path}: finding at line {line_number} needs file:line")
        previous_finding = True
        if match.group(1) == "CRITICAL":
            critical = True
    return critical, content


def validate_report_body(report: Document, plan: Document, reviewed_head: str, requirements: Sequence[str], scenarios: Sequence[str]) -> None:
    required_evidence = ["What shipped", "Completeness", "Correctness", "Coherence", "Independent challenge"]
    check_substantive(report, required_evidence)
    actions_by_title: Dict[str, List[str]] = {}
    all_check_statuses: List[str] = []
    for title in ("Completeness", "Correctness", "Coherence"):
        content = report.subsection(title)
        checks = []
        actions = []
        for line in content.splitlines():
            if not line.startswith("- "):
                continue
            match = CHECK_RE.fullmatch(line)
            if not match or PLACEHOLDER_RE.search(line):
                raise ArtifactError(f"{report.path}: {title} has a malformed check entry")
            checks.append(match.group(1))
            actions.append(match.group(2))
        if not checks:
            raise ArtifactError(f"{report.path}: {title} needs a check with status, action, observation, and evidence")
        if report.fields.get("verdict", "").lower() == "pass" and any(status != "PASS" for status in checks):
            raise ArtifactError(f"{report.path}: passing report has a non-passing {title} check")
        all_check_statuses.extend(checks)
        actions_by_title[title] = actions
    if report.fields.get("verdict", "").lower() == "fail" and "FAIL" not in all_check_statuses:
        raise ArtifactError(f"{report.path}: failing report needs a FAIL check entry")
    for name in requirements:
        if not any(name in action for action in actions_by_title["Completeness"]):
            raise ArtifactError(f"{report.path}: Completeness check omits requirement '{name}'")
    for name in scenarios:
        if not any(name in action for action in actions_by_title["Correctness"]):
            raise ArtifactError(f"{report.path}: Correctness check omits scenario '{name}'")
    for title in ("Deviations from plan", "Not checked", "Release handoff"):
        content = report.section(title)
        if PLACEHOLDER_RE.search(content):
            raise ArtifactError(f"{report.path}: section '## {title}' still contains template guidance")
    change = report.section("Change inspected")
    base = plan.fields.get("base_commit", "")
    if not SHA_RE.fullmatch(base) or base not in change:
        raise ArtifactError("report Change inspected must name the plan base_commit")
    if reviewed_head not in change:
        raise ArtifactError("report Change inspected must name reviewed_head")
    lowered = change.lower()
    if "working tree" not in lowered and "working-tree" not in lowered and "worktree" not in lowered:
        raise ArtifactError("report Change inspected must describe working-tree state")
    if "untracked" not in lowered:
        raise ArtifactError("report Change inspected must describe untracked paths")
    diff = subprocess.run(
        ["git", "-C", str(plan.path.parents[2]), "diff", "--name-only", base, reviewed_head],
        capture_output=True,
        text=True,
        check=False,
    )
    if diff.returncode:
        raise ArtifactError("could not inspect implementation paths named by the report")
    absent_paths = [path for path in diff.stdout.splitlines() if path and path not in change]
    if absent_paths:
        raise ArtifactError("report Change inspected omits changed paths: " + ", ".join(absent_paths))
    verdict_section = report.section("Verdict")
    verdict = report.fields.get("verdict", "").lower()
    body_value = re.match(r"(?i)^(pass|fail|blocked)\b", verdict_section)
    if not body_value or body_value.group(1).lower() != verdict:
        raise ArtifactError("report Verdict section must match frontmatter verdict")
    if re.search(r"(?i)verified in (?:the )?implementing session", report.body):
        raise ArtifactError("report discloses verification in the implementing session")
    if not report.section("Not checked").strip():
        raise ArtifactError("report Not checked section is empty")


def check_blocked_report(report: Document) -> None:
    if report.fields.get("verdict", "").lower() != "blocked":
        raise ArtifactError("blocked handoff requires verdict: blocked")
    not_checked = report.section("Not checked")
    lines = [line.strip() for line in not_checked.splitlines() if line.strip()]
    reason = re.findall(r"(?im)^Reason:[ \t]*(.+)$", not_checked)
    recovery = re.findall(r"(?im)^Recovery:[ \t]*(.+)$", not_checked)
    if len(lines) != 2 or len(reason) != 1 or len(recovery) != 1 or not lines[0].startswith("Reason:") or not lines[1].startswith("Recovery:"):
        raise ArtifactError("blocked report Not checked must contain exactly one nonempty Reason: and Recovery: line")
    if PLACEHOLDER_RE.search(not_checked):
        raise ArtifactError("blocked report still contains template guidance")
    try:
        report.section("Findings")
    except ArtifactError:
        return
    critical, _ = parse_findings(report)
    if critical:
        raise ArtifactError("blocked report contains a CRITICAL finding that requires a fix")


def validate_change(root: Path, slug: str, require_done: bool = False) -> Tuple[Document, Document, Document, Document, Tuple[int, int]]:
    if not SLUG_RE.fullmatch(slug) or slug in {".", "..", "archive"}:
        raise ArtifactError(f"invalid intent slug: {slug!r}")
    intent = load_document(root, slug, "intent.md", "intent")
    spec = load_document(root, slug, "spec.md", "spec")
    plan = load_document(root, slug, "plan.md", "plan")
    report = load_document(root, slug, "report.md", "report")
    assert intent and spec and plan and report
    check_substantive(intent, SECTIONS["intent"])
    check_substantive(spec, SECTIONS["spec"])
    requirements, scenarios = check_spec_structure(spec)
    check_substantive(plan, ["Files that change", "Risks", "Proof", "Review route"])
    intent_digest = verify_approval(intent, ("accepted", "done"))
    spec_digest = verify_approval(spec, ("specified", "done"), ("intent_digest", intent_digest))
    plan_digest = verify_approval(plan, ("planned", "done"), ("spec_digest", spec_digest))
    ticked, total = check_task_list(plan)
    if total == 0:
        raise ArtifactError("plan has zero task boxes")
    if ticked != total:
        raise ArtifactError(f"plan has unticked task boxes ({ticked}/{total})")
    if plan.fields.get("base_commit") == "pending":
        raise ArtifactError("plan base_commit is still pending")
    require_commit(root, plan.fields.get("base_commit", ""), "plan base_commit")
    is_ancestor(root, plan.fields["base_commit"], current_head(root), "plan base_commit")
    if report.fields.get("verdict", "").lower() not in {"pass", "fail", "blocked", "pending"}:
        raise ArtifactError("report has invalid verdict")
    if report.fields.get("intent_digest") != intent_digest:
        raise ArtifactError("report has a stale or missing intent_digest")
    if report.fields.get("spec_digest") != spec_digest:
        raise ArtifactError("report has a stale or missing spec_digest")
    if report.fields.get("plan_digest") != plan_digest:
        raise ArtifactError("report has a stale or missing plan_digest")
    verdict = report.fields.get("verdict", "").lower()
    isolation = report.fields.get("isolation", "")
    if isolation == "none":
        if verdict != "blocked":
            raise ArtifactError("isolation: none is valid only for a blocked report")
    elif isolation not in ALLOWED_ISOLATION:
        raise ArtifactError("report has invalid isolation")
    critical, _ = parse_findings(report)
    if verdict == "blocked":
        check_blocked_report(report)
    elif verdict in {"pass", "fail"}:
        validate_report_body(report, plan, report.fields.get("reviewed_head", ""), requirements, scenarios)
    if verdict == "pass" and critical:
        raise ArtifactError("passing report contains a CRITICAL finding")
    if verdict == "pass":
        check_report_freshness(root, slug, intent, spec, plan, report)
    if require_done:
        for doc in (intent, spec, plan):
            if doc.fields.get("status") != "done":
                raise ArtifactError(f"{doc.kind} status is not done")
        if report.fields.get("verdict", "").lower() != "pass":
            raise ArtifactError("report verdict is not pass")
        if critical:
            raise ArtifactError("report contains a CRITICAL finding")
        check_report_freshness(root, slug, intent, spec, plan, report)
    return intent, spec, plan, report, (ticked, total)


def archive_check(root: Path, slug: str) -> None:
    validate_change(root, slug, require_done=True)


def _artifact_status(root: Path, slug: str, filename: str, kind: str) -> Tuple[Optional[Document], str]:
    path = root / "intent" / slug / filename
    if not path.exists():
        return None, "missing"
    doc = load_document(root, slug, filename, kind)
    assert doc is not None
    return doc, doc.fields.get("status", "missing")


def route_one(root: Path, slug: str) -> Tuple[str, Dict[str, str]]:
    directory = root / "intent" / slug
    try:
        intent, intent_status = _artifact_status(root, slug, "intent.md", "intent")
        spec, spec_status = _artifact_status(root, slug, "spec.md", "spec")
        plan, plan_status = _artifact_status(root, slug, "plan.md", "plan")
    except ArtifactError as error:
        message = str(error)
        if message.startswith("invalid ") and " status (" in message:
            return f"inspect {message}", {}
        return f"inspect invalid artifact ({message})", {}
    statuses = {"intent": intent_status, "spec": spec_status, "plan": plan_status}
    if intent is None:
        if (directory / "context.md").exists():
            return "sdlc-explore (context.md only), then sdlc-plan when ready", statuses
        return "sdlc-plan (no intent.md)", statuses
    if intent_status == "draft":
        return "present intent; on accept set accepted, then sdlc-design", statuses
    if intent_status not in {"accepted", "done"}:
        return f"inspect invalid intent status ({intent_status})", statuses
    try:
        intent_digest = verify_approval(intent, ("accepted", "done"))
        check_substantive(intent, SECTIONS["intent"])
    except ArtifactError as error:
        return f"reconcile intent approval ({error})", statuses
    if spec is None:
        return "sdlc-design", statuses
    if spec_status == "draft":
        return "sdlc-design (review draft and readiness before approval)", statuses
    if spec_status not in {"specified", "done"}:
        return f"inspect invalid spec status ({spec_status})", statuses
    try:
        spec_digest = verify_approval(spec, ("specified", "done"), ("intent_digest", intent_digest))
        check_substantive(spec, SECTIONS["spec"])
        check_spec_structure(spec)
    except ArtifactError as error:
        return f"sdlc-design (reconcile specification: {error})", statuses
    if plan is None:
        return "sdlc-apply (plan step)", statuses
    if plan_status == "draft":
        try:
            _, total = check_task_list(plan)
            if total == 0:
                return "repair plan (0 boxes)", statuses
        except ArtifactError as error:
            return f"repair plan ({error})", statuses
        return "sdlc-apply (reconcile draft plan with approved spec before approval)", statuses
    if plan_status not in {"planned", "done"}:
        return f"inspect invalid plan status ({plan_status})", statuses
    try:
        plan_digest = verify_approval(plan, ("planned", "done"), ("spec_digest", spec_digest))
        check_substantive(plan, ["Files that change", "Risks", "Proof", "Review route"])
        ticked, total = check_task_list(plan)
    except ArtifactError as error:
        if "task entry" in str(error) or "non-task content" in str(error):
            return f"repair plan ({error})", statuses
        return f"sdlc-apply (reconcile approved plan: {error})", statuses
    statuses["boxes"] = f"{ticked}/{total}"
    if total == 0:
        return "repair plan (0 boxes)", statuses
    if plan_status == "done" and ticked < total:
        return "repair inconsistent plan (done with unticked boxes)", statuses
    if ticked < total:
        return f"sdlc-apply implement ({ticked}/{total} boxes ticked)", statuses
    report_path = directory / "report.md"
    if not report_path.exists():
        return "sdlc-verify", statuses
    try:
        report = load_document(root, slug, "report.md", "report")
        assert report is not None
    except ArtifactError as error:
        return f"sdlc-verify (invalid report: {error})", statuses
    verdict = report.fields.get("verdict", "").lower()
    statuses["verdict"] = verdict or "missing"
    if verdict == "blocked":
        try:
            validate_change(root, slug, require_done=False)
        except ArtifactError as error:
            if "CRITICAL" in str(error):
                return "sdlc-apply (fix findings) then sdlc-verify", statuses
            return f"sdlc-verify (invalid blocked handoff: {error})", statuses
        return "sdlc-verify (resolve blocked verification prerequisites)", statuses
    if verdict == "fail":
        try:
            validate_change(root, slug, require_done=False)
        except ArtifactError as error:
            return f"sdlc-verify (invalid failing report: {error})", statuses
        return "sdlc-apply (fix findings) then sdlc-verify", statuses
    if verdict != "pass":
        return "sdlc-verify", statuses
    try:
        validate_change(root, slug, require_done=False)
    except ArtifactError as error:
        message = str(error)
        if "CRITICAL" in message:
            return "sdlc-apply (fix findings) then sdlc-verify", statuses
        return f"sdlc-verify (invalid or stale evidence: {message})", statuses
    if any(status != "done" for status in (intent_status, spec_status, plan_status)):
        return "mark artifacts done", statuses
    try:
        archive_check(root, slug)
    except ArtifactError as error:
        return f"sdlc-verify (archive prerequisites invalid: {error})", statuses
    return "sdlc-archive", statuses


def route(root: Path) -> int:
    intent_root = root / "intent"
    if not intent_root.is_dir():
        print("no intent/ directory")
        return 0
    found = False
    for directory in sorted(intent_root.iterdir()):
        if not directory.is_dir() or directory.name == "archive":
            continue
        found = True
        slug = directory.name
        next_gate, statuses = route_one(root, slug)
        print(f"slug: {slug}")
        for key in ("intent", "spec", "plan"):
            print(f"  {key}: {statuses.get(key, 'invalid')}")
        if "boxes" in statuses:
            print(f"  boxes: {statuses['boxes']}")
        if "verdict" in statuses:
            print(f"  verdict: {statuses['verdict']}")
        print(f"  next: {next_gate}")
    if not found:
        print("no active intent slugs")
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    route_parser = sub.add_parser("route", help="list active intents and their next gate")
    route_parser.add_argument("root", nargs="?", default=".")
    digest_parser = sub.add_parser("digest", help="print a canonical approval fingerprint")
    digest_parser.add_argument("artifact")
    digest_parser.add_argument("root", nargs="?", default=".")
    validate_parser = sub.add_parser("validate", help="validate artifacts and report freshness")
    validate_parser.add_argument("slug")
    validate_parser.add_argument("root", nargs="?", default=".")
    archive_parser = sub.add_parser("archive-check", help="validate all archive preconditions")
    archive_parser.add_argument("slug")
    archive_parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve() if args.command in {"route", "validate", "archive-check"} else Path(args.root).resolve()
    try:
        if args.command == "route":
            return route(root)
        if args.command == "digest":
            artifact = Path(args.artifact)
            path = artifact if artifact.is_absolute() else root / artifact
            print(canonical_digest(path))
            return 0
        if args.command == "validate":
            validate_change(root, args.slug, require_done=False)
        else:
            archive_check(root, args.slug)
        print(f"{args.slug}: valid")
        return 0
    except ArtifactError as error:
        print(f"{args.command}: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
