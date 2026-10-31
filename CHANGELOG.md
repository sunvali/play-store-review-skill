# Changelog

## 2.1.0 - 2026-10-31

Tested on eight open-source Android apps, and fixed what they exposed.

### Fixed

- The scanner now finds SDK levels in shared build scripts, convention plugins, Kotlin constants, Gradle properties, AGP 9 `release()` blocks, and Expo `expo-build-properties`
- It follows version catalog bundles and `add(config, libs.x)`, which hid Play-only SDKs
- NDK versions resolve from catalogs, and dangling symlinks no longer count as errors
- Output stays smaller on large multi-module projects

### Added

- `sdk.app`, the values for the installed app, with the scope they came from
- `module`, `source_set`, and `removed_in` on permissions, so flavor-only and demo permissions are not mistaken for the Play build
- Evidence rules for those cases, and for apps already live on Play

## 2.0.0 - 2026-10-31

Checked against the Developer Program Policy effective 2026-10-29, using the raw text of Google's pages.

### Changed

- Moved the whole skill into `skills/play-store-review/`, so it works when only that folder is installed. Rule files moved from `rules/` to `references/`.
- Rewrote every rule file from Google's page text. Each section now links to its source.
- Moved all dated facts into `references/deadlines.md`.
- Added separate paths for a full review, a notice diagnosis, and a single feature question.

### Added

- `scripts/scan_android.py`, a read-only scanner for project facts
- `scripts/validate_report.py`, a report format check
- `references/rejection-playbook.md`, with evidence levels on each row
- `references/report-template.md`, with a worked example
- Evals, unit tests, and CI

### Removed

- `metadata.json`

## 1.0.0 - 2026-10-31

First release.
