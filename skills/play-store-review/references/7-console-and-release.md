---
name: console-and-release
description: Google Play publishing gates, mandatory Console tasks, target API, 16 KB verification, app bundle and sizes, Android vitals, production access, reviewer access, declarations, account type and developer verification, and enforcement states
---

# 7. Console and Release

These gates can block publishing even when the code follows every content policy. Most cannot be seen from code, so ask the user or list them as "could not verify". Dated rules and future deadlines live in `deadlines.md`; this file states a future rule only as `(from YYYY-MM-DD)`.

## Contents

- 7.1 Publishing gate: Errors summary and review states
- 7.2 Mandatory Console tasks before submission
- 7.3 Target API level
- 7.4 Native code: 64-bit and 16 KB
- 7.5 App bundle, sizes, and signing
- 7.6 Technical quality
- 7.7 Production access for new personal accounts
- 7.8 Reviewer access
- 7.9 Declarations
- 7.10 Account type and developer verification
- 7.11 Review time and extended review
- 7.12 Enforcement states
- 7.13 Hostile cases

## 7.1 Publishing gate: Errors summary and review states

- [ ] The release review summary shows no "Errors summary" heading. Errors must be resolved before the release can be published. Warnings and minor issues alone do not block
- [ ] If the status is Update rejected or App rejected, the choice is fix and resubmit, or appeal. Do not resubmit until every violation is fixed
- [ ] Changes sit in "Changes not yet sent for review" until the developer sends them. With managed publishing, an approved update goes live only when the developer publishes it

**Evidence:** App rejected applies only to a draft app being published for the first time. Update rejected applies to updates. Removed by Google needs a policy-compliant update. Suspended by Google needs a successful appeal. Release actions need the right Console permissions (for example "Release to production, exclude devices, and use Play App Signing"), so a user without them cannot ship.

Source: https://support.google.com/googleplay/android-developer/answer/9859751

## 7.2 Mandatory Console tasks before submission

- [ ] App information and metadata are accurate and complete
- [ ] Privacy policy uploaded, and the Data safety section completed
- [ ] An active demo account, login information, and any other resource the reviewer needs (sign-in details, QR code) are provided. Outdated sign-in details are a listed "don't"
- [ ] App package names are registered in Play Console for Android developer verification
- [ ] Developer account details are accurate: legal name and address, D-U-N-S number for organizations, contact email and phone, developer email and phone shown on Google Play where applicable, payment methods where applicable, and a linked Google payment profile
- [ ] Organization accounts: account details match the Dun & Bradstreet profile and are kept up to date

**Evidence:** These are the "before you submit your app" and account items in the Play Console Requirements policy (items 2.1, 2.2, 3.1 to 3.4).

Source: https://support.google.com/googleplay/android-developer/answer/10788890

## 7.3 Target API level

- [ ] New apps and updates meet the target level for their form factor (in force since 2026-08-31): API 36 for everything not listed next, such as phones and tablets; API 35 for Wear OS and Android Automotive OS; API 34 for Android TV and Android XR
- [ ] Existing apps are not stale. To stay available to new users on devices running a newer OS than the app's target, an existing app must target API 35 or higher. Affected: target 34 or lower generally, 33 or lower for Wear OS, TV, and XR, 31 or lower for Automotive OS
- [ ] Extension status is known. An extension to 2026-11-01 could be requested; the page said the Console extension forms would appear "later this year". Ask whether the app has an approved extension, and do not assume it expired or that it still applies
- [ ] `targetSdk` was read from the built artifact or Gradle, not guessed. A framework wrapper (Flutter, Expo, others) is not described on the Google pages: check the generated manifest
- [ ] Exempt only if permanently private: restricted to a specific organization and for internal distribution only

**Evidence:** Policy says new apps and updates that miss the level are prevented from submission in Console. For existing apps, the consequence is limited availability to devices at or below the target level, not removal. The page is dated 2026-10-28.

Source: https://developer.android.com/google/play/requirements/target-sdk

## 7.4 Native code: 64-bit and 16 KB

Apps with native code must support 64-bit and 16 KB memory pages. Java and Kotlin-only apps, including all libraries and SDKs, already support 16 KB; testing is still recommended. Apps count as native if they use NDK or C/C++, link a third-party native library or SDK, or were built by a tool that ships native libraries.

