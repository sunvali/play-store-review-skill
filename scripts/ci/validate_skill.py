#!/usr/bin/env python3
"""Validate every skill under skills/: frontmatter, links, sources, versions, freshness.

Example: python3 -B scripts/ci/validate_skill.py [--strict]
Failures exit 1. Freshness findings (stale verified_on, passed upcoming dates) are
warnings unless --strict.
"""
import datetime
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ALLOWED = ("support.google.com/googleplay", "developer.android.com", "play.google.com/about",
           "support.google.com/paymentscenter", "support.google.com/android-developer-console")
STALE_DAYS = 45


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def frontmatter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    fm, section = {}, None
    for line in m.group(1).splitlines():
        top = re.match(r"(\w[\w-]*):\s*(.*)$", line)
        sub = re.match(r"\s+(\w[\w-]*):\s*(.*)$", line)
        if top:
            section = top.group(1) if not top.group(2) else None
            fm[top.group(1)] = top.group(2).strip().strip("\"'")
        elif sub and section:
            fm[section + "." + sub.group(1)] = sub.group(2).strip().strip("\"'")
    return fm


def prose(text):
    """Text with fenced code blocks removed."""
    return re.sub(r"^```.*?^```", "", text, flags=re.M | re.S)


def check_links(skill, problems):
    real = os.path.realpath(skill)
    for dp, _, fns in os.walk(skill):
        for fn in sorted(f for f in fns if f.endswith(".md")):
            path = os.path.join(dp, fn)
            for target in re.findall(r"\]\(([^)\s]+)", prose(read(path))):
                if re.match(r"[a-z][a-z0-9+.-]*:", target) or target.startswith("#"):
                    continue
                dest = os.path.realpath(os.path.join(dp, target.split("#")[0]))
                rel = os.path.relpath(path, skill)
                if os.path.commonpath([real, dest]) != real:
                    problems.append("%s: link '%s' leaves the skill folder" % (rel, target))
                elif not os.path.isfile(dest):
                    problems.append("%s: link '%s' does not resolve to a file" % (rel, target))


def check_sources(skill, problems):
    refs = os.path.join(skill, "references")
    for fn in sorted(os.listdir(refs)) if os.path.isdir(refs) else []:
        if not re.match(r"[1-7]-.*\.md$", fn):
            continue
        parts = re.split(r"^(?=## )", read(os.path.join(refs, fn)), flags=re.M)
        for part in parts:
            head = part.split("\n", 1)[0]
            if not re.match(r"## \d+\.\d+\b", head):
                continue
            lines = [ln for ln in part.splitlines() if ln.strip()]
            last = lines[-1].strip()
            urls = re.findall(r"https?://([^\s)\]>,;]+)", last)
            if not last.startswith(("Source:", "Sources:")):
                problems.append("references/%s: section '%s' must end with a Source: line" % (fn, head[3:]))
            elif not urls or not all(u.startswith(ALLOWED) for u in urls):
                problems.append("references/%s: section '%s' Source: needs URLs on allowed Google domains" % (fn, head[3:]))


def check_versions(skill, name, fm, problems):
    versions = {"SKILL.md metadata.version": fm.get("metadata.version")}
    for rel in (".claude-plugin/plugin.json", ".codex-plugin/plugin.json", ".claude-plugin/marketplace.json"):
        try:
            data = json.loads(read(os.path.join(ROOT, rel)))
        except (OSError, ValueError) as e:
            problems.append("%s: cannot read (%s)" % (rel, e))
            continue
        if rel.endswith("marketplace.json"):
            data = next((p for p in data.get("plugins", []) if p.get("name") == name), {})
        versions[rel] = data.get("version")
    if len(set(versions.values())) != 1 or None in versions.values():
        problems.append("versions differ or are missing: %s" % ", ".join("%s=%s" % kv for kv in sorted(versions.items())))


def check_deadlines(skill, problems, warnings):
    path = os.path.join(skill, "references", "deadlines.md")
    if not os.path.isfile(path):
        problems.append("references/deadlines.md is missing")
        return
    text, today = read(path), datetime.date.today()
    m = re.search(r"verified_on\W+(\d{4}-\d{2}-\d{2})", text)
    if not m:
        problems.append("references/deadlines.md has no verified_on: YYYY-MM-DD")
    elif (today - datetime.date.fromisoformat(m.group(1))).days > STALE_DAYS:
        warnings.append("deadlines.md verified_on %s is more than %d days old" % (m.group(1), STALE_DAYS))
    for n, line in enumerate(text.splitlines(), 1):
        d = re.search(r"\d{4}-\d{2}-\d{2}", line)
        if d and "upcoming" in line.lower() and datetime.date.fromisoformat(d.group(0)) < today:
            warnings.append("deadlines.md:%d upcoming date %s has passed" % (n, d.group(0)))


def check_skill(skill, problems, warnings):
    name = os.path.basename(skill)
    try:
        text = read(os.path.join(skill, "SKILL.md"))
    except OSError:
        problems.append("%s: SKILL.md is missing" % name)
        return
    fm = frontmatter(text)
    if fm is None:
        problems.append("SKILL.md: frontmatter is missing")
        return
    if fm.get("name") != name:
        problems.append("SKILL.md: name '%s' must equal the folder name '%s'" % (fm.get("name"), name))
    desc = fm.get("description", "")
    if not desc or len(desc) >= 1024 or re.search(r"[<>]", desc):
        problems.append("SKILL.md: description must be non-empty, under 1024 characters, with no angle brackets")
    if len(text.splitlines()) >= 500:
        problems.append("SKILL.md: %d lines, must be under 500" % len(text.splitlines()))
    check_links(skill, problems)
    check_sources(skill, problems)
    check_versions(skill, name, fm, problems)
    check_deadlines(skill, problems, warnings)


def main(argv):
    if set(argv[1:]) - {"--strict"}:
        print(__doc__.strip())
        return 2
    problems, warnings = [], []
    skills = os.path.join(ROOT, "skills")
    for name in sorted(os.listdir(skills)) if os.path.isdir(skills) else []:
        check_skill(os.path.join(skills, name), problems, warnings)
    if not problems and not os.path.isdir(skills):
        problems.append("no skills/ directory")
    if "--strict" in argv:
        problems, warnings = problems + warnings, []
    for w in warnings:
        print("WARN: " + w)
    for p in problems:
        print("FAIL: " + p)
    print("%d failure(s), %d warning(s)" % (len(problems), len(warnings)))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
