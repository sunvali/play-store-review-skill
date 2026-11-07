---
name: privacy-and-permissions
description: Google Play user data, prominent disclosure, Data safety, privacy policy, account deletion, restricted permissions, and foreground services
---

# 2. Privacy and Permissions

Basis: Developer Program Policy effective 2026-10-29, plus the linked help pages. A rule not yet in force carries `(from YYYY-MM-DD)`. Never report those as current violations. Report them as "will fail from that date".

## Contents

- 2.1 User data (identifiers, SDKs, AI providers)
- 2.2 Prominent disclosure and consent
- 2.3 Data safety form
- 2.4 Privacy policy
- 2.5 Account deletion
- 2.6 Restricted permissions (table, SMS and call log exceptions)
- 2.7 Foreground services
- 2.8 Age Signals API

## 2.1 User data

- [ ] Every access, collection, use, and sharing of user data is disclosed. Use is limited to disclosed, policy-compliant purposes the user reasonably expects
- [ ] Personal and sensitive data is not sold. Sale means transfer to a third party for money. A user-initiated transfer is not a sale
- [ ] Sensitive data travels over modern cryptography such as HTTPS
- [ ] A runtime permission request comes before access to any data gated by a permission
- [ ] Every SDK is compliant, and its provider does not sell user data. This holds whether data goes via a server or via embedded code
- [ ] Third-party AI integrations (products, services, code) meet the same rules, including limited use, disclosure, and consent. The developer stays responsible
- [ ] Data used for ads follows the Ads policy (see 4.3)
- [ ] The app does not publish financial or government ID numbers, or non-public contacts
- [ ] Security or anti-virus apps explain, in the policy plus in-app disclosures, what they collect, how they use it, and who gets it
- [ ] Apps that handle EEA, UK, or Swiss personal information received from Google follow the data-protection duties on the page. If they cannot comply, they must tell Google at once at the address named there

**Identifiers**

- [ ] Persistent device IDs (IMEI, IMSI, SIM serial) are not linked to other personal data or to resettable IDs. Exceptions: SIM-linked telephony, and enterprise device-owner management. Both need prominent disclosure
- [ ] Advertising ID (AAID) is used only for ads and user analytics, and the opt-out setting is checked on every access
- [ ] AAID for ads: never linked to persistent IDs (SSAID, MAC, IMEI). Linked to personally identifiable information only with explicit consent. For analytics it links to neither
- [ ] After an opt-out: no profiling or personalized targeting. Contextual ads, frequency capping, conversion tracking, reporting, and fraud detection stay allowed
- [ ] After a reset: the new ID is not linked to the old ID or data derived from it, without explicit consent. After deletion the ID reads as zeros, and a device with no ID is not linked to data derived from a previous ID
- [ ] AAID use and collection are disclosed in a legally adequate privacy notice
- [ ] App Set ID: not used for ad personalization or ad measurement, and not linked to AAID, other Android IDs, or personal data for advertising. Use and collection are disclosed in the privacy policy, with legally valid consent where required

**Evidence:** merged manifest and network layer. Look for `http://` endpoints carrying personal data, `usesCleartextTraffic="true"`, SDK init that runs before consent, and the SDK list against the Data safety form. For AI features, find every call that sends user content to a model provider.

**Violations Google lists:**

- IMEI linked to location
- An SDK tying AAID to a SIM serial, or to an email address for analytics
- An SDK that claims anti-fraud use but shares data with third parties for ads or analytics
- An SDK that sends the installed-package list without disclosure
- An SDK that requests background location for an undisclosed purpose

Source: https://support.google.com/googleplay/android-developer/answer/10144311

## 2.2 Prominent disclosure and consent

**When it applies:** data access, collection, use, or sharing may be outside what the user reasonably expects. Example: collection while the app is not in use. SDKs that collect sensitive data by default are in scope.

The disclosure:

- [ ] Is inside the app and shown in normal use. Not only in the listing or on a website, and not behind a menu or settings
- [ ] Names the data and says how it is used and shared
- [ ] Is not only in the privacy policy or terms of service
- [ ] Is not bundled with unrelated disclosures

The consent:

