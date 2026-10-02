"""Regression tests for deterministic SDLC artifact routing and integrity checks."""

from pathlib import Path
from tempfile import TemporaryDirectory
import shutil
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
CONTINUE_SCRIPTS = ROOT / "skills/sdlc-continue/scripts"
ARCHIVE_SCRIPTS = ROOT / "skills/sdlc-archive/scripts"
STATUS = CONTINUE_SCRIPTS / "status.sh"
VALIDATOR = CONTINUE_SCRIPTS / "validator.py"
FINGERPRINT = CONTINUE_SCRIPTS / "fingerprint.py"


def command(*args, cwd, check=True):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=check)


class ProductRepo:
    """Create a complete, passing change in a disposable Git repository."""

    def __init__(self, path):
        self.root = Path(path)
        self.slug = "example"
        self.change = self.root / "intent" / self.slug
        self.change.mkdir(parents=True)
        command("git", "init", "-q", cwd=self.root)
        command("git", "config", "user.email", "test@example.com", cwd=self.root)
        command("git", "config", "user.name", "Test", cwd=self.root)
        self.write("src/app.py", "value = 'before'\n")
        self.commit("initial source")
        self.base = self.head()

        self.intent_digest = self.write_approved("intent.md", self.intent_body(), {
            "status": '"done"',
            "slug": self.slug,
            "approved_by": "human",
            "approved_digest": "pending",
        })
        self.spec_digest = self.write_approved("spec.md", self.spec_body(), {
            "status": "done",
            "slug": self.slug,
            "intent": "intent.md",
            "intent_digest": self.intent_digest,
            "approved_by": "human",
            "approved_digest": "pending",
        })
        self.plan_digest = self.write_approved("plan.md", self.plan_body(), {
            "status": "done",
            "slug": self.slug,
            "spec": "spec.md",
            "base_commit": self.base,
            "spec_digest": self.spec_digest,
            "approved_by": "human",
            "approved_digest": "pending",
        })
        self.commit("approve artifacts")
        self.write("src/app.py", "value = 'after'\n")
        self.commit("implement change")
        self.reviewed = self.head()
        self.write_report()
        self.commit("record verification")

    def head(self):
        return command("git", "rev-parse", "HEAD", cwd=self.root).stdout.strip()

    def commit(self, message):
        command("git", "add", "-A", cwd=self.root)
        command("git", "commit", "-qm", message, cwd=self.root)

    def write(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def write_approved(self, name, body, fields):
        self.write(f"intent/{self.slug}/{name}", self.markdown(fields, body))
        digest = self.digest(f"intent/{self.slug}/{name}")
        fields["approved_digest"] = digest
        self.write(f"intent/{self.slug}/{name}", self.markdown(fields, body))
        return digest

    def digest(self, relative):
        return command(sys.executable, str(FINGERPRINT), relative, cwd=self.root).stdout.strip()

    @staticmethod
    def markdown(fields, body):
        frontmatter = "".join(f"{key}: {value}\n" for key, value in fields.items())
        return f"---\n{frontmatter}---\n\n{body.strip()}\n"

    @staticmethod
    def intent_body():
        return """# Intent: example

## Problem
The example flow currently returns the old value.

## Evidence
The existing repository behavior confirms the issue.

## Proposed outcome
The flow returns the updated value to callers.

## Affected users and systems
Users of the example module and its local caller.

## Constraints
None.

## Out of scope
None.

## Open questions
None.
"""

    @staticmethod
    def spec_body():
        return """# Spec: example

## Requirements
### Requirement: return updated value
The system SHALL return the updated value.
#### Scenario: read value
- **WHEN** a caller reads the value
- **THEN** the updated value is returned

## Design
Update the existing example module in place.

## Gotchas / policy flags
None.

## Open questions carried forward
None.
"""

    @staticmethod
    def plan_body():
        return """# Plan: example

## Files that change
`src/app.py` — return the updated value.

## Order of work
- [x] 1.1 Update and verify the value — verify: `python3 -m unittest`

## Risks
None.

## Proof
Run the focused unit test and inspect the result.

## Review route
An independent fresh-context subagent checks the committed snapshot.
"""

    def report_fields(self, verdict="pass", isolation="subagent"):
        fields = {
            "slug": self.slug,
            "intent_digest": self.intent_digest,
            "spec_digest": self.spec_digest,
            "plan_digest": self.plan_digest,
            "reviewed_head": self.reviewed,
            "verdict": verdict,
            "isolation": isolation,
        }
        return fields

    def report_body(self, findings="None.", not_checked="None."):
        paths = command(
            "git", "diff", "--name-only", self.base, self.reviewed, cwd=self.root
        ).stdout.splitlines()
        changed_paths = ", ".join(f"`{path}`" for path in paths)
        return f"""# Report: example

## Change inspected
Base commit: `{self.base}`. Reviewed HEAD: `{self.reviewed}`. Changed paths: {changed_paths}. The working tree was clean during review, with no untracked paths. The report records all three approved artifact digests.

## What shipped
The example module now returns the updated value required by the spec.

## Deviations from plan
None.

## Verification
The required check passed and its result was observed.

### Completeness
- PASS | action: inspect completed plan task and return updated value requirement | observed: the task is ticked and source returns the updated value | evidence: `intent/example/plan.md` and `src/app.py`.

### Correctness
- PASS | action: run read value scenario with a focused source check | observed: the updated value is returned | evidence: `src/app.py` inspection output.

### Coherence
- PASS | action: review full committed source diff for logic and regressions | observed: the existing caller remains compatible | evidence: `git diff` output and `src/app.py`.

## Independent challenge
A fresh reviewer challenged whether the existing caller remained compatible; the diff and requirement evidence resolved that concern.

## Findings
{findings}

## Not checked
{not_checked}

## Release handoff
None.

## Verdict
{self._verdict_from_fields} — the required behavior is supported by the observed evidence.
"""

    @property
    def _verdict_from_fields(self):
        # Filled by write_report/mutate_report before serializing the body.
        return getattr(self, "verdict", "pass")

    def write_report(self, verdict="pass", isolation="subagent", findings="None.", not_checked="None."):
        self.verdict = verdict
        fields = self.report_fields(verdict, isolation)
        self.write(f"intent/{self.slug}/report.md", self.markdown(fields, self.report_body(findings, not_checked)))

    def update_approved_digest(self, name):
        path = self.change / name
        fields, body = self.read_frontmatter(path)
        fields["approved_digest"] = "pending"
        path.write_text(self.markdown(fields, body), encoding="utf-8")
        fields["approved_digest"] = self.digest(f"intent/{self.slug}/{name}")
        path.write_text(self.markdown(fields, body), encoding="utf-8")

    @staticmethod
    def read_frontmatter(path):
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        close = lines.index("---", 1)
        fields = {}
        for line in lines[1:close]:
            key, value = line.split(":", 1)
            fields[key] = value.strip()
        return fields, "\n".join(lines[close + 1:]).strip()


class StatusRouterTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = ProductRepo(self.temp.name)

    def route(self):
        result = command(sys.executable, str(VALIDATOR), "route", cwd=self.repo.root)
        return result.stdout.split("  next: ", 1)[1].strip()

    def archive_check(self):
        return command(sys.executable, str(VALIDATOR), "archive-check", self.repo.slug, str(self.repo.root), cwd=self.repo.root, check=False)

    def mutate_report(self, verdict="pass", isolation="subagent", findings="None.", not_checked="None."):
        self.repo.write_report(verdict, isolation, findings, not_checked)
        self.repo.commit("update report")

    def test_valid_content_bound_report_routes_to_archive(self):
        self.assertEqual(self.route(), "sdlc-archive")
        self.assertEqual(self.archive_check().returncode, 0)

    @unittest.skipUnless(shutil.which("sh") and shutil.which("python3"), "optional POSIX wrapper unavailable")
    def test_optional_posix_wrapper_matches_portable_python_route(self):
        wrapped = command("sh", str(STATUS), cwd=self.repo.root)
        direct = command(sys.executable, str(VALIDATOR), "route", cwd=self.repo.root)
        self.assertEqual(wrapped.stdout, direct.stdout)

    def test_portable_checks_resolve_spaced_resource_and_product_paths(self):
        with TemporaryDirectory(prefix="ai sdlc é ") as temporary:
            root = Path(temporary)
            repo = ProductRepo(root / "product repo")
            resources = root / "installed skill" / "scripts"
            shutil.copytree(CONTINUE_SCRIPTS, resources, ignore=shutil.ignore_patterns("__pycache__"))
            validator = resources / "validator.py"
            route = command(sys.executable, str(validator), "route", str(repo.root), cwd=root)
            self.assertIn("next: sdlc-archive", route.stdout)
            checked = command(sys.executable, str(validator), "archive-check", repo.slug, str(repo.root), cwd=root)
            self.assertIn("example: valid", checked.stdout)

    def approve_with_high_confidence(self):
        review = """

## Decision review
Confidence: high. The explicit outcome is to return the updated value while
preserving the existing caller. Current src/app.py and its reviewed diff support
that approach. The read-value scenario and focused verification cover the caller
contract and unchanged failure behavior. No material assumption or conflicting
evidence remains. A separate challenge was skipped on this evidence; final
independent verification is still required.
"""
        for name, digest_attribute, dependency in [
            ("intent.md", "intent_digest", None),
            ("spec.md", "spec_digest", "intent_digest"),
            ("plan.md", "plan_digest", "spec_digest"),
        ]:
            fields, body = self.repo.read_frontmatter(self.repo.change / name)
            fields["approved_by"] = "autonomous"
            if dependency:
                fields[dependency] = getattr(self.repo, dependency)
            digest = self.repo.write_approved(name, body + review, fields)
            setattr(self.repo, digest_attribute, digest)
        self.repo.commit("approve evidence-supported autonomous decisions")
        self.repo.reviewed = self.repo.head()
        self.repo.write_report()
        report = self.repo.change / "report.md"
        text = report.read_text(encoding="utf-8")
        before, rest = text.split("## Independent challenge\n", 1)
        _, after = rest.split("## Findings\n", 1)
        report.write_text(
            before + "## Independent challenge\n" + review.split("## Decision review\n", 1)[1]
            + "\n## Findings\n" + after,
            encoding="utf-8",
        )
        self.repo.commit("record fresh independent verification without extra challenge")

    def test_high_confidence_autonomous_approvals_can_archive_without_extra_challenge(self):
        self.approve_with_high_confidence()
        self.assertEqual(self.route(), "sdlc-archive")
        self.assertEqual(self.archive_check().returncode, 0)

    def test_high_confidence_does_not_bypass_approval_digest(self):
        self.approve_with_high_confidence()
        intent = self.repo.change / "intent.md"
        intent.write_text(
            intent.read_text(encoding="utf-8").replace("updated value", "different value"),
            encoding="utf-8",
        )
        self.assertIn("reconcile intent approval", self.route())
        self.assertNotEqual(self.archive_check().returncode, 0)

    def test_high_confidence_does_not_bypass_independent_review(self):
        self.approve_with_high_confidence()
        self.mutate_report(isolation="none")
        self.assertIn("sdlc-verify (invalid or stale evidence:", self.route())
        self.assertNotEqual(self.archive_check().returncode, 0)

    def test_high_confidence_does_not_preserve_a_verdict_after_source_changes(self):
        self.approve_with_high_confidence()
        self.repo.write("src/app.py", "value = 'changed after review'\n")
        self.repo.commit("change independently reviewed source")
        self.assertIn("sdlc-verify (invalid or stale evidence:", self.route())
        self.assertNotEqual(self.archive_check().returncode, 0)

    def test_plan_compaction_requires_reapproval_and_fresh_verification(self):
        self.approve_with_high_confidence()
        plan = self.repo.change / "plan.md"
        fields, body = self.repo.read_frontmatter(plan)
        original_base = fields["base_commit"]
        original_tasks = [line for line in body.splitlines() if "- [x]" in line]
        compact_body = body.split("## Decision review\n", 1)[0] + """## Decision review
Confidence: high. src/app.py and the read-value scenario establish the explicit
outcome and caller contract. Focused verification covers failure behavior; no
material conflicting evidence remains. Superseded rationale is retained in Git.
"""
        plan.write_text(self.repo.markdown(fields, compact_body), encoding="utf-8")
        self.assertIn("reconcile approved plan", self.route())
        self.assertNotEqual(self.archive_check().returncode, 0)
        self.repo.plan_digest = self.repo.write_approved("plan.md", compact_body, fields)
        self.repo.commit("reapprove compact operative plan")
        self.assertIn("sdlc-verify", self.route())
        self.assertNotEqual(self.archive_check().returncode, 0)
        current_fields, current_body = self.repo.read_frontmatter(plan)
        self.assertEqual(current_fields["base_commit"], original_base)
        self.assertEqual([line for line in current_body.splitlines() if "- [x]" in line], original_tasks)
        self.assertIn("## Proof\nRun the focused unit test", current_body)
        self.repo.reviewed = self.repo.head()
        self.repo.write_report()
        self.repo.commit("record fresh verification of compact plan")
        self.assertEqual(self.route(), "sdlc-archive")
        self.assertEqual(self.archive_check().returncode, 0)

    def test_frontmatter_only_report_fails_closed(self):
        report = self.repo.change / "report.md"
        report.write_text(
            f"---\nslug: {self.repo.slug}\nintent_digest: {self.repo.intent_digest}\n"
            f"spec_digest: {self.repo.spec_digest}\nplan_digest: {self.repo.plan_digest}\n"
            f"reviewed_head: {self.repo.reviewed}\nverdict: pass\nisolation: subagent\n---\n",
            encoding="utf-8",
        )
        self.repo.commit("replace report with frontmatter only")
        self.assertIn("sdlc-verify (invalid report:", self.route())
        self.assertNotEqual(self.archive_check().returncode, 0)

    def test_frontmatter_after_body_fails_closed(self):
        report = self.repo.change / "report.md"
        report.write_text(report.read_text(encoding="utf-8").replace(
            "# Report: example\n",
            "# Report: example\n\n---\nverdict: pass\n---\n",
            1,
        ), encoding="utf-8")
        self.repo.commit("append a late metadata block")
        self.assertIn("sdlc-verify (invalid report:", self.route())

    def test_numbered_critical_finding_blocks_archive(self):
        self.mutate_report(findings="1. **CRITICAL**: broken behavior at `src/app.py:1`.")
        self.assertEqual(self.route(), "sdlc-apply (fix findings) then sdlc-verify")
        self.assertNotEqual(self.archive_check().returncode, 0)

    def test_bold_critical_finding_blocks_archive(self):
        self.mutate_report(findings="- **CRITICAL**: broken behavior at `src/app.py:1`.")
        self.assertEqual(self.route(), "sdlc-apply (fix findings) then sdlc-verify")

    def test_ambiguous_negated_findings_prose_fails_closed(self):
        self.mutate_report(findings="No CRITICAL, WARNING, or SUGGESTION findings.")
        self.assertIn("sdlc-verify (invalid or stale evidence:", self.route())

    def test_indented_critical_finding_cannot_disappear(self):
        self.mutate_report(findings="- WARNING: possible issue at `src/app.py:1`.\n  1. CRITICAL: hidden issue at `src/app.py:1`.")
        self.assertEqual(self.route(), "sdlc-apply (fix findings) then sdlc-verify")

    def test_indented_unfinished_task_is_rejected(self):
        plan = self.repo.change / "plan.md"
        text = plan.read_text(encoding="utf-8").replace(
            "- [x] 1.1 Update and verify the value — verify: `python3 -m unittest`",
            "  - [ ] 1.1 Update and verify the value — verify: `python3 -m unittest`",
        )
        plan.write_text(text, encoding="utf-8")
        self.repo.update_approved_digest("plan.md")
        self.assertIn("repair plan (", self.route())
        self.assertNotEqual(self.archive_check().returncode, 0)

    def test_template_task_cannot_be_ticked_as_completed_work(self):
        plan = self.repo.change / "plan.md"
        plan.write_text(plan.read_text(encoding="utf-8").replace(
            "## Risks", "- [x] 1.2 Next step in this area — verify: ...\n\n## Risks"
        ), encoding="utf-8")
        self.repo.update_approved_digest("plan.md")
        self.assertIn("task entry still contains template guidance", self.route())

    def test_template_prose_before_tasks_is_rejected(self):
        plan = self.repo.change / "plan.md"
        plan.write_text(plan.read_text(encoding="utf-8").replace(
            "## Order of work\n", "## Order of work\nBuild and verify order, not a task dump.\n"
        ), encoding="utf-8")
        self.repo.update_approved_digest("plan.md")
        self.assertIn("unexpected non-task content", self.route())

    def test_zero_box_plan_cannot_verify(self):
        plan = self.repo.change / "plan.md"
        text = plan.read_text(encoding="utf-8").replace(
            "- [x] 1.1 Update and verify the value — verify: `python3 -m unittest`\n", ""
        )
        plan.write_text(text, encoding="utf-8")
        self.repo.update_approved_digest("plan.md")
        self.assertEqual(self.route(), "repair plan (0 boxes)")

    def test_zero_box_draft_plan_cannot_be_approved(self):
        plan = self.repo.change / "plan.md"
        text = plan.read_text(encoding="utf-8").replace("status: done", "status: draft")
        text = text.replace("- [x] 1.1 Update and verify the value — verify: `python3 -m unittest`\n", "")
        plan.write_text(text, encoding="utf-8")
        self.assertEqual(self.route(), "repair plan (0 boxes)")

    def test_done_plan_with_unticked_box_is_inconsistent(self):
        plan = self.repo.change / "plan.md"
        plan.write_text(plan.read_text(encoding="utf-8").replace("[x]", "[ ]"), encoding="utf-8")
        self.assertEqual(self.route(), "repair inconsistent plan (done with unticked boxes)")

    def test_implementing_session_disclosure_invalidates_report(self):
        self.mutate_report(not_checked="Verified in the implementing session.")
        self.assertIn("sdlc-verify (invalid or stale evidence:", self.route())

    def test_source_commit_after_review_invalidates_report(self):
        self.repo.write("src/app.py", "value = 'changed after review'\n")
        self.repo.commit("change source after review")
        self.assertIn("sdlc-verify (invalid or stale evidence: implementation changed after verification", self.route())

    def test_report_edit_after_review_invalidates_previous_pass(self):
        self.mutate_report(not_checked="The deployment environment was outside this local review.")
        self.assertIn("sdlc-verify (invalid or stale evidence: report must be committed once", self.route())

    def test_dirty_and_untracked_worktree_blocks_archive(self):
        self.repo.write("src/app.py", "value = 'dirty'\n")
        self.assertIn("sdlc-verify (invalid or stale evidence: working tree is dirty", self.route())
        self.assertNotEqual(self.archive_check().returncode, 0)
        (self.repo.root / "untracked.txt").write_text("untracked\n", encoding="utf-8")
        self.assertNotEqual(self.archive_check().returncode, 0)

    def test_quoted_status_scalar_is_supported(self):
        self.assertEqual(self.route(), "sdlc-archive")

    def test_approval_digest_binds_content_but_ignores_status_and_plan_checkmarks(self):
        original_plan = self.repo.digest("intent/example/plan.md")
        plan = self.repo.change / "plan.md"
        plan.write_text(plan.read_text(encoding="utf-8").replace("[x]", "[ ]"), encoding="utf-8")
        self.assertEqual(original_plan, self.repo.digest("intent/example/plan.md"))
        plan.write_text(plan.read_text(encoding="utf-8").replace("[ ]", "[x]").replace("Update and verify", "Change and verify"), encoding="utf-8")
        self.assertNotEqual(original_plan, self.repo.digest("intent/example/plan.md"))

    def test_changed_approved_intent_requires_reapproval(self):
        path = self.repo.change / "intent.md"
        path.write_text(path.read_text(encoding="utf-8").replace("updated value", "different value"), encoding="utf-8")
        self.assertIn("reconcile intent approval (intent approval digest is stale", self.route())

    def test_reapproval_after_review_cannot_retroactively_validate_old_head(self):
        command("git", "reset", "--hard", self.repo.reviewed, cwd=self.repo.root)
        spec = self.repo.change / "spec.md"
        spec.write_text(spec.read_text(encoding="utf-8").replace("Update the existing example module in place.", "Update the existing example module and its callers."), encoding="utf-8")
        self.repo.update_approved_digest("spec.md")
        self.repo.spec_digest = self.repo.digest("intent/example/spec.md")
        plan = self.repo.change / "plan.md"
        plan.write_text(plan.read_text(encoding="utf-8").replace(self.repo.read_frontmatter(plan)[0]["spec_digest"], self.repo.spec_digest), encoding="utf-8")
        self.repo.update_approved_digest("plan.md")
        self.repo.plan_digest = self.repo.digest("intent/example/plan.md")
        self.repo.commit("reapprove changed artifacts")
        self.repo.write_report()
        self.repo.commit("record later report")
        self.assertIn("approval changed after reviewed_head", self.route())

    def test_approved_spec_requires_scenario_structure(self):
        spec = self.repo.change / "spec.md"
        spec.write_text(spec.read_text(encoding="utf-8").replace("- **THEN** the updated value is returned", "- **AND** the updated value is returned"), encoding="utf-8")
        self.repo.update_approved_digest("spec.md")
        self.assertIn("needs WHEN and THEN", self.route())

    def test_duplicate_scenario_names_are_rejected(self):
        spec = self.repo.change / "spec.md"
        spec.write_text(spec.read_text(encoding="utf-8").replace("## Design", "#### Scenario: read value\n- **WHEN** another caller reads the value\n- **THEN** the updated value is returned\n\n## Design"), encoding="utf-8")
        self.repo.update_approved_digest("spec.md")
        self.assertIn("duplicate scenario name", self.route())

    def test_legitimate_pending_word_in_report_is_allowed(self):
        command("git", "reset", "--hard", self.repo.reviewed, cwd=self.repo.root)
        self.repo.write_report()
        report = self.repo.change / "report.md"
        report.write_text(report.read_text(encoding="utf-8").replace("## Release handoff\nNone.", "## Release handoff\nRollout pending approval by the release owner; observe the example caller after deployment."), encoding="utf-8")
        self.repo.commit("record report with release handoff")
        self.assertEqual(self.route(), "sdlc-archive")

    def test_passing_report_requires_structured_check_evidence(self):
        report = self.repo.change / "report.md"
        report.write_text(report.read_text(encoding="utf-8").replace("- PASS | action: run read value scenario with a focused source check | observed: the updated value is returned | evidence: `src/app.py` inspection output.", "The scenario was checked."), encoding="utf-8")
        self.repo.commit("weaken verification evidence")
        self.assertIn("needs a check with status, action, observation, and evidence", self.route())

    def test_scenario_name_in_prose_does_not_count_as_evidence(self):
        report = self.repo.change / "report.md"
        report.write_text(report.read_text(encoding="utf-8").replace("action: run read value scenario with a focused source check", "action: run focused source check"), encoding="utf-8")
        self.repo.commit("remove scenario from check action")
        self.assertIn("Correctness check omits scenario 'read value'", self.route())

    def test_malformed_failing_report_does_not_route_to_implementation(self):
        self.mutate_report(verdict="fail", findings="A problem was found.")
        self.assertIn("sdlc-verify (invalid failing report:", self.route())

    def test_failing_report_needs_an_observed_failed_check(self):
        self.mutate_report(verdict="fail", findings="- CRITICAL: broken behavior at `src/app.py:1`.")
        self.assertIn("failing report needs a FAIL check entry", self.route())

    def test_valid_failing_report_routes_to_repair(self):
        self.repo.write_report(verdict="fail", findings="- CRITICAL: broken behavior at `src/app.py:1`.")
        report = self.repo.change / "report.md"
        report.write_text(report.read_text(encoding="utf-8").replace(
            "- PASS | action: run read value scenario", "- FAIL | action: run read value scenario"
        ), encoding="utf-8")
        self.repo.commit("record observed failure")
        self.assertEqual(self.route(), "sdlc-apply (fix findings) then sdlc-verify")

    def test_finding_requires_file_line(self):
        self.mutate_report(verdict="fail", findings="- CRITICAL: a required behavior is broken")
        self.assertIn("needs file:line", self.route())

    def test_blocked_report_rejects_extra_unchecked_prose(self):
        self.mutate_report(
            verdict="blocked",
            isolation="none",
            not_checked="Reason: the environment is unavailable.\nRecovery: restore it.\nEverything else was fine.",
        )
        self.assertIn("exactly one nonempty Reason: and Recovery: line", self.route())

    def test_blocked_report_routes_to_recovery_and_never_archives(self):
        self.mutate_report(
            verdict="blocked",
            isolation="none",
            not_checked="Reason: no independent reviewer could be dispatched.\nRecovery: start a fresh review session and rerun verification.",
        )
        self.assertEqual(self.route(), "sdlc-verify (resolve blocked verification prerequisites)")
        self.assertNotEqual(self.archive_check().returncode, 0)

    def test_dispatched_reviewer_can_report_blocked_environment(self):
        self.mutate_report(
            verdict="blocked",
            isolation="subagent",
            not_checked="Reason: the test environment is unavailable.\nRecovery: restore the environment and rerun independent verification.",
        )
        self.assertEqual(self.route(), "sdlc-verify (resolve blocked verification prerequisites)")
        self.assertNotEqual(self.archive_check().returncode, 0)

    def test_isolation_none_is_invalid_for_a_passing_report(self):
        self.mutate_report(isolation="none")
        self.assertIn("sdlc-verify (invalid or stale evidence:", self.route())

    def test_pending_verdict_routes_to_verify(self):
        report = self.repo.change / "report.md"
        report.write_text(report.read_text(encoding="utf-8").replace("verdict: pass", "verdict: pending"), encoding="utf-8")
        self.repo.commit("mark report pending")
        self.assertEqual(self.route(), "sdlc-verify")

    def test_invalid_spec_status_is_reported(self):
        spec = self.repo.change / "spec.md"
        spec.write_text(spec.read_text(encoding="utf-8").replace("status: done", "status: unknown"), encoding="utf-8")
        self.assertEqual(self.route(), "inspect invalid spec status (unknown)")

    def test_draft_intent_waits_for_acceptance(self):
        intent = self.repo.change / "intent.md"
        intent.write_text(intent.read_text(encoding="utf-8").replace('status: "done"', "status: draft"), encoding="utf-8")
        self.assertEqual(self.route(), "present intent; on accept set accepted, then sdlc-design")

    def test_draft_spec_routes_to_design_even_when_plan_exists(self):
        spec = self.repo.change / "spec.md"
        spec.write_text(spec.read_text(encoding="utf-8").replace("status: done", "status: draft"), encoding="utf-8")
        self.assertEqual(self.route(), "sdlc-design (review draft and readiness before approval)")

    def test_reopened_plan_routes_to_reconciliation(self):
        plan = self.repo.change / "plan.md"
        plan.write_text(plan.read_text(encoding="utf-8").replace("status: done", "status: draft"), encoding="utf-8")
        self.assertEqual(self.route(), "sdlc-apply (reconcile draft plan with approved spec before approval)")

    def test_context_only_resumes_exploration(self):
        (self.repo.change / "intent.md").unlink()
        (self.repo.change / "context.md").write_text("# Context\n\nCarry-forward evidence.\n", encoding="utf-8")
        self.assertEqual(self.route(), "sdlc-explore (context.md only), then sdlc-plan when ready")

    def test_missing_intent_routes_to_plan(self):
        (self.repo.change / "intent.md").unlink()
        for path in (self.repo.change / "spec.md", self.repo.change / "plan.md", self.repo.change / "report.md"):
            path.unlink()
        self.assertEqual(self.route(), "sdlc-plan (no intent.md)")


class ValidatorPackagingTests(unittest.TestCase):
    def test_standalone_validator_and_fingerprint_copies_are_identical(self):
        self.assertEqual(
            (CONTINUE_SCRIPTS / "validator.py").read_bytes(),
            (ARCHIVE_SCRIPTS / "validator.py").read_bytes(),
        )
        fingerprint_copies = [
            ARCHIVE_SCRIPTS / "fingerprint.py",
            ROOT / "skills/sdlc-plan/scripts/fingerprint.py",
            ROOT / "skills/sdlc-design/scripts/fingerprint.py",
            ROOT / "skills/sdlc-apply/scripts/fingerprint.py",
            ROOT / "skills/sdlc-verify/scripts/fingerprint.py",
        ]
        for copy in fingerprint_copies:
            with self.subTest(copy=copy):
                self.assertEqual(FINGERPRINT.read_bytes(), copy.read_bytes())

    def test_status_shell_script_is_a_thin_python_wrapper(self):
        content = STATUS.read_text(encoding="utf-8")
        self.assertIn('validator.py" route', content)
        self.assertNotIn("awk", content)


if __name__ == "__main__":
    unittest.main()
