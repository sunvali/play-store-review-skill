# Google Play Review Skill

An agent skill that checks Android apps against Google Play policies and release requirements, then reports what would block, reject, or remove the app.

**Supports:** Kotlin, Java, Jetpack Compose, Flutter, React Native, and Expo

**Rules verified:** October 31, 2026, against the Developer Program Policy effective October 29, 2026

## Installation

### Claude Code

```bash
/plugin marketplace add sunvali/play-store-review-skill
/plugin install play-store-review@play-store-review
```

### Codex

```bash
codex plugin marketplace add sunvali/play-store-review-skill
```

Then run `/plugins`, choose the Play Store Review marketplace, and install `play-store-review`.

### skills.sh

```bash
npx skills add sunvali/play-store-review-skill
```

## Usage

```text
Review this app for Google Play compliance
Why might Play reject this build?
Check my subscription flow against Play billing rules
We got a policy warning about permissions. What needs to change?
```

The report separates:

1. **Blocked at the door:** automatic gates such as target API and closed testing
2. **Will likely be rejected or removed:** evidenced policy findings
3. **Upcoming deadlines** that apply to this app
4. **Could not verify:** Console state and anything else code cannot show
5. **Order of work**

## Coverage

| Rule file | Covers |
|-----------|--------|
| [Restricted content](rules/1-restricted-content.md) | Child safety, age restrictions, finance, gambling, UGC, AI content, health, blockchain, IP |
| [Privacy and permissions](rules/2-privacy-and-permissions.md) | User data, disclosure, Data safety, privacy policy, account deletion, restricted permissions, foreground services |
| [Security and deception](rules/3-security-and-deception.md) | Device abuse, dynamic code, deceptive behavior, impersonation, SDKs, malware, AppFunctions |
| [Monetization and ads](rules/4-monetization-and-ads.md) | Play billing, regional programs, subscriptions, loot boxes, ads |
| [Listing and functionality](rules/5-listing-and-functionality.md) | Metadata, ratings, content ratings, spam, minimum and broken functionality |
| [Families](rules/6-families.md) | Target audience, child-directed data and ads |
| [Console and release](rules/7-console-and-release.md) | Target API, 16 KB, vitals, quality thresholds, closed testing, reviewer access, declarations, account type |

## How it differs from Google's skill

Google's [`play-policy-insights`](https://github.com/android/skills/tree/main/play/play-policy-insights) is an automated scanner for data safety, demo credentials, and restricted permissions. Use it for deep data-flow evidence.

This skill is a lighter, instructions-only review of the wider policy and release process: payments by region, ads, listings, families, UGC, AI content, health, finance, quality thresholds, closed testing, and dated deadlines. The two work well together.

## Keeping it current

Google changes these rules several times a year, so treat every date here as a snapshot. The skill tells the agent to check Google's live Policy Deadlines page first, and the live page wins.

This skill is not legal advice and does not guarantee approval.

**This skill collects no telemetry and makes no network calls of its own.** It can ask your agent to read Google's public pages. It only files feedback issues after you approve the exact text.

## Feedback

Found a false positive, a miss, or an outdated rule? [File a feedback issue](https://github.com/sunvali/play-store-review-skill/issues/new?template=skill-feedback.yml). Please leave out app names and proprietary code.

## Credits

Structure and packaging are adapted from [safaiyeh/app-store-review-skill](https://github.com/safaiyeh/app-store-review-skill) (MIT). This project is not affiliated with or endorsed by Google.

## License

MIT
