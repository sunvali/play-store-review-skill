---
name: security-and-deception
description: Google Play device and network abuse, deceptive behavior, misrepresentation, impersonation, SDKs, malware, unwanted software, and AppFunctions
---

# 3. Security and Deception

## 3.1 Device and network abuse

- [ ] No self-update outside Google Play. Use Play In-App Updates
- [ ] No executable code downloaded from outside Play: flag `DexClassLoader` or `dlopen` on downloaded files, and APK downloads
- [ ] Interpreted code in a VM or webview is allowed, but it must not enable policy violations. This includes React Native over-the-air bundles and Flutter code push
- [ ] No webview JavaScript interface loading untrusted content
- [ ] No known exploitable vulnerabilities. Flag secrets in the client, and resolve Play Console security warnings
- [ ] No interfering with other apps, blocking their ads, or bypassing power management, sandboxes, or `FLAG_SECURE`
- [ ] On-device containers honor `REQUIRE_SECURE_ENV`

## 3.2 AppFunctions

Apps exposing the AppFunctions API follow all existing policies, and must not deceive or manipulate AI agents, bypass security controls, or interfere with other apps. Policy Deadlines lists this for 2027-04-14.

## 3.3 Deceptive behavior

- [ ] Title, icon, screenshots, and description match real functionality
- [ ] No impossible claims, and no unverifiable claims such as "clinically proven"
- [ ] Correct category, and no false government or official-app claims
- [ ] No device settings changes outside the app without consent
- [ ] No generators for IDs, passports, diplomas, credit cards, or bank accounts
- [ ] Extra resources are downloaded only when needed, with size disclosed first
- [ ] "Prank" or "entertainment" labels do not exempt an app
- [ ] Manipulated media that could cause harm is not allowed. Satire and clearly artificial content are excepted
- [ ] **No hidden, dormant, or undocumented features, and no review evasion.** Trace remote flags that switch behavior on after approval, and any branch on reviewer IP, emulator, or device
- [ ] No manipulating the review process
- [ ] No mimicking OS or other app warnings

Do not flag ordinary feature flags, staged rollouts, or A/B tests unless they conceal functionality from review. Do not flag root or emulator detection without evidence of review evasion.

## 3.4 Misrepresentation and impersonation

- [ ] No hiding ownership or primary purpose
- [ ] No implying a relationship with a company, developer, or app that does not exist
- [ ] No misleading names or icons, and no "official" claims without rights
- [ ] Android references follow the Android Brand Guidelines

## 3.5 SDKs

You are responsible for every SDK in the app.

- [ ] Each SDK is compliant, current, and declared in Data safety. Check the Google Play SDK Index for outdated or non-compliant versions
- [ ] No SDK sells personal or sensitive data
- [ ] Prominent disclosure covers unexpected SDK data use
- [ ] Evidence of default SDK collection can be produced within 2 weeks of a request
- [ ] Child-directed apps use only self-certified SDKs (see [Families](6-families.md))
- [ ] SDK foreground services have a valid use case

## 3.6 Malware and unwanted software

- [ ] No backdoors, billing fraud, spyware, ransomware, phishing, rooting, or trojans. These rules apply to SDKs too
- [ ] Monitoring apps use the `IsMonitoringTool` flag, a persistent notification, a clear icon, and listing disclosure
- [ ] The app delivers everything it promises, and explains system changes
- [ ] No false device security claims
- [ ] No asking or rewarding users to turn off Google Play Protect
