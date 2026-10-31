import os
import subprocess
import sys
import tempfile
import unittest

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "skills", "play-store-review", "scripts", "validate_report.py")

GOOD = """# Report

## Verdict
Not ready. Two blockers.

## Blocked at the door
**[CRITICAL] Restricted SMS permission (Confirmed)**
- Evidence: app/src/main/AndroidManifest.xml:5 declares READ_SMS
- Rule: SMS and Call Log policy
- Fix: remove it or use the SMS Retriever API

### [HIGH] Missing account deletion link (Verify)
Evidence: no web deletion URL found
Rule: Account deletion
Fix: add the link

## Could not verify
- Data safety form: not in the repository.
"""


def run(text):
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
        f.write(text)
    try:
        p = subprocess.run([sys.executable, "-B", SCRIPT, f.name], capture_output=True, text=True)
        return p.returncode, p.stdout
    finally:
        os.unlink(f.name)


class ValidateReportTests(unittest.TestCase):
    def test_good_report_is_clean(self):
        self.assertEqual(run(GOOD), (0, "OK\n"))

    def test_missing_fix_and_label(self):
        code, out = run(GOOD.replace("- Fix: remove it or use the SMS Retriever API\n", "").replace(" (Confirmed)**", "**"))
        self.assertEqual(code, 1)
        self.assertIn(":7: finding is missing a 'Fix:' line", out)
        self.assertIn(":7: finding needs a (Confirmed) or (Verify) label", out)

    def test_missing_required_heading(self):
        code, out = run(GOOD.replace("## Could not verify", "## Notes"))
        self.assertEqual(code, 1)
        self.assertIn("missing required heading '## Could not verify'", out)
        self.assertIn("unexpected heading '## Notes'", out)

    def test_headings_out_of_order(self):
        code, out = run(GOOD + "\n## Order of work\n1. x\n\n## Upcoming deadlines\n- y\n")
        self.assertEqual(code, 1)
        self.assertIn("'## Upcoming deadlines' is out of order", out)

    def test_verdict_wording(self):
        code, out = run(GOOD.replace("Not ready. Two blockers.", "Looks fine"))
        self.assertEqual(code, 1)
        self.assertIn("Verdict must say", out)
        for ok in ("Ready", "Fixable before submission"):
            self.assertEqual(run(GOOD.replace("Not ready. Two blockers.", ok))[0], 0)
        self.assertEqual(run(GOOD.replace("Not ready", "Unready"))[0], 1)

    def test_findings_in_code_fences_are_ignored(self):
        self.assertEqual(run(GOOD + "\n```\n[HIGH] example only\n```\n")[0], 0)

    def test_bold_prefixed_finding_fields(self):
        text = GOOD.replace("- Evidence:", "- **Evidence:**").replace("- Rule:", "- **Rule**:")
        self.assertEqual(run(text)[0], 0)

    def test_unreadable_file(self):
        p = subprocess.run([sys.executable, "-B", SCRIPT, "/nonexistent.md"], capture_output=True, text=True)
        self.assertEqual(p.returncode, 2)


if __name__ == "__main__":
    unittest.main()
