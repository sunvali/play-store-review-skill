#!/usr/bin/env python3
"""Check the structure of a Play review report.

Example: python3 -B scripts/validate_report.py REPORT.md
Prints each problem with its line number. Exit 1 on problems, 0 when clean.
"""
import re
import sys

HEADINGS = ["Verdict", "Blocked at the door", "Will likely be rejected or removed",
            "Upcoming deadlines", "Could not verify", "Order of work"]
REQUIRED = {"Verdict", "Could not verify"}
VERDICTS = ["Fixable before submission", "Not ready", "Ready"]
FINDING = re.compile(r"^\s*(?:#+\s*|[-*]\s+)?\**\s*\[(CRITICAL|HIGH|MEDIUM)\]")
FIELD = r"^\s*(?:[-*]\s+)?\**%s\**\s*:"


def check(lines):
    problems, seen, fence = [], [], False
    findings, verdict_start = [], None   # findings: [start_line, [lines]]
    current = None
    for n, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        m = re.match(r"##\s+(.*?)\s*$", line)
        if m:
            current = None
            title = m.group(1)
            if title not in HEADINGS:
                problems.append((n, "unexpected heading '## %s'" % title))
                continue
            seen.append((title, n))
            if title == "Verdict":
                verdict_start = n
            continue
        if FINDING.match(line):
            current = [n, [line]]
            findings.append(current)
        elif current is not None:
            current[1].append(line)
    names = [t for t, _ in seen]
    for req in sorted(REQUIRED):
        if req not in names:
            problems.append((1, "missing required heading '## %s'" % req))
    order = [HEADINGS.index(t) for t in names]
    for (title, n), prev, cur in zip(seen[1:], order, order[1:]):
        if cur <= prev:
            problems.append((n, "heading '## %s' is out of order or repeated" % title))
    if verdict_start:
        body = []
        for line in lines[verdict_start:]:
            if line.startswith("## "):
                break
            body.append(line)
        text = "\n".join(body)
        if not any(re.search(r"(?<![A-Za-z])%s(?![A-Za-z])" % v, text) for v in VERDICTS):
            problems.append((verdict_start, "Verdict must say Ready, Fixable before submission, or Not ready"))
    for start, block in findings:
        text = "\n".join(block)
        for field in ("Evidence", "Rule", "Fix"):
            if not re.search(FIELD % field, text, re.M):
                problems.append((start, "finding is missing a '%s:' line" % field))
        if "(Confirmed)" not in text and "(Verify)" not in text:
            problems.append((start, "finding needs a (Confirmed) or (Verify) label"))
    return sorted(problems)


def main(argv):
    if len(argv) != 2 or argv[1] in ("-h", "--help"):
        print(__doc__.strip())
        return 2 if len(argv) != 2 else 0
    try:
        with open(argv[1], encoding="utf-8") as f:
            lines = f.read().splitlines()
    except OSError as e:
        print("cannot read %s: %s" % (argv[1], e.strerror))
        return 2
    problems = check(lines)
    for n, msg in problems:
        print("%s:%d: %s" % (argv[1], n, msg))
    if not problems:
        print("OK")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