- [ ] The consent or runtime permission request comes straight after the disclosure
- [ ] The user takes an affirmative action (tap accept, tick a box)
- [ ] Back, home, or tapping away is not treated as consent. Auto-dismissing or expiring messages are not consent
- [ ] Consent exists before any collection or access starts
- [ ] If the app relies on a non-consent legal basis such as GDPR legitimate interest, it still gives the in-app disclosure

Recommended wording pattern: "[App] collects/transmits/syncs/stores [data type] to enable [feature], [when]".

**Evidence:** trace the first collection call or permission request. If it runs before the accept action, or the user can dismiss and continue, the disclosure fails even when the screen exists. For SDK-driven collection, Google can ask for proof within 2 weeks (longer if the request says so).

**Violations Google lists:**

- Location collected with no disclosure of the feature, or of background use
- A runtime permission prompt shown before the disclosure
- Installed-app inventory, contacts, or screen recording treated as non-sensitive
- Restricted permissions used in the background for tracking, research, or marketing without disclosure and consent

Source: https://support.google.com/googleplay/android-developer/answer/10144311

## 2.3 Data safety form

**When it applies:** every app on closed, open, or production tracks, even apps that collect nothing (they still complete the form and link a privacy policy). Pregranted and preloaded apps that update through Play are in scope. Exempt: apps active only on internal testing, system services, private apps. Old artifacts with effective target SDK below 21 may be left out only if 90% or more of active installs use target SDK 21 or higher.

| Term | Meaning |
|------|---------|
| Collect | Data leaves the device, including via SDKs, and via webviews whose code or behavior the developer controls. Open-web browsing in a webview is out of scope |
| Share | Collected data goes to a third party: server to server, on-device to another app, via an SDK, or via a controlled webview |
| Not sharing | Service providers acting on the developer's instructions, legal-purpose transfers, user-initiated transfers the user expects (or transfers under a compliant prominent disclosure and consent), fully anonymized data |
| Ephemeral | Off-device data held only in memory, no longer than the live request needs. It MUST be included in the form response, but is not displayed on the listing. Ads and profile building are never ephemeral |
| Not collection | Data processed only on the device. End-to-end encrypted data that nobody but sender and recipient can read |
| Pseudonymous | Still disclosed if it can reasonably be tied back to a user |

- [ ] The form matches the code, every SDK, and the privacy policy. One global form covers the sum of all versions and regions currently distributed
- [ ] Each purpose is declared. Data collected as part of another type (photos used to infer traits) is declared for both
- [ ] "Optional" is used only if every user, on every device and region, can decline or skip it
- [ ] Encryption in transit is claimed only if the code uses industry-standard encryption such as TLS or HTTPS
- [ ] The deletion-request answer is true. It is valid when users can request deletion, or data is auto-deleted or anonymized within 90 days of collection. Legal or abuse retention does not block it
- [ ] Location: approximate means an area of 3 km2 or more, precise means under 3 km2. Location inferred from IP address or Access Point Name is declared
- [ ] IP-based location, advertising ID (as device or other IDs), and diagnostics sent with a device ID are declared
- [ ] Payment details that a payment service takes straight from the user, and the app never sees, are not declared. Purchase history or anti-fraud data the app receives is declared

**AI providers and other third-party processors**

- [ ] User content sent to an AI provider (prompts, images, audio, health or diet data, chat history, account data) is collection. Declare each data type and purpose
- [ ] Classify the provider. It is a service provider ("not sharing") only if it processes the data solely on the developer's behalf and instructions. Check its terms for use for its own purposes (training, profiling, ads). If it has such use, treat it as a third party and declare sharing. The training example is an inference from the service-provider definition. Google's own example is an SDK provider building ad profiles across customers
- [ ] A transfer triggered by a specific user action the user expects, or covered by a compliant disclosure and consent, need not be declared as sharing. It is still collection
- [ ] The privacy policy names the provider type and what it receives (see 2.4)
- [ ] An unexpected or background transfer to an AI provider has a prominent disclosure (see 2.2)

**Evidence:** list network destinations and SDK init calls, then compare them to the declared types and sharing flags. Check each SDK's own published Data safety info or its Google Play SDK Index entry.

**Violations Google lists:** none itemised for the form. Google says it can enforce on any gap between app behavior and the declaration.

Note: one FAQ answer on that page words the ephemeral rule as "no need to include". The definition section says include. Follow the definition. `Verify` on the live page if a finding depends on it.

