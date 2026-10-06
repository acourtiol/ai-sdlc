import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "skills" / "sdlc-continue" / "scripts" / "status.sh"


def run_status(repo: Path) -> str:
    result = subprocess.run(["sh", str(SCRIPT), str(repo)], capture_output=True, text=True, check=True)
    return result.stdout.strip()


def write(repo: Path, rel: str, text: str) -> None:
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def intent(status: str, tier: str, steps: str = "") -> str:
    return f"---\nstatus: {status}   # comment\ntier: {tier}\nslug: x\n---\n\n# Intent\n\n## Steps\n{steps}\n## Result\n"


class StatusTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_no_intents(self) -> None:
        self.assertEqual(run_status(self.repo), "no open intents")

    def test_archive_is_ignored(self) -> None:
        write(self.repo, "intent/archive/2026-01-01-old/intent.md", intent("done", "change"))
        self.assertEqual(run_status(self.repo), "no open intents")

    def test_draft_needs_acceptance(self) -> None:
        write(self.repo, "intent/a/intent.md", intent("draft", "change"))
        self.assertIn("accept or correct the intent", run_status(self.repo))

    def test_accepted_change_with_open_steps(self) -> None:
        write(self.repo, "intent/a/intent.md", intent("accepted", "change", "- [x] one\n- [ ] two\n"))
        out = run_status(self.repo)
        self.assertIn("steps 1/2", out)
        self.assertIn("continue steps (sdlc-apply)", out)

    def test_accepted_without_steps_goes_to_apply(self) -> None:
        write(self.repo, "intent/a/intent.md", intent("accepted", "change"))
        self.assertIn("write the steps and build (sdlc-apply)", run_status(self.repo))

    def test_finished_change_needs_review(self) -> None:
        write(self.repo, "intent/a/intent.md", intent("accepted", "change", "- [x] one\n"))
        self.assertIn("independent review (sdlc-verify)", run_status(self.repo))

    def test_reviewed_change_waits_for_user(self) -> None:
        write(self.repo, "intent/a/intent.md", intent("accepted", "change", "- [x] one\n"))
        write(self.repo, "intent/a/report.md", "---\nverdict: pass\n---\n")
        self.assertIn("user acceptance, then close", run_status(self.repo))

    def test_critical_finished_needs_review(self) -> None:
        write(self.repo, "intent/a/intent.md", intent("accepted", "critical", "- [x] one\n"))
        self.assertIn("independent review (sdlc-verify)", run_status(self.repo))

    def test_critical_with_passing_report_waits_for_user(self) -> None:
        write(self.repo, "intent/a/intent.md", intent("accepted", "critical", "- [x] one\n"))
        write(self.repo, "intent/a/report.md", "---\nverdict: pass\n---\n")
        self.assertIn("user acceptance, then close", run_status(self.repo))

    def test_legacy_intent_without_tier_is_a_change(self) -> None:
        write(self.repo, "intent/a/intent.md", "---\nstatus: accepted\nslug: a\napproved_digest: sha256:x\n---\n# Intent\n")
        write(self.repo, "intent/a/plan.md", "---\nstatus: planned\n---\n## Order of work\n- [ ] a\n- [x] b\n")
        out = run_status(self.repo)
        self.assertIn("tier change", out)
        self.assertIn("steps 1/2", out)

    def test_done_is_ready_to_close(self) -> None:
        write(self.repo, "intent/a/intent.md", intent("done", "change"))
        self.assertIn("close: delete the folder", run_status(self.repo))


    def test_failed_report_means_repair(self) -> None:
        write(self.repo, "intent/a/intent.md", intent("accepted", "change", "- [x] one\n"))
        write(self.repo, "intent/a/report.md", "---\nverdict: fail\n---\n")
        self.assertIn("repair the findings", run_status(self.repo))

    def test_blocked_report_restores_route(self) -> None:
        write(self.repo, "intent/a/intent.md", intent("accepted", "change", "- [x] one\n"))
        write(self.repo, "intent/a/report.md", "---\nverdict: blocked\n---\n")
        self.assertIn("restore a fresh review route", run_status(self.repo))

    def test_crlf_and_quotes_are_tolerated(self) -> None:
        text = '---\r\nstatus: accepted\r\ntier: "critical"\r\n---\r\n## Steps\r\n- [x] one\r\n'
        write(self.repo, "intent/a/intent.md", text)
        out = run_status(self.repo)
        self.assertIn("tier critical", out)
        self.assertIn("accepted", out)

    def test_legacy_spec_marks_critical(self) -> None:
        write(self.repo, "intent/a/intent.md", "---\nstatus: accepted\n---\n## Steps\n- [ ] one\n")
        write(self.repo, "intent/a/spec.md", "---\nstatus: approved\n---\n")
        self.assertIn("tier critical", run_status(self.repo))


if __name__ == "__main__":
    unittest.main()