- [ ] Rule: apps targeting API 35+ must support 16 KB pages on 64-bit devices. Updates that do not support it cannot be released `(from 2027-02-01)`
- [ ] Wear OS apps (required since 2026-09-15) and Android TV apps (required since 2026-08-01) with native code already need 64-bit and 16 KB support (technical quality page)
- [ ] Find native code: APK Analyzer lists `.so` files under `lib/`. No `.so` files or no `lib/` folder means no native code
- [ ] Bundle zip alignment: `bundletool dump config --bundle=app-release.aab | grep alignment`. Expected `PAGE_ALIGNMENT_16K`. `PAGE_ALIGNMENT_4K` means the APK built from the bundle has 4 KB aligned `.so` files
- [ ] ELF alignment, Linux or macOS: `check_elf_alignment.sh app.apk` prints `ALIGNED` or `UNALIGNED` for the `arm64-v8a` libraries. Any `UNALIGNED` `arm64-v8a` or `x86_64` library needs repackaging and a rebuild
- [ ] ELF alignment by hand: `llvm-objdump -p lib.so | grep LOAD`. Expected `align 2**14` on every LOAD line. `2**13`, `2**12`, or lower fails
- [ ] Zip alignment of the APK (build-tools 35.0.0 or newer): `zipalign -v -c -P 16 4 app.apk`. Expected last line `Verification successful`. This works on an APK, not an AAB
- [ ] RELRO: `llvm-readelf -Wl lib.so | grep 'RELRO\|Type'`. If a `GNU_RELRO` segment shares a LOAD segment with writable data, `(VirtAddr + MemSiz) % 0x4000` must be 0. If `GNU_RELRO` sits in its own LOAD segment, or there is no RELRO, it is compliant. A misaligned RELRO crashes at runtime with a segmentation fault; libraries built with NDK r27 or lower without the flags are the usual cause
- [ ] Runtime check on a 16 KB device or emulator image: `adb shell getconf PAGE_SIZE` returns `16384`. Then rerun the zipalign check and exercise the app
- [ ] A first-launch compatibility-mode warning on a 16 KB device means the app has 4 KB LOAD alignment or 4 KB zip alignment. It runs, but it is not compliant

**Evidence (toolchain):** AGP 8.5.1 or higher with NDK r28 or higher builds 16 KB compatible by default, if prebuilt dependencies are also compatible. NDK r27 and lower need `-Wl,-z,max-page-size=16384` and `-Wl,-z,common-page-size=16384` (in `Android.mk` via `LOCAL_LDFLAGS`, or CMake `target_link_options`). Prebuilt shared libraries must be recompiled the same way. AGP 8.3 to 8.5 aligns by default but bundletool does not zipalign APKs by default, so an app built from a bundle in Play can fail to install. AGP below 8.5.1 can fall back to compressed libraries (`useLegacyPackaging`) at the cost of disk space. Remove hard-coded 4096 or `PAGE_SIZE` assumptions in code. Check each SDK vendor for a 16 KB compatible version.

Source: https://developer.android.com/guide/practices/page-sizes and https://support.google.com/googleplay/android-developer/answer/17492799

## 7.5 App bundle, sizes, and signing

- [ ] Limits use compressed download size as computed by Play Console on upload. Base module 500 MB; each feature module 500 MB; each asset pack 1.5 GB; total of all modules and install-time asset packs 4 GB; on-demand and fast-follow asset packs 30 GB total; 34 GB total for the app
- [ ] An app over 1 GB must have minSdk API 21 or higher. Feature modules: recommended maximum 100 (50 when minSdk is below 26). At most 100 asset packs per bundle. Over 200 MB, mobile-data users get a non-blocking size dialog
- [ ] New apps must publish as an Android App Bundle (required since August 2021). An app still published as APKs is held to the legacy limit of 100 MB per APK
- [ ] Play App Signing: new apps are enrolled automatically, the upload key is RSA 2048 or larger, and a lost or compromised upload key can be reset through a Console request. A signing key you supply yourself must be RSA 2048 or larger, and the app signing key itself can be changed only before the app reaches open testing or production (a later change is a key upgrade). The Play App Signing page does not call enrollment mandatory

**Evidence:** Sizes are from the size-limit page. The `versionCode` maximum is 2,100,000,000, and Console blocks uploads above it. Signing details are from https://support.google.com/googleplay/android-developer/answer/9842756, and the bundle requirement is from https://developer.android.com/guide/app-bundle.

Source: https://support.google.com/googleplay/android-developer/answer/9859372

## 7.6 Technical quality

Current bad-behavior thresholds. Play generally uses the last 28 days of data and may act sooner on a spike. Exceeding a threshold makes an app likely to be less discoverable, and a warning may be shown on the listing; for a single device model, Play steers users on that model away from the app.

