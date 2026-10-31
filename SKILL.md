---
name: play-store-review
description: Use when preparing an Android app for Google Play submission, reviewing Android code (Kotlin, Java, Compose, Flutter, React Native, Expo) for Play policy compliance, investigating a Play rejection, removal, or policy warning, or building payments, permissions, ads, user content, AI, kids, health, or finance features for Play.
license: MIT
metadata:
  author: sunvali
  version: "1.0.0"
---

# Google Play Review Checker

Find what would stop an Android app from reaching or staying on Google Play, across the whole Developer Program Policy and the release gates around it.

**Supports:** Kotlin, Java, Jetpack Compose, Flutter, React Native, and Expo

**Rules verified against Google's pages on:** 2026-10-31, using the Developer Program Policy effective 2026-10-29

## Workflow

1. **Get the date.** Compare today with "Rules verified" above. Then, if you can browse, read [Policy Deadlines](https://support.google.com/googleplay/android-developer/table/12921780) and [target API requirements](https://developer.android.com/google/play/requirements/target-sdk). Live Google pages beat this skill. If you cannot browse, say so in the report.
2. **Establish the facts:**
   - Merged manifest permissions, `targetSdk`, `compileSdk`, AGP, NDK, and native libraries
   - Dependencies and their data use
   - What is sold, and in which countries
   - Whether users create accounts, post content, or receive AI output
   - Target audience and listing text
   - Account type and age: personal or organization, and when it was created
   - Console answers, if available
3. **Load only the rule files that apply.** Always load 2 and 7. Load the others when the facts call for them.
4. **Trace before reporting.** Follow each candidate from entry point to effect. Cite `file:line`.
5. **Write the report** in the format below.

## Rule files

| File | Load when |
|------|-----------|
| [1. Restricted content](rules/1-restricted-content.md) | User content, chat, AI output, health, finance, crypto, gambling, dating, regulated goods |
| [2. Privacy and permissions](rules/2-privacy-and-permissions.md) | Always |
| [3. Security and deception](rules/3-security-and-deception.md) | Dynamic code, updaters, webviews, SDKs, remote flags, claims, AppFunctions |
| [4. Monetization and ads](rules/4-monetization-and-ads.md) | Purchases, subscriptions, external links, ads |
| [5. Listing and functionality](rules/5-listing-and-functionality.md) | Listing text available, rating prompts, webview apps, news apps |
| [6. Families](rules/6-families.md) | Under-13 audience, or child appeal in the listing or art |
| [7. Console and release](rules/7-console-and-release.md) | Always |

## Report format

Use these parts, in this order. Omit a part only if it is empty, except **Could not verify**, which is always present.

1. **Verdict:** one line, `Ready`, `Fixable before submission`, or `Not ready`, plus today's date and the checked commit, or "no commit" outside git.
2. **Blocked at the door:** gates Google enforces automatically, before a human reviews anything. These are target API, production access for new personal accounts, unfinished mandatory Console tasks, and package registration.
3. **Will likely be rejected or removed:** policy findings, most severe first. Severity is `CRITICAL` for data abuse or anything risking the account, `HIGH` for likely rejection, and `MEDIUM` for review risk.
4. **Upcoming deadlines that apply to this app:** each with its date, and what to change. Not rated as violations.
5. **Could not verify:** Console state, runtime behavior, and any facts you lacked. State who can answer each one.
6. **Order of work:** the shortest path to submission.

Each finding has these fields:

```
[SEVERITY] Short title (Confirmed | Verify)
Evidence: file:line, and what the code does
Rule: rules/N-file.md section, and the Google policy name
Fix: the specific change for this codebase
```

`Confirmed` means traced in code, or stated in a file you read. `Verify` means it depends on something you could not see. Merge duplicates: one finding per root cause, listing its other locations.

## Evidence standard

| Situation | Report as |
|-----------|-----------|
| SMS or call log permission in the manifest, app not a default handler | Confirmed: the declaration is the violation |
| Other restricted permission, use traced to a feature | Confirmed |
| Other restricted permission, no use found | Verify, and suggest removing it |
| Non-Play checkout for digital goods, enrollment unknown | Verify, with the per-region answer |
| Non-Play checkout for physical goods | Not a finding |
| Disclosure screen exists | Check the gatekeeper test before passing it |
| Ad timing or moderation process, not visible in code | Could not verify |
| Upcoming rule, date not reached | Upcoming, not a violation |
| Project notes or Console drafts state a fact | Confirmed, citing the file. Check it against the code |
| A referenced class or file is missing from the source | Verify, naming what is missing |
| Code exists, but no call site was found | Verify, unless a file you read states when it runs |

## Key dates

Checked 2026-10-31. Dates are from Google's Policy Deadlines table unless noted.

| Date | Applies to | Requirement |
|------|-----------|-------------|
| In force | Phone and tablet uploads | Target API 36, since 2026-08-31 |
| In force | All apps | Package names registered for developer verification, since 2026-09-30 |
| In force | Anonymous and random chat | Child safety and age-restriction rules, since 2026-08-26 |
| 2026-11-01 | Target API extensions | Last extension date |
| November 2026 | Developers in scope | Trader status declaration starts (2026-10-29 announcement) |
| 2026-12-01 | Selling into or out of Japan | Payments authorization, or payments are held (2026-10-29 announcement) |
| 2027-01-27 | Location | Location button mandatory on API 37+ for one-time or infrequent requests |
| 2027-01-27 | Contacts | Use the Contact Picker unless broad access is needed |
| 2027-01-27 | `READ_CALL_LOG` | Phone-call verification ends |
| 2027-01-27 | Foreground services | Geofencing no longer an approved use |
| 2027-01-27 | Subscriptions | Eligibility-based discount disclosures |
| 2027-02-01 | Native code on API 35+ | 16 KB page size, or updates are blocked (Android developer docs) |
| 2027-02-01 | External content links | Report downloads and pay fees (US policy update) |
| February 2027 | Quality | Memory and code optimization thresholds (technical quality page) |
| 2027-04-14 | AppFunctions | Policy compliance rules |
| April 2027 | Apps with sign-in | Zero-tap sign-in restoration (technical quality page) |
| 2027-08-25 | Local network, manage contacts | Restricted, with declarations |

## Common false positives

- Stripe or any other checkout for physical goods
- A US app enrolled in alternative billing or external content links
- Firebase Analytics or any SDK by itself, without checking what it collects
- `SCHEDULE_EXACT_ALARM`, which is not the restricted permission
- Feature flags and staged rollouts that do not hide functionality from review
- Root or emulator detection
- `isMinifyEnabled = false`, which is an upcoming concern above 10 MB of DEX, not a violation today
- Java or Kotlin-only apps, which already support 16 KB

## Relationship to Google's skill

Google publishes [`play-policy-insights`](https://github.com/android/skills/tree/main/play/play-policy-insights), an automated scanner for data safety, demo credentials, and restricted permissions. If it is installed and the user wants deep data-flow evidence, run it and fold its findings into this report. This skill covers the wider policy, release gates, deadlines, and the go or no-go call.

## Reporting skill issues

If this skill failed the user, for example a false positive, a miss, an outdated rule, a bad fix, or a wrong citation, offer once per session to draft an issue.

1. Ask first. If the user declines, drop it.
2. Show the exact title and body before sending.
3. Never include the user's code, app name, package name, file paths, or credentials.
4. Send only after approval, with `gh issue create --repo sunvali/play-store-review-skill --title "[Feedback] <category>: <description>" --body "..."`. Without `gh`, give the user https://github.com/sunvali/play-store-review-skill/issues/new?template=skill-feedback.yml
5. Never send anything silently or automatically.

Include the skill version, category, rule section, what the skill did, what should have happened, and today's date.

## References

- [Developer Program Policy](https://support.google.com/googleplay/android-developer/answer/18258653)
- [Policy Deadlines](https://support.google.com/googleplay/android-developer/table/12921780)
- [Announcements](https://support.google.com/googleplay/android-developer/announcements/13412212)
- [October 29, 2026 announcement](https://support.google.com/googleplay/android-developer/answer/18100766)
- [July 15, 2026 announcement](https://support.google.com/googleplay/android-developer/answer/17134731)
- [Target API requirements](https://developer.android.com/google/play/requirements/target-sdk)
- [16 KB page sizes](https://developer.android.com/guide/practices/page-sizes)
- [Technical quality requirements](https://support.google.com/googleplay/android-developer/answer/17492799)
- [Data safety form](https://support.google.com/googleplay/android-developer/answer/10787469)
- [Account deletion](https://support.google.com/googleplay/android-developer/answer/13327111)
- [Testing requirements for new personal accounts](https://support.google.com/googleplay/android-developer/answer/14151465)
- [Sign-in details for review](https://support.google.com/googleplay/android-developer/answer/15748846)
- [Play Console requirements](https://support.google.com/googleplay/android-developer/answer/10788890)
- [US payments update](https://support.google.com/googleplay/android-developer/answer/15582165)
