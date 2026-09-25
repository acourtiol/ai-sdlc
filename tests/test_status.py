"""Regression checks for the continue skill's deterministic status router."""

from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "skills/sdlc-continue/scripts/status.sh"


class StatusRouterTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.change = Path(self.temp.name) / "intent" / "example"
        self.change.mkdir(parents=True)

    def write(self, name, frontmatter="", body=""):
        (self.change / name).write_text(
            f"---\n{frontmatter}---\n{body}", encoding="utf-8"
        )

    def route(self):
        result = subprocess.run(
            ["sh", str(SCRIPT)],
            cwd=self.temp.name,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.split("  next: ", 1)[1].strip()

    def ready_plan(self, status="done", boxes="- [x] 1. Verify — verify: test"):
        self.write("intent.md", "status: done\n")
        self.write("spec.md", "status: done\n")
        self.write("plan.md", f"status: {status}\n", f"## Order of work\n{boxes}\n")

    def report(self, verdict="pass", isolation="subagent", findings="None."):
        self.write(
            "report.md",
            f"verdict: {verdict}\nisolation: {isolation}\n",
            f"## Findings\n\n{findings}\n\n## Not checked\n\nNone.\n",
        )

    def test_negated_critical_in_prose_does_not_block_pass(self):
        self.ready_plan()
        self.report(findings="No CRITICAL, WARNING, or SUGGESTION findings.")
        self.assertEqual(self.route(), "sdlc-archive")

    def test_critical_finding_blocks_even_with_pass_verdict(self):
        self.ready_plan()
        self.report(findings="- CRITICAL — broken auth. `src/auth.py:42`")
        self.assertEqual(self.route(), "sdlc-apply (fix findings) then sdlc-verify")

    def test_bold_critical_finding_blocks(self):
        self.ready_plan()
        self.report(findings="- **CRITICAL**: broken auth. `src/auth.py:42`")
        self.assertEqual(self.route(), "sdlc-apply (fix findings) then sdlc-verify")

    def test_zero_box_plan_cannot_verify(self):
        self.ready_plan(status="planned", boxes="")
        self.assertEqual(self.route(), "repair plan (0 boxes)")

    def test_zero_box_draft_plan_cannot_be_approved(self):
        self.ready_plan(status="draft", boxes="")
        self.assertEqual(self.route(), "repair plan (0 boxes)")

    def test_done_plan_with_unticked_box_is_inconsistent(self):
        self.ready_plan(boxes="- [ ] 1. Verify — verify: test")
        self.assertEqual(self.route(), "repair inconsistent plan (done with unticked boxes)")

    def test_invalid_isolation_cannot_route_to_archive(self):
        self.ready_plan()
        self.report(isolation="pending")
        self.assertEqual(self.route(), "sdlc-verify (invalid isolation)")

    def test_pending_verdict_cannot_route_to_archive(self):
        self.ready_plan()
        self.report(verdict="pending")
        self.assertEqual(self.route(), "sdlc-verify")

    def test_invalid_spec_status_cannot_route_to_apply(self):
        self.write("intent.md", "status: accepted\n")
        self.write("spec.md", "status: unknown\n")
        self.assertEqual(self.route(), "inspect invalid spec status (unknown)")

    def test_context_only_resumes_exploration(self):
        (self.change / "context.md").write_text("# Context\n", encoding="utf-8")
        self.assertEqual(
            self.route(), "sdlc-explore (context.md only), then sdlc-plan when ready"
        )


if __name__ == "__main__":
    unittest.main()
