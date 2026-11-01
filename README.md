# Google Play Review Skill

An agent skill that audits Android apps against the Google Play Developer Program Policy and Play Console release gates, then reports what would block, reject, or remove the app, with file and line evidence and a go or no-go verdict.

**Supports:** Kotlin, Java, Jetpack Compose, Flutter, React Native, and Expo

**Policy checked:** the Developer Program Policy effective October 29, 2026. See [deadlines.md](skills/play-store-review/references/deadlines.md) for the date of the last check.

## Installation

The skill is one self-contained folder that follows the [Agent Skills](https://agentskills.io) format, so most agents can load it with no changes.

### Claude Code

Inside Claude Code:

```text
/plugin marketplace add sunvali/play-store-review-skill
/plugin install play-store-review@play-store-review
```

Or from a shell:

```bash
claude plugin marketplace add sunvali/play-store-review-skill
```

```bash
claude plugin install play-store-review@play-store-review
```

### Codex

```bash
codex plugin marketplace add sunvali/play-store-review-skill
```

```bash
codex plugin add play-store-review@play-store-review
```

### GitHub Copilot

Needs `gh` 2.90 or newer:

```bash
gh skill install sunvali/play-store-review-skill play-store-review --agent github-copilot --scope user
```

### Gemini CLI

```bash
gemini skills install https://github.com/sunvali/play-store-review-skill --path skills/play-store-review --scope user --consent
```

### Most other agents

[`npx skills`](https://github.com/vercel-labs/skills) installs for many agents. Choose yours with `-a`. Add `-g` for your user account, or leave it out to install into the current project:

```bash
npx skills add sunvali/play-store-review-skill -g -a cursor
```

### By hand

Copy `skills/play-store-review` into your agent's skills folder:

| Agent | User folder |
|-------|-------------|
| Cursor, OpenCode, Roo Code, Kilo Code, Goose, Zed, Warp, Junie, Qwen Code, Windsurf | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cline | `~/.cline/skills/` |
| Kiro | `~/.kiro/skills/` |
| Amp | `~/.config/agents/skills/` |

Python 3 is optional. Without it, the agent gathers the same facts by hand.

Tested installs: Claude Code, Codex, `gh skill`, `npx skills`, and copying the folder. The other routes follow each agent's documentation and have not been tested here.

## Usage

```text
Is this app ready for Google Play?
Google rejected my app, here is the notice. What do I do?
Check my subscription flow against Play billing rules
We got a policy warning about permissions. What needs to change?
```

A full review has this shape:

1. **Verdict:** `Ready`, `Fixable before submission`, or `Not ready`
2. **Blocked at the door:** automatic gates such as target API and closed testing
3. **Will likely be rejected or removed:** evidenced findings, labeled `Confirmed` or `Verify`
4. **Upcoming deadlines** that apply to this app, never rated as violations
5. **Could not verify:** Console state and anything else code cannot show
6. **Order of work**

## What is in it

| Part | Purpose |
|------|---------|
| [Restricted content](skills/play-store-review/references/1-restricted-content.md) | Child safety, age restrictions, finance, gambling, UGC, AI content, health, blockchain, IP |
| [Privacy and permissions](skills/play-store-review/references/2-privacy-and-permissions.md) | User data, disclosure, Data safety, privacy policy, account deletion, restricted permissions, foreground services |
| [Security and deception](skills/play-store-review/references/3-security-and-deception.md) | Device abuse, dynamic code, deceptive behavior, impersonation, SDKs, malware, AppFunctions |
| [Monetization and ads](skills/play-store-review/references/4-monetization-and-ads.md) | Play Billing, regional programs, subscriptions, ads |
| [Listing and functionality](skills/play-store-review/references/5-listing-and-functionality.md) | Metadata, store assets, ratings, spam, minimum and broken functionality |
| [Families](skills/play-store-review/references/6-families.md) | Target audience, child-directed data, ads, and social features |
| [Console and release](skills/play-store-review/references/7-console-and-release.md) | Target API, 16 KB, quality thresholds, production access, reviewer access, declarations, enforcement |
| [Deadlines](skills/play-store-review/references/deadlines.md) | Every dated requirement, in one table |
| [Rejection playbook](skills/play-store-review/references/rejection-playbook.md) | Notice wording mapped to cause and fix, each with an evidence level |
| [`scan_android.py`](skills/play-store-review/scripts/scan_android.py) | Read-only scanner that collects project facts without running any project code |
| [`validate_report.py`](skills/play-store-review/scripts/validate_report.py) | Checks that a finished report has the required parts |

Every rule section links to the Google page it came from. Items that sources could not settle are marked `Verify`, and reports from developers are labeled as field reports, not policy.

## How it differs from Google's skill

Google's [`play-policy-insights`](https://github.com/android/skills/tree/main/play/play-policy-insights) traces data flows for data safety, demo credentials, and restricted permissions in depth. Use it for that evidence.

This skill covers the wider policy and release process, and makes the go or no-go call. It also reads what Google's scanner leaves out, such as merged manifests, native library alignment, billing and ad SDKs, and Flutter and Expo config. The two work well together.

## Keeping it current

Google changes these rules several times a year, so treat every date here as a snapshot. The skill tells the agent to check Google's live pages first, and the live page wins. A weekly CI job flags deadlines that have passed.

This skill is not legal advice and does not guarantee approval.

**This skill collects no telemetry.** The bundled scripts never use the network and never run your project's code. Your agent may read Google's public pages, and it files feedback issues only after you approve the exact text.

## Development

```bash
python3 -B -m unittest discover -s tests
```

```bash
python3 -B scripts/ci/validate_skill.py
```

[`evals/`](evals) holds test cases in the format `claude plugin eval` reads. They are real, billed model runs, so they are not part of CI:

```bash
claude plugin eval . --allow-tools Write,Bash --scaffold
```

## Privacy

This project has no server and collects no data. Neither the skill nor its authors receive your code, your reports, or anything about you.

- **What it reads:** the agent reads your Android project to run the review, and the bundled scanner reads the project's files on your machine. Secrets the scanner finds are reported by file and kind, with at most the first 4 characters of a match.
- **What it runs:** two local Python scripts, `scan_android.py` and `validate_report.py`. They make no network calls and run no project code. If `aapt2` is installed, the scanner uses it to read a binary manifest in an artifact you pass with `--artifact`.
- **What it writes:** the scan results and the report, only to paths your agent chooses on your machine. It keeps nothing else.
- **What it fetches:** if your agent can browse, it reads Google's public policy pages. That sends no project data.
- **Your agent:** the agent and model you use see what they read from your project, under that provider's own terms. Check those terms before reviewing confidential code.

## Feedback

Found a false positive, a miss, or an outdated rule? [File a feedback issue](https://github.com/sunvali/play-store-review-skill/issues/new?template=skill-feedback.yml). Please leave out app names and proprietary code.

## Credits

Packaging was first adapted from [safaiyeh/app-store-review-skill](https://github.com/safaiyeh/app-store-review-skill) (MIT). This project is not affiliated with or endorsed by Google.

## License

MIT