Source: https://support.google.com/googleplay/android-developer/answer/10787469

## 2.4 Privacy policy

- [ ] Linked in the Play Console field **and** in the app (link or text)
- [ ] Active, public, non-geofenced URL. **No PDFs.** Not editable by visitors
- [ ] Includes developer information and a privacy contact or inquiry method
- [ ] Lists the personal and sensitive data types accessed, collected, used, and shared, and every party they are shared with
- [ ] Describes secure handling, and the retention and deletion policy
- [ ] Clearly labeled as a privacy policy (for example in the title)
- [ ] Names the entity shown on the store listing, or names the app
- [ ] Exists even if the app touches no personal data
- [ ] Consistent with the Data safety form. The policy covers more than the form does

**Evidence:** the Console field, an in-app link or text, and the live page.

**Violations Google lists:** omitting data handling, missing app or company identification, no globally reachable URL.

Source: https://support.google.com/googleplay/android-developer/answer/10144311

## 2.5 Account deletion

**When it applies:** users can create an account in the app, or the app sends them to an account-creation flow outside it. It applies even if the account is optional. Accounts created and operated offline are out of scope.

- [ ] A readily discoverable in-app path starts deletion, such as account settings. A full in-app flow is ideal. A link in the app to the web deletion resource is accepted
- [ ] A web resource is linked in the Play Console URL field. It loads, shows the deletion path prominently, and names the app or developer as listed on Play
- [ ] The web route works without reinstalling the app
- [ ] Deletion removes the account and its associated user data. Freezing, disabling, or deactivating does not count
- [ ] For data held by service providers: delete from own servers and ask the provider to delete
- [ ] Retained data (security, fraud prevention, regulation) is disclosed, for example in the privacy policy
- [ ] Prerequisites, such as cancelling a subscription, are explained, with a support route
- [ ] The Data safety deletion answers match this behavior

**Exempt:** permanently private apps and enterprise device management apps. Non-mobile surfaces (Wear OS, TV, web) need only the web option. Highly regulated industries may add flows.

**Evidence:** the account settings screen, the Console URL, and the retention text.

**Violations Google lists:** hidden or unduly hard steps, broken or outdated links, missing retention information, a web page that does not reference the app.

Sources: https://support.google.com/googleplay/android-developer/answer/13327111 and https://support.google.com/googleplay/android-developer/answer/10144311

## 2.6 Restricted permissions

General rules:

- [ ] Each permission is needed by a current feature promoted in the listing. No undisclosed, unimplemented, or disallowed use
- [ ] Requests are in context (incremental), not all at launch
- [ ] A user who declines gets a reasonable alternative, such as manual entry. No pressure into non-critical permissions
- [ ] Data from permissions is never sold or shared for sale

Flag **SMS and call log** and any "must be removed" item from the manifest alone. For the rest, trace the use.

