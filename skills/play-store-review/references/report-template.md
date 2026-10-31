# Report template

Use these headings, in this order. Omit a section only if it has nothing in it, except **Verdict** and **Could not verify**, which are always present. `scripts/validate_report.py` checks this.

- **Verdict:** one line with `Ready`, `Fixable before submission`, or `Not ready`, then today's date and the checked commit, or "no commit" outside git. `Ready` needs an empty "Blocked at the door" and "Will likely be rejected or removed".
- **Blocked at the door:** gates Google enforces automatically, before a human reviews anything, such as target API, production access for new personal accounts, unfinished mandatory Console tasks, and app registration.
- **Will likely be rejected or removed:** policy findings, most severe first.
- **Upcoming deadlines:** only those that apply to this app, each with its date and what to change. Never rated as violations.
- **Could not verify:** Console state, runtime behavior, and missing facts, each saying who can answer it. Include the scanner's `unknown` items.
- **Order of work:** the shortest path to submission, numbered.

## Findings

```
[SEVERITY] Short title (Confirmed | Verify)
Evidence: file:line, and what the code does
Rule: references/N-file.md section, and the Google policy name
Fix: the specific change for this codebase
```

| Severity | Meaning |
|----------|---------|
| `CRITICAL` | Data abuse, or anything that puts the app's removal or the developer account at risk |
| `HIGH` | Likely rejection |
| `MEDIUM` | Review risk |

`Confirmed` means traced in code, or stated in a file you read. `Verify` means it depends on something you could not see. Write one finding per root cause, and list its other locations under Evidence.

## Example

```markdown
## Verdict

Not ready. 2026-11-03, commit a1b2c3d.

## Blocked at the door

[HIGH] Target API is below the current requirement (Confirmed)
Evidence: app/build.gradle.kts:14 sets targetSdk = 35. This phone app is below the level in deadlines.md.
Rule: references/7-console-and-release.md 7.3, Target API level
Fix: Set targetSdk to the required level and retest edge-to-edge screens.

## Will likely be rejected or removed

[CRITICAL] Location is collected before consent (Confirmed)
Evidence: AnalyticsInit.kt:22 calls getLastLocation() in Application.onCreate. The consent screen, ConsentActivity.kt:40, runs later.
Rule: references/2-privacy-and-permissions.md 2.2, Prominent Disclosure and Consent
Fix: Move the location call behind the accept action in ConsentActivity.

[HIGH] Photo permission for a one-off avatar picker (Confirmed)
Evidence: The merged manifest has READ_MEDIA_IMAGES from com.example:imagepicker:2.1. Its only use is AvatarPicker.kt:18.
Rule: references/2-privacy-and-permissions.md 2.6, Restricted permissions
Fix: Use the Android Photo Picker, then add tools:node="remove" for the permission.

## Upcoming deadlines

- 2027-02-01: libfoo.so in arm64-v8a is 4 KB aligned, and this app targets API 35 or higher. Rebuild it for 16 KB before the date, or updates cannot be released.

## Could not verify

- Data safety answers: the developer can export them from the Console.
- Whether production access is granted: the account owner can confirm from the Dashboard.
- Merged manifest for the free flavor: run a release build, then rescan with --artifact.

## Order of work

1. Raise targetSdk.
2. Fix the consent order.
3. Replace the photo permission and update Data safety.
4. Rescan the release artifact, then submit.
```
