---
name: security-and-deception
description: Google Play device and network abuse, deceptive behavior, misrepresentation, impersonation, SDKs, malware, mobile unwanted software, and AppFunctions
---

# 3. Security and Deception

Items marked `Verify` are interpretation or come from pages not checked here, not policy text. Confirm before reporting.

## Contents

- 3.1 Device and network abuse
- 3.2 AppFunctions (from 2027-04-14)
- 3.3 Deceptive behavior
- 3.4 Misrepresentation, impersonation, and target API
- 3.5 SDKs
- 3.6 Malware and mobile unwanted software
- 3.7 FLAG_SECURE, on-device containers, and full-screen intent

## 3.1 Device and network abuse

Applies to the app and to any SDK it includes. Foreground services, user-initiated data transfer jobs, `VpnService`, and exact alarms are in [Privacy and permissions](2-privacy-and-permissions.md#27-foreground-services).

- [ ] No interfering with, disrupting, damaging, or accessing without authorization the device, other devices, servers, networks, APIs, or services, including other apps, Google services, or a carrier network
- [ ] Follows the default Android system optimization requirements in the Core App Quality guidelines
- [ ] The app does not modify, replace, or update itself by any means other than Google Play's update mechanism. SDK self-update code counts
- [ ] No executable code (dex, JAR, `.so`) downloaded from outside Google Play, by the app or an SDK
- [ ] Code in a virtual machine or interpreter that gives only indirect access to Android APIs (such as JavaScript in a webview or browser) is exempt
- [ ] Interpreted code (JavaScript, Python, Lua) loaded at run time and not packaged with the app does not allow potential policy violations. Applies to SDKs
- [ ] No webview with an added JavaScript interface that loads untrusted web content (for example an `http://` URL) or unverified URLs from untrusted sources (for example URLs from untrusted Intents)
- [ ] No code that introduces or exploits security vulnerabilities. Check flags from the App Security Improvement Program. An SDK that downloads files over an insecure connection is an example
- [ ] No blocking or interfering with another app's ads
- [ ] No game cheating that affects other apps' gameplay
- [ ] No hacking or circumvention instructions or tools for services, software, or hardware
- [ ] No use of a service or API that breaks its terms of service
- [ ] Apps not eligible for allowlisting do not try to bypass system power management
- [ ] Proxy services for third parties only where that is the primary, user-facing core purpose of the app
- [ ] No installing other apps without the user's prior consent, and no linking to or facilitating malicious software
- [ ] No circumventing Android sandbox protections to learn user activity or identity from other apps
- [ ] No full-screen intent used to force interaction with disruptive ads or notifications

**Evidence:** search for `DexClassLoader`, `PathClassLoader`, `System.load`, `dlopen`, and `Runtime.exec` fed by downloaded files (these are detection hints, not policy text). Check `addJavascriptInterface` against the URLs loaded in that webview. Check for `REQUEST_INSTALL_PACKAGES` and install flows, `PackageInstaller` use, and self-update logic. Flag hot-update or over-the-air code delivery for interpreted code (React Native bundles, Flutter code push) as `Verify`: it is allowed only if it cannot enable policy violations. Policy does not name these frameworks.

**Violations Google lists:** an app or SDK that downloads dex or native code from outside Google Play; a JavaScript-interface webview loading `http://` or Intent-supplied URLs; installing apps without consent; an SDK with self-update code; proxy services that are not the core purpose.

Source: https://support.google.com/googleplay/android-developer/answer/16559646

## 3.2 AppFunctions (from 2027-04-14)

Applies to apps that expose functions through the AppFunctions API. Not a current violation before 2027-04-14. Policy Deadlines and the announcement dated 2026-10-29 carry the rule.

- [ ] The app follows all existing Google Play policies for its AppFunctions
- [ ] No deceiving or manipulating AI agents
- [ ] No bypassing security controls
- [ ] No interfering with other applications

Detail from the Preview: Permissions and APIs page: function names, parameters, and descriptions match runtime behavior; no hidden system instructions or prompts returned dynamically in runtime responses (instructions for agents are declared at registration); no dictating execution rules for other apps' AppFunctions; no coaxing agents to reveal system instructions or user data; no interfering with an agent's ability to pick or call other apps; schemas limited to what the tool needs; data collected through AppFunctions covered in Data safety and the User Data policy.

**Evidence:** AppFunctions declarations and their descriptions, and whether runtime responses carry instruction-like text aimed at an agent.

Source: https://support.google.com/googleplay/android-developer/answer/16909972

## 3.3 Deceptive behavior

Policy has five parts: misleading claims, deceptive device settings changes, enabling dishonest behavior, manipulated media, and behavior transparency.

**Misleading claims**

- [ ] Title, icon, screenshots, description, and all other metadata describe the real functionality accurately
- [ ] No functionally impossible claims, even as a prank, fake, or joke (an insect repellent app, a phone breathalyzer)
- [ ] Rating and category are correct
- [ ] No false or deceptive content that could interfere with voting or election outcomes
- [ ] No false claim of affiliation with a government entity, or of providing government services without authorization
- [ ] No "official app" claim, or titles such as "[Celebrity] Official", without the rights

**Device settings changes**

- [ ] No change to device settings or features outside the app without the user's knowledge and consent. This covers system and browser settings, bookmarks, shortcuts, icons, widgets, and homescreen presentation
- [ ] Consented changes are easily reversible
- [ ] No settings changes as a service to third parties or for advertising
- [ ] No misleading users into removing or disabling third-party apps or changing settings or features. No encouraging or incentivizing it either, unless it is part of a verifiable security service

**Enabling dishonest behavior**

- [ ] No generators for ID cards, social security numbers, passports, diplomas, credit cards, bank accounts, or driver's licenses
- [ ] Extra resources (such as game assets) are downloaded only if necessary. Prompt the user and disclose the download size first. Applies to CDN downloads
- [ ] A "prank" or "for entertainment" label does not exempt an app
- [ ] No mimicking apps or sites to get personal or authentication information
- [ ] No unverified or real phone numbers, contacts, addresses, or personal information of non-consenting people
- [ ] Core functionality that differs by geography, device parameters, or other user data is prominently advertised in the listing
- [ ] Significant changes between versions are disclosed in what's new and in the listing

**Manipulated media**

- [ ] No promoting or creating demonstrably false or misleading imagery, audio, video, or text that may cause harm about a sensitive event, politics, social issues, or public concern
- [ ] Exceptions: public interest, clearly artificial images, media with user-facing disclaimers or watermarks, obvious satire or parody
- [ ] The listing does not use public figures or sensitive-event media to advertise media-altering features

**Behavior transparency**

- [ ] **No hidden, dormant, or undocumented features, and no review evasion.** Trace remote flags that switch behavior on after approval, and any branch on reviewer IP, emulator, or device
- [ ] No manipulating or modifying behavior during review, and no misleading reviewers about purpose or function (clarified 2026-10-29, enforcement standard unchanged)
- [ ] No mimicking OS or other app functionality or warnings

Do not flag ordinary feature flags, staged rollouts, or A/B tests unless they conceal functionality from review. Do not flag root or emulator detection without evidence of review evasion.

**Evidence:** compare the listing to the real UI; read remote config and feature flag defaults; check how geography or device checks change core features; check the manifest for settings-writing permissions such as `WRITE_SETTINGS`; confirm a size prompt before large downloads.

**Violations Google lists:** a racing game listing for a block puzzle game; an antivirus app that is only a removal guide; breathalyzer or insect-repellent apps; wrong rating or category; election falsehoods; false government affiliation; "Official" celebrity titles; apps that mimic others to steal credentials; unadvertised geography-based core differences; silent major version changes; changing behavior in review; CDN downloads with no size prompt; news-broadcast mimics with real outlet logos and no watermark.

Source: https://support.google.com/googleplay/android-developer/answer/17006354

## 3.4 Misrepresentation, impersonation, and target API

**Misrepresentation** applies to apps and developer accounts.

- [ ] No impersonating a person or organization, and no hiding or misrepresenting ownership or primary purpose
- [ ] No coordinated activity to mislead users, including hiding or misrepresenting country of origin while directing content at users in another country
- [ ] No coordination with other apps, sites, developers, or accounts to hide developer or app identity or other material details where content relates to politics, social issues, or public concern

**Impersonation**

- [ ] The app does not imply a relationship to, or authorization by, another company, developer, entity, organization, or app that the developer does not actually have
- [ ] Icons, titles, descriptions, and in-app elements do not mislead about the app's relationship to someone else
- [ ] Developer name does not suggest a relationship to Google or another company without one
- [ ] No national emblems that suggest government ties, and no copied business or website logos
- [ ] Titles and icons are not so close to existing products that users may be misled
- [ ] No "official" claims, such as "[Celebrity] Official", without rights
- [ ] Android references follow the Android Brand Guidelines
- [ ] No pretending to be another app to trick users into actions meant for the trusted app (Social Engineering)

**Target API level** (details in [Console and release](7-console-and-release.md#73-target-api-level)): new apps and updates must target an API level within one year of the latest major Android release or submission is blocked. Unupdated apps not within two years are hidden from new users on newer Android versions.

**Violations Google lists:** a developer name implying a Google relationship; a national emblem implying government ties; a copied business logo; a cryptocurrency website's logo in the icon; a famous TV show's character and title in an icon.

Source: https://support.google.com/googleplay/android-developer/answer/9888689 and https://support.google.com/googleplay/android-developer/answer/9888374

## 3.5 SDKs

The developer is responsible for every SDK and for third-party code behavior. SDKs must align with the app's policy-compliant use of data.

- [ ] No SDK sells personal and sensitive user data, whether sent to a server or collected by embedded code. User-initiated transfers are not sales
- [ ] SDK data access is limited to purposes users reasonably expect, handled securely (modern cryptography such as HTTPS), and gated by runtime permission requests where available
- [ ] Unexpected SDK data use meets the prominent disclosure and consent rules
- [ ] For SDKs that collect personal and sensitive data by default, evidence of prominent disclosure and consent can be produced within 2 weeks of a Google Play request, or the longer period given in the request
- [ ] Persistent device identifiers (IMEI, IMSI, SIM Serial) are not linked to other personal and sensitive data or to resettable identifiers. Exceptions: SIM-linked telephony, and enterprise device management in device owner mode, both with prominent disclosure
- [ ] Data collected through SDKs is declared in the Data safety section, and it matches the privacy policy
- [ ] Permissions and sensitive APIs used by an SDK are necessary for features promoted in the listing
- [ ] Child-directed apps include only SDKs that self-certified for child-directed use (see [Families](6-families.md#65-families-self-certified-ads-sdk-program))
- [ ] SDK foreground services have a valid use case and are declared in the app manifest
- [ ] SDKs meet Malware, Mobile Unwanted Software, Device and Network Abuse, and Deceptive Behavior rules. An SDK must not evade app review

**Evidence:** list SDKs from `build.gradle` or the dependency report, then check each for network calls, permissions, and identifiers in the merged manifest. Check the Google Play SDK Index for outdated or non-compliant versions (`Verify`: the SDK Index is not part of the policy text).

**Field report:** libraries that add permissions to the merged manifest cause rejections the developer did not expect. Example: Expo's `expo-video` merging `FOREGROUND_SERVICE_MEDIA_PLAYBACK` even with background playback disabled in config (Expo issue 39988). Inspect the merged manifest of the release build, not just the app config.

**Violations Google lists:** an SDK that collects personal data without treating it as user data; an SDK that claims anti-fraud only but shares data for ads or analytics; an SDK sending installed packages without prominent disclosure; an SDK linking IMEI with location; an SDK linking the advertising ID to persistent identifiers or email; an SDK requesting background location for an undisclosed purpose; an SDK sending IMEI from `READ_PHONE_STATE` without consent; an SDK sending audio or call recordings unrelated to function; an SDK billing users through the phone bill by trickery; an SDK that uses foreground services without a use case, or one not declared in the manifest.

Source: https://support.google.com/googleplay/android-developer/answer/13323374

## 3.6 Malware and mobile unwanted software

Malware is any code that could put a user, their data, or a device at risk. The rules apply to third-party code, including SDKs. Code can be flagged even if harm was not intended.

**Malware categories**

- [ ] No backdoors: code allowing unwanted, remote-controlled operations. Dynamic code loading that is used to extract SMS is a backdoor. Arbitrary code execution with no sign of malicious intent is treated as a vulnerability to patch
- [ ] No billing fraud: premium SMS without consent (or hiding disclosures or carrier confirmations), premium calls without consent, or toll fraud (carrier, WAP, or airtime billing, including silent clicks on a transparent webview)
- [ ] No denial of service, such as high-volume HTTP requests to overload remote servers
- [ ] No hostile downloaders: code made to spread harmful apps, or whose downloads are at least 5% harmful with at least 500 observed downloads (25 harmful). Major browsers and file-sharing apps are exempt if all downloads are user initiated
- [ ] No phishing: code posing as a trusted source to collect credentials or billing information, or intercepting credentials in transit
- [ ] No elevated privilege abuse: breaking the sandbox, stealing OAuth tokens from other apps, preventing uninstall or stop, disabling SELinux
- [ ] No ransomware: locking the device or encrypting data for payment, or using device policy manager features to block removal. Subsidized device management code that meets lock, disclosure, and consent rules may be excluded
- [ ] No rooting without the user told in advance, and no other harmful action alongside it
- [ ] No spam: unsolicited messages to contacts, or using the device as an email spam relay
- [ ] No spyware: collecting, exfiltrating, or sharing user or device data unrelated to policy-compliant function, including recording audio or calls and stealing app data
- [ ] No trojans: harmless-looking apps with a hidden harmful part
- [ ] No riskware: obfuscation, dynamic code loading, or cloaking to show different or fake functionality
- [ ] No non-Android threats (components harmful to other platforms)

**Monitoring apps (stalkerware)**: only apps designed and marketed exclusively for parents monitoring children, or enterprises monitoring employees, are acceptable. Not for tracking a spouse, even with consent.

- [ ] The manifest uses the `IsMonitoringTool` metadata flag. Help article: the value is `child_monitoring`, `enterprise_management`, or `other` (`other` gets a case-by-case exemption review), on all version codes across all tracks
- [ ] Not presented as spying or secret surveillance, and tracking is not hidden or cloaked
- [ ] A persistent notification whenever the app runs, and a unique icon that identifies the app
- [ ] Monitoring is disclosed in the store description
- [ ] The listing does not link to a non-compliant APK hosted outside Google Play
- [ ] Prominent disclosure and consent per the User Data policy

**Mobile unwanted software (MUwS)**

- [ ] The app delivers every function it communicates, and explains system changes and lets users review and approve significant installation options
- [ ] No false claims that the device is in a critical security state or infected
- [ ] No invalid activity designed to increase ad traffic or conversions
- [ ] No requests, tricks, or rewards (extra features) to turn off device protections such as Google Play Protect
- [ ] Personal and sensitive data handled as the User Data policy requires, with secure transmission
- [ ] No ads shown in unexpected ways: impairing device functions, or displayed outside the app without being easily dismissable and with adequate consent and attribution
- [ ] No interfering with other apps or device usability, and uninstall is clear
- [ ] No mimicking OS or other apps' prompts, and no suppressing alerts from other apps or the OS, especially those about OS changes
- [ ] System notifications are used only for integral features (for example an airline's deals alert), and never to serve ads
- [ ] No ad fraud: hidden ads, automatic ad clicks, fake install attribution clicks, ads popping up outside the app, spoofing another OS or a different package name to ad networks
- [ ] Bundled software is disclosed
- [ ] No hostile downloaders of unwanted software, under the same 5% and 500 download test as above

**Evidence:** `SmsManager` or premium-number calls, hidden or zero-size webviews, root checks that run `su` commands, `DevicePolicyManager` calls that block uninstall, and ad code that triggers clicks. Verify that a monitoring app sets the flag and shows the notification.

**Violations Google lists:** an SDK from a provider that distributes malware; stealing OAuth tokens; abusing features to prevent uninstall; disabling SELinux; ads delivered through a system notification; ads that look like app UI; hidden ads; automatic ad clicks; fake install attribution; popup ads outside the app.

Source: https://support.google.com/googleplay/android-developer/answer/9888380 and https://support.google.com/googleplay/android-developer/answer/9970222

## 3.7 FLAG_SECURE, on-device containers, and full-screen intent

- [ ] Apps do not facilitate or create workarounds that bypass another app's `FLAG_SECURE`. Accessibility Tools are exempt if they do not transmit, save, or cache protected content for access outside the device
- [ ] Apps that provide on-device Android containers read the manifests of apps they load, do not load apps that declare `REQUIRE_SECURE_ENV`, do not proxy device APIs to make them appear installed in the container, and do not work around the flag (for example by loading an older version)
- [ ] `USE_FULL_SCREEN_INTENT` (target API 34+) is granted automatically only when core function is setting an alarm or receiving phone or video calls. Otherwise the user must grant it. It must not interfere with, disrupt, or access the device in an unauthorized manner

**Evidence:** `FLAG_SECURE` handling in screen capture or accessibility code; `REQUIRE_SECURE_ENV` in the manifest of apps that opt out of containers; `USE_FULL_SCREEN_INTENT` in the merged manifest and the notification it fires.

Source: https://support.google.com/googleplay/android-developer/answer/16559646 and https://support.google.com/googleplay/android-developer/answer/13609005