- [ ] User-perceived crash rate under 1.09% of daily users overall, and under 8% on any single phone model (4% per watch model)
- [ ] User-perceived ANR rate under 0.47% overall and under 8% on any single phone model (5% per watch model)
- [ ] Excessive partial wake locks: more than 5% of battery sessions with partial wake locks totalling over 3 hours. This metric is in beta and does not currently reduce discoverability
- [ ] Watch faces: excessive battery usage over 1% of sessions
- [ ] Core value signals: DAU/MAU below 8%, or user loss above 5%, may trigger a listing warning and loss of some surfaces

Upcoming, report as upcoming and never as a violation today:

- **Memory `(from 2027-02)`, phones and tablets:** P90, rolling 28 days, Android 13+ data, for anonymous RSS plus swap by RAM tier and app state, and for bitmap memory. The tier table is on the quality page
- **Code optimization `(from 2027-02)`, all form factors:** apps over 10 MB of DEX and games over 50 MB must reach at least 25% each in obfuscation, optimization, and shrinking. Flag `isMinifyEnabled = false` on release builds above that size
- **Zero-tap sign-in restoration `(from 2027-04)`, phones and tablets:** apps with sign-in must restore sign-in on device switch, primarily with the Restore Credentials API. Games, permanently private apps, and enterprise device management apps are out of scope. Block Store integrations in production on or before 2026-09-30 count as compliant. Regulated apps (financial, healthcare) can request an exemption in Console before enforcement

**Evidence:** The quality page states that these requirements are not optional and that missing them can affect visibility and publishing. Uploaded builds may differ from local builds on CI, so minor differences in optimization percentages can be expected.

Source: https://support.google.com/googleplay/android-developer/answer/17492799

## 7.7 Production access for new personal accounts

Applies to personal accounts created after 2023-11-13.

- [ ] Closed test with at least 12 testers opted in continuously for the 14 days before applying. Internal testing has no requirement; closed testing needs completed app setup; open testing opens only after production access
- [ ] Application filed from the Dashboard (Apply for production). Three sections: about the closed test (how easy recruiting was, whether testers used all features, whether usage matched expected production use, summary of feedback and how it was collected), about the app, and about production readiness (changes made from test learnings, how readiness was judged)
- [ ] A tester who opted in, then out before 14 days, does not count. A tester who opts out and back in must again reach 14 consecutive days
- [ ] Test credentials in the Console are valid so reviewers can reach the features

**Evidence:** Production and Pre-registration stay disabled until the requirement is met. Review usually takes seven days or less, but can take longer. Google can ask you to keep testing, for example with fewer than 12 opted-in testers or insufficient engagement. The page does not say whether the whole test clock resets when the count dips below 12. See `rejection-playbook.md` for field reports.

Source: https://support.google.com/googleplay/android-developer/answer/14151465

## 7.8 Reviewer access

- [ ] If any feature needs sign-in, App access says so and provides working details. A paywall with no sign-in also needs access instructions that let reviewers use the paid content freely
- [ ] Details are reusable, valid at all times and from any location, and kept working without error
- [ ] Two-step or one-time-password flows have reusable credentials that bypass them. An expired password may stop review and cause rejection
- [ ] Details are in English, including any non-English login
- [ ] A QR code, barcode, or other non-alphanumeric credential is supplied as a static URL uploaded to Console
- [ ] If the user sets a password or PIN, clear instructions are given
- [ ] For sign in with Google, Facebook, or similar, full account information and detailed instructions are given
- [ ] A geo-gated login has "master" style credentials valid anywhere

**Evidence:** Saying all functionality is open to review in an app that has a login or paywall is a mismatch to report; that inference is not Google wording. Giving real user credentials is not addressed on the page; treat it as advice, not rule.

Source: https://support.google.com/googleplay/android-developer/answer/15748846

## 7.9 Declarations

Compare what the code does with what the Console says. Check each one that applies:

- [ ] Privacy policy, Data safety, App access, Ads, Content rating (see 5.5), Target audience
- [ ] Health apps declaration: all developers complete it on the App content page, even with no health features (see 1.8)
- [ ] Financial features, News (5.8), and Government apps declarations
- [ ] Advertising ID, permissions, and foreground service declarations, including photo and video, SMS and call log, location, and All Files Access where used
- [ ] Package name registration for Android developer verification (7.2)
- [ ] Trader status: from 2026-11 developers must declare it under new Console requirements. **Scope unverified:** the announcement does not say who is a trader, which regions apply, or what non-traders do, and no Console help page for it was read. Ask the user and read the Console page
- [ ] `(from 2027-08-25)` Local Network permission declaration for apps targeting API 37+, and Manage Contacts declaration for apps targeting API 38+ (scope per the Preview: Permissions and APIs page; the announcement states no API level)
- [ ] `(from 2027-01-27)` ACCESS_FINE_LOCATION declaration justifying why coarse location or the location button is insufficient, for apps targeting API 37+ (scope per the Preview page)
- [ ] Play Age Signals API data used only for legal and regulatory age-appropriate experiences; see the policy section on it