| Permission | Allowed when | Alternative | Console declaration |
|-----------|--------------|-------------|---------------------|
| `READ_MEDIA_IMAGES`, `READ_MEDIA_VIDEO` | Target API 33+. Only if system pickers cannot support core functionality | Android Photo Picker | Yes: why the picker is not enough |
| `MANAGE_EXTERNAL_STORAGE` | Target API 30+. Only if platform intents cannot support core functionality. No storage access for third parties outside core function. Prompt users to enable "All files access" | Storage Access Framework | Yes |
| SMS group (`READ_SMS`, `SEND_SMS`, `RECEIVE_SMS`, `WRITE_SMS`, `RECEIVE_MMS`, `RECEIVE_WAP_PUSH`) | Active default SMS or Assistant handler, or a listed exception | SMS Retriever, SMS User Consent, SMS intent | Yes |
| Call log group (`READ_CALL_LOG`, `WRITE_CALL_LOG`, `PROCESS_OUTGOING_CALLS`) | Active default Phone or Assistant handler, or a listed exception. Phone-call account verification stops being valid (from 2027-01-27) | Digital Credentials API, SMS Retriever, Incoming Call Retriever, Dial intent | Yes |
| `ACCESS_BACKGROUND_LOCATION` | Feature benefits the user and is core. Strong justification and explicit consent. Never solely for ads or analytics | Foreground ("while in use") location | Yes |
| `ACCESS_FINE_LOCATION` | Minimum scope: coarse before fine, foreground before background. (from 2027-01-27, target API 37+) the location button serves one-time or infrequent requests | `ACCESS_COARSE_LOCATION`, Android location button | (from 2027-01-27) Yes: why coarse and the button are insufficient |
| Broad contacts access (`READ_CONTACTS`) | (from 2027-01-27) only if core functionality needs broad access | Android Contact Picker | `Verify`. Not stated in the text read |
| Manage Contacts | (from 2027-08-25) core functionality where system pickers are insufficient | Narrowly scoped platform intents | (from 2027-08-25) Yes, for apps targeting API 38+ (Android 18) |
| Local Network | (from 2027-08-25) core functionality where device pickers are insufficient. Manifest string: `Verify` | Device pickers | (from 2027-08-25) Yes, for apps targeting API 37+ (Android 17) |
| `QUERY_ALL_PACKAGES` | Target API 30+. Core purpose is to launch, search, or work with any installed app. Inventory is never sold or shared for analytics or ads | `<queries>` element, targeted package queries | Yes |
| `REQUEST_INSTALL_PACKAGES` | Core function is sending or receiving packages with user-initiated installs. Categories: browser or search, communication with attachments, file management, enterprise device management, backup and restore, device migration, wearable or IoT companion. No self-update or bundling APKs (device management excepted) | Not named in the text read | Yes. A change of use needs a revised declaration |
| `USE_EXACT_ALARM` | Target API 33+. Core function is an alarm or timer app, or a calendar app with event notifications | `SCHEDULE_EXACT_ALARM` (user grants) | Yes |
| `USE_FULL_SCREEN_INTENT` | Target API 34+. Auto-granted only for alarms and calls. Others must ask the user. Never to force disruptive ads or notifications, or to interfere with the device | Normal notification | Yes, to establish pre-grant eligibility |
| `BODY_SENSORS`, `BODY_SENSORS_BACKGROUND` | Apps targeting Android 16 (API 36) or higher must use the granular `android.permission.health.*` permissions (for example `READ_HEART_RATE`). Every request is reviewed | Granular health permissions | `Verify`. Not stated in the text read |
| Health Connect | Approved health and fitness use cases only. See below | None | Yes |
| `BIND_ACCESSIBILITY_SERVICE` | See below | Narrower APIs | Yes, with demo video |
| `BIND_VPN_SERVICE` | See below | None | Not stated. The listing must document use |

**SMS and call log exceptions.** Google may grant a temporary exception for a non-default-handler app when the use is core and no alternative method exists. Each is subject to review.

- Default handler roles: SMS, Phone, Assistant. Contact prioritization only for a default handler
- Backup and restore (must prove restore to the original default handler), caller ID and spam blocking, connected-device companions, cross-device sync, device automation
- Enterprise archive, CRM, or device management (corporate login required)
- Anti-smishing, only with a proven track record of significant user protection
- Government or authorized mobile operator quality-of-service reporting (`READ_CALL_LOG`)
- In-vehicle hands-free, emergency-alert SMS (`SEND_SMS`), proxy calls, cell broadcast (`RECEIVE_SMS`)
- SMS financial transactions, SMS money management, banking or brokerage call authentication, writing call history to the dialer (`WRITE_CALL_LOG`)
- System services with the `SYSTEM_UI_INTELLIGENCE` role
- Legacy APKs published before 2019-01-01, under conditions
- Not valid: authentication via broad access, invites, profiling, call recording, boosters, locators, keyboards, research, remote control, any sale of the data. Contact prioritization, SMS translation, and notification add-ons are invalid for a non-default app
- Always: be the default handler before prompting, stop using the permission when the role is lost, no placeholder manifest entries, no deriving the same data by other means

**Accessibility API.** Banned: changing settings without permission, blocking uninstall (unless a parent or admin authorizes it), bypassing platform security, privacy controls, or notifications, deceptive UI changes, remote call audio recording, and agents that autonomously plan and act. Use must be documented in the listing. `isAccessibilityTool` is only for apps whose core function directly supports people with disabilities. Other apps need prominent disclosure and consent. Narrower APIs are expected where possible.

**VpnService.** VPN must be core. Exceptions: parental control, enterprise management, app usage tracking, device security, network tools, web browsing, carrier apps. Document use in the listing and encrypt data from the device to the tunnel endpoint. No sensitive-data collection without prominent disclosure and consent. No redirecting other apps' traffic for monetization.

