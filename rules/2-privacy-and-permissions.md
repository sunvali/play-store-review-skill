---
name: privacy-and-permissions
description: Google Play user data, prominent disclosure, Data safety, privacy policy, account deletion, and restricted permissions
---

# 2. Privacy and Permissions

## 2.1 User data

- [ ] All collection and sharing is disclosed, including by SDKs, webviews the app controls, and third-party AI integrations
- [ ] Sensitive data is used only for disclosed, expected purposes, and is never sold
- [ ] Sensitive data is transmitted securely. Flag `http://` endpoints carrying credentials or personal data, and `usesCleartextTraffic="true"`
- [ ] Runtime permissions are requested before gated data is accessed
- [ ] Denied permissions are respected, with no manipulation into granting them
- [ ] Credentials and tokens never reach logs

**Identifiers:**

- [ ] IMEI and other persistent identifiers are linked to other data only for SIM-linked telephony or device-owner enterprise management
- [ ] Advertising ID is used only for ads and analytics, checks the opt-out on each access, and is not linked to persistent identifiers. A reset ID is not joined to old data without consent
- [ ] App Set ID is used only for analytics and fraud prevention, and is not linked to the Advertising ID

## 2.2 Prominent disclosure and consent

Required when data use may be unexpected, such as background collection. The disclosure:

- Appears in the app, before the permission prompt or collection
- Describes the data and how it is used and shared
- Requires an affirmative user action

Navigating away, or an auto-dismissing message, is not consent.

**Gatekeeper test:** trace the first collection call. If it runs before the accept action, or the user can dismiss and continue, the disclosure fails even if the screen exists.

## 2.3 Data safety form

Required for every app on closed, open, or production tracks, even apps that collect nothing.

| Term | Meaning |
|------|---------|
| Collection | Data leaves the device, including through SDKs and controlled webviews |
| Sharing | Collected data reaches a third party |
| Ephemeral | Held only in memory and discarded after the request. Still answered in the form, not shown on the listing. Ads and profiling are never ephemeral |
| Not sharing | Service providers acting on your instructions, user-initiated transfers |
| Out of scope | On-device-only processing, end-to-end encrypted data you cannot read, fully anonymized data |

- [ ] The form matches the code, every SDK, and the privacy policy
- [ ] Encryption in transit is answered truthfully
- [ ] Deletion questions are answered, and a deletion route exists
- [ ] Precise and approximate location are declared correctly

For a line-by-line data-flow trace, use Google's `play-policy-insights` skill (see [SKILL.md](../SKILL.md#relationship-to-googles-skill)).

## 2.4 Privacy policy

- [ ] Linked in Play Console **and** inside the app
- [ ] Public HTTPS URL, reachable worldwide with no login or geofence
- [ ] A standard web page. **PDFs and downloads are not accepted**
- [ ] Not editable by visitors
- [ ] Specific to the app, covering collection, use, sharing, retention, and deletion

## 2.5 Account deletion

Applies when users can create an account, even when an account is optional.

- [ ] Deletion starts inside the app, on a prominent path such as account settings. Wear OS, TV, and other non-mobile apps are exempt from this item
- [ ] A working public web link lets users request deletion without reinstalling, and names the app or developer as listed on Play
- [ ] Deletion covers the account and its data, including the data declared in Data safety. Freezing does not count
- [ ] Any legally required retention is disclosed
- [ ] Any prerequisite, such as canceling a subscription, is explained with a support path

**Exempt:** permanently private apps, enterprise device management apps, and accounts created and operated offline.

## 2.6 Restricted permissions

Report a permission only with its use. A manifest entry alone is enough to flag **SMS/Call Log** and any "must be removed" item, because declaring those without eligibility is itself the problem. For the rest, trace how it is used.