**Evidence:** Declarations in this list marked with a date come from the 2026-10-29 announcement and the Policy Deadlines page. Account deletion and Ads declarations were not verified on a page in this research.

Source: https://support.google.com/googleplay/android-developer/answer/18100766 and https://support.google.com/googleplay/android-developer/answer/16679511

## 7.10 Account type and developer verification

- [ ] Developers providing these services must register as an Organization when creating the account: financial products and services (banking, loans, stock trading, investment funds, cryptocurrency software wallets and exchanges); health apps such as Medical apps and Human Subjects Research apps; apps approved to use the `VpnService` class; and government apps, including apps developed by or on behalf of a government agency
- [ ] Account ownership changes go through the official account transfer process. Unofficial transfer is prohibited, including buying, leasing, or selling accounts obtained through illegitimate means on third-party marketplaces. Moving a single app uses the app owner transfer process
- [ ] Developer verification: protections began 2026-09-30 for installs from participating stores on certified devices (Android 7+) in Brazil, Indonesia, Singapore, and Thailand, and Google says they expand globally in 2027. Play-registered package names count (see 7.2). Organizations need a D-U-N-S number (free, can take up to 28 days) and a website verified through Search Console. Limited-distribution accounts (no identity check) are capped at 20 devices. Sources: https://developer.android.com/developer-verification and https://support.google.com/android-developer-console/answer/16561738

**Evidence:** The org list above keeps the Console requirements page wording. A narrower reading ("only medical and human-subjects health apps are Organization-only") was not confirmed; do not apply it. Whether a general wellness app counts as a health app is not decided by that wording, so check the Health apps page before flagging.

Source: https://support.google.com/googleplay/android-developer/answer/10788890

## 7.11 Review time and extended review

- [ ] The user has planned for extended review. Some developer accounts get a longer review, up to seven days, or longer in exceptional cases, for new and updated apps
- [ ] The user knows no fixed review time is published, so release-day dependencies (marketing, server cutover) have slack
- [ ] Managed publishing is considered when go-live timing matters

**Evidence:** The Publish page gives the seven-day figure and the "longer in exceptional cases" wording, for both new and standard-publishing updates.

Source: https://support.google.com/googleplay/android-developer/answer/9859751

## 7.12 Enforcement states

Outcome summary. Causes, fixes, and appeal routes are in `rejection-playbook.md`.

- Rejection: the new app or update is not made available, the previously published version stays live, and account standing is unaffected
- Removal: the app and all earlier versions come down; a compliant update restores it; multiple removals may become a suspension
- Suspension: like removal, plus a strike; an appeal must succeed to reinstate; multiple strikes can end in termination of individual and related accounts
- Limited visibility, limited regions, a restricted developer account, termination, and dormant-account closure are the other states

**Evidence:** Notices may not list every violation, so check the whole catalog before resubmitting.

Source: https://support.google.com/googleplay/android-developer/answer/9899234

## 7.13 Hostile cases

- [ ] App has a login but the declaration says all functionality is available: mismatch
- [ ] Demo account works only from the developer's country, or needs an SMS code: fails the any-location and bypass rules
- [ ] Demo password rotates or the test server is down during review: review may be impossible and the app can be rejected
- [ ] Native code arrives only through an SDK, game engine, or app builder: it still counts as native for 16 KB
- [ ] A library update re-adds a permission or a 4 KB aligned `.so`: re-run the checks on the final release artifact, not on the previous build
- [ ] Target API read from `build.gradle` but a plugin overrides it at build time: read the built manifest
- [ ] Personal account older than 2023-11-13: the 12-tester rule does not apply by its text; confirm account creation date in Console
- [ ] Testers added and removed during the 14 days, or fewer than 12 on any day: treat the requirement as unmet until continuous opt-in is shown
- [ ] App moved between a personal and an organization account: use the official transfer process; an unofficial route is prohibited
- [ ] Pre-launch crashes on test devices only: they do not affect crash statistics, but still point to a crash a reviewer could hit
- [ ] Form factor added late (Wear OS, TV, XR, Automotive): its own target level, asset, and 64-bit and 16 KB rules start applying
- [ ] Private or enterprise app: exempt from target-API availability limits only if permanently private and restricted to one organization

**Evidence:** Each case follows from the Console, App access, testing, target API, and 16 KB pages cited above.

Source: https://support.google.com/googleplay/android-developer/answer/15748846
