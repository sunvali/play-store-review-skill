---
name: console-and-release
description: Google Play target API, 16 KB, Android vitals, quality thresholds, closed testing, reviewer access, declarations, account type, and enforcement
---

# 7. Console and Release

These gates can block publishing even when the code follows every content policy. Many cannot be seen from code, so ask or list them as "could not verify".

## 7.1 Target API level

Uploads since 2026-08-31 must meet:

| Form factor | New apps and updates |
|-------------|----------------------|
| Phones, tablets, foldables | API 36 |
| Wear OS, Android Automotive OS | API 35 |
| Android TV, Android XR | API 34 |

- Extensions run to **2026-11-01** only. Treat them as expired for planning
- Existing phone apps must target API 35 or higher to stay available to new users on newer Android versions
- Permanently private apps are exempt
- Read `targetSdk` from the Gradle file or version catalog. For Flutter check `flutter.targetSdkVersion`, and for Expo check the SDK version and `expo-build-properties`

## 7.2 Native code: 64-bit and 16 KB

Apps with native code must support 64-bit and 16 KB pages. Java and Kotlin-only apps comply by default.

- Updates that do not support 16 KB cannot be released from **2027-02-01** (Android developer docs)
- Wear OS and TV requirements are already in force (2026-09-15 and 2026-08-01)

**Check:** look for `.so` files in `jniLibs/`, and in native dependencies. Ship with AGP 8.5.1+ and NDK r28+, and rebuild prebuilt libraries. To verify a built artifact:

```bash
bundletool dump config --bundle=app-release.aab | grep alignment
zipalign -v -c -P 16 4 app-release.apk
```

## 7.3 Technical quality

Exceeding these can reduce visibility. Play uses 28-day vitals data.

| Metric | Overall | Per phone model |
|--------|---------|-----------------|
| User-perceived crash rate | 1.09% | 8% |
| User-perceived ANR rate | 0.47% | 8% |
| Excessive partial wake locks | 5% | |

**Upcoming**

- **From February 2027, memory (phones and tablets):** P90 thresholds for Anonymous RSS plus Swap, by RAM tier, and for bitmap memory. See [the requirements page](https://support.google.com/googleplay/android-developer/answer/17492799) for the table
- **From February 2027, code optimization (all form factors):** apps with over 10 MB of DEX, and games with over 50 MB, must reach at least 25% obfuscation, optimization, and shrinking. Flag `isMinifyEnabled = false` on release builds
- **From April 2027, zero-tap sign-in restoration (phones and tablets):** apps with sign-in support device-to-device or cloud restore, primarily through the Restore Credentials API. Games are out of scope, and private, enterprise, and existing Block Store integrations have exceptions

Do not call these violations today. Report them as upcoming.

## 7.4 Production access for new personal accounts

For personal developer accounts created after 2023-11-13:

- [ ] Closed test with at least **12 testers** opted in continuously for **14 days**
- [ ] Production access applied for from the Dashboard

Production and pre-registration stay disabled until this is met. Google typically takes up to seven days to review the application.

## 7.5 Reviewer access

- [ ] If any feature needs sign-in, App access says so and gives working test credentials. Never give real user credentials
- [ ] Credentials are reusable and valid from any location for the whole review, and written in English
- [ ] One-time-code or multi-factor flows have a bypass account or instructions
- [ ] Paywalled features have a reviewer route

Saying "all functionality is available" in an app with a login is a mismatch to report.

## 7.6 Console declarations

Compare what the code does with what the Console says. Check each one that applies:

- Privacy policy, Data safety, App access, Ads, Content rating, Target audience
- Health apps, Financial features, News, and Government apps declarations
- Advertising ID, permissions, and foreground service declarations
- Package name registration for Android developer verification (required since 2026-09-30)
- Trader status, starting November 2026. Confirm scope in the Console

## 7.7 Account type

Must publish from an **Organization** account: financial services, medical and human-subjects-research health apps, approved `VpnService` apps, and government apps. Check the linked category pages before flagging general wellness or tracking apps, since their scope is narrower than "any health app".

## 7.8 Enforcement

Rejection keeps the prior version live. Removal takes the app down. Suspension adds a strike. Limited visibility, limited regions, a restricted account, and termination are the other outcomes. Appeal through the link in the enforcement email.