| Permission | Allowed when | Alternative | Console |
|-----------|--------------|-------------|---------|
| `READ_MEDIA_IMAGES`, `READ_MEDIA_VIDEO` | Pickers cannot support core functionality. One-time or infrequent picks do not qualify | Android Photo Picker | Declaration |
| `MANAGE_EXTERNAL_STORAGE` | Platform intents cannot support core functionality | Storage Access Framework | Declaration |
| `READ_SMS` and SMS group | App is the active default SMS or Assistant handler | SMS Retriever, SMS User Consent | Declaration |
| `READ_CALL_LOG` and call group | App is the active default Phone or Assistant handler. Phone-call verification ends 2027-01-27 | Digital Credentials API, SMS Retriever | Declaration |
| `ACCESS_BACKGROUND_LOCATION` | User-beneficial feature central to the app. Never solely for ads or analytics | Foreground location, Geofence API | Declaration and video |
| `ACCESS_FINE_LOCATION` | Minimum scope needed. Location button is mandatory for one-time or infrequent requests on API 37+ from 2027-01-27 | `ACCESS_COARSE_LOCATION` | Declaration for fine location |
| `READ_CONTACTS` | Needs broad contact access. Others use the picker from 2027-01-27 | Android Contact Picker | |
| Manage contacts | Core functionality, pickers insufficient. Listed for 2027-08-25 | Scoped platform intents | Declaration |
| Local network | Core functionality, device pickers insufficient. Listed for 2027-08-25 | Device pickers | Declaration for API 37+ |
| `QUERY_ALL_PACKAGES` | Core purpose needs awareness of all apps | `<queries>` declarations | Declaration |
| `REQUEST_INSTALL_PACKAGES` | Core purpose is sending or receiving packages with user-initiated installs. Never self-update | Play In-App Updates | Declaration |
| `USE_EXACT_ALARM` | Core purpose of the app is alarm, timer, or calendar event notifications. A timer feature in another kind of app is `Verify` | `SCHEDULE_EXACT_ALARM`, WorkManager, inexact alarms | Declaration |
| `USE_FULL_SCREEN_INTENT` | Auto-granted only for alarms and calls. Others ask the user. Never for ads | High-priority notification | Declaration |
| `BODY_SENSORS` | Approved health or fitness uses. API 36+ uses granular `android.permission.health.*` | Health Connect | Declaration |
| `BIND_ACCESSIBILITY_SERVICE` | See below | Narrower APIs | Declaration and listing text |
| `BIND_VPN_SERVICE` | See below | | Declaration, Organization account |

**Accessibility API.** `isAccessibilityTool` is only for apps whose core function directly supports people with disabilities. Other apps need prominent disclosure and consent. Not allowed: changing settings without permission, blocking uninstall without parent or admin authorization, bypassing privacy controls, remote call audio recording, or apps that autonomously plan and act.

**VpnService.** The VPN must be core functionality, with narrow exceptions such as parental control, device security, and network tools. Encrypt traffic to the endpoint, document use in the listing, and never redirect other apps' traffic for monetization.

**Health Connect.** Only health or fitness features may request it. Headless access is not allowed. Prohibited: safety-critical use, apps solely for children, and use for ads, credit decisions, or data sale. Request the minimum data, with a privacy policy and deletion help.

**Permissions added by libraries** still count. Check the merged manifest, and remove unwanted ones with `tools:node="remove"`.

## 2.7 Foreground services

For API 34+, declare the service type and its matching `FOREGROUND_SERVICE_*` permission, and complete the Console declaration with a description, user impact, and a demo video.

The use must benefit the user, be core to the app, be user-initiated or perceptible, be stoppable, not be deferrable by the system, and run only as long as needed.

- `systemExempted` and `shortService` are exempt. `dataSync` is exempt only with Play Asset Delivery
- Geofencing stops being an approved use on 2027-01-27. Use the Geofence API
- Location via a foreground service must continue a user-initiated action and end with it
- User-initiated data transfer jobs are for user-started network transfers only