**Health Connect.** Only a health or fitness feature in an approved use case may request it. No headless access (a clear icon is required). Not for apps solely for children. No syncing between incompatible platforms. Data may not go to ads, brokers, credit decisions, or uncleared medical devices. Human access is restricted. Request the minimum scope. Privacy policy plus help text on managing and deleting data. Secure transmission.

Policy names system pickers as the alternative, so a feature that lets users pick a few photos, such as attachments in a support chat, does not justify a broad media permission.

**Field report** (not policy): the most corroborated rejection is `READ_MEDIA_IMAGES` or `READ_MEDIA_VIDEO` added by a plugin or library, where the app only needs a picker. Console wording seen: one-time or infrequent access, and not related to core purpose. Rewording the in-app prompt did not fix it. Remove with `tools:node="remove"`, switch to the Photo Picker, and fix Data safety. It can return after a rebuild because the merge re-adds it. Also seen: media-playback foreground-service permissions merged by Expo libraries, and debug-only permissions leaking into release builds.

**Source conflict, location button.** The Policy Deadlines table calls the button the "recommended minimum scope". The policy page and the 2026-10-29 announcement call it mandatory for API 37+ from 2027-01-27. Report the conflict, rely on the policy wording, and do not raise it as a current violation.

**Evidence:** the **merged** manifest of the release bundle (permissions from libraries still count), `tools:node="remove"` entries, `<queries>`, the Console declaration, and the listing text that documents core function.

**Violations Google lists:**

- SMS or call log declared without the default-handler role, including placeholder text
- `QUERY_ALL_PACKAGES` where targeted queries would work
- `REQUEST_INSTALL_PACKAGES` used for self-update
- Full-screen intent used to push disruptive ads
- Location requested solely for ads or analytics

Sources: https://support.google.com/googleplay/android-developer/answer/9888170 and https://support.google.com/googleplay/android-developer/answer/10208820 . Dates: https://support.google.com/googleplay/android-developer/table/12921780

## 2.7 Foreground services

**When it applies:** the app runs a foreground service and targets Android 14 (API 34) or higher.

- [ ] Each service has a valid `foregroundServiceType`
- [ ] The matching `FOREGROUND_SERVICE_*` permission is declared. Example: location needs `FOREGROUND_SERVICE_LOCATION`
- [ ] The Console declaration (App content page) exists per type. It gives a functionality description, user impact if the system defers the task, user impact if the system interrupts it, a demo video link of the user steps that trigger it, and the use case
- [ ] The use benefits the user and is core, is user-initiated or perceptible, can be stopped by the user, cannot be deferred or interrupted by the system without hurting the feature, and runs only as long as needed
- [ ] Exempt from those criteria: types `systemExempted` and `shortService`, and `dataSync` only with Play Asset Delivery
- [ ] For user-requested network transfers, Google recommends user-initiated data transfer jobs over `dataSync`. Those jobs must be user-initiated, network transfers only, and run only as long as needed
- [ ] `specialUse` is for limited cases that meet the other criteria, and is reviewed
- [ ] Location through a foreground service continues a user-initiated action and ends with it
- [ ] Geofencing is not an approved use (from 2027-01-27). Use the Geofence API
- [ ] Media playback is user-started. Automatic soundtracks do not qualify

**Evidence:** manifest `<service>` entries and types, the Console declaration and video, and the start trigger in code.

**Violations Google lists:** none itemised. Per-type video rules exist. For example, a `dataSync` backup video must show a user action, not automatic backup.

Sources: https://support.google.com/googleplay/android-developer/answer/13392821 and the Permissions for Foreground Services section of https://support.google.com/googleplay/android-developer/answer/18258653

## 2.8 Age Signals API

**When it applies:** the app reads Play Age Signals data (age and parental consent).

- [ ] Used only to meet legal or regulatory duties, such as age-appropriate experiences
- [ ] Never used for advertising, marketing, personalization, analytics, profiling, or business intelligence
- [ ] Never sold, shared, or transferred to a third party, except as strictly required by law

**Evidence:** every read of the Age Signals result, and where the value flows (analytics SDKs, ad SDKs, backend).

Source: https://support.google.com/googleplay/android-developer/answer/9888170
