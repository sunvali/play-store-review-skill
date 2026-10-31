---
name: families
description: Google Play Families policies, target audience, child-directed data, social features, ads, and the Families Self-Certified Ads SDK program
---

# 6. Families

Load this file when any selected target age group includes children, **or** the listing, art, or wording appeals to children. Google can treat an app as child-directed from its imagery and terminology, whatever the Console says. "Works great for kids" in a listing is enough to raise this. "Children" can mean different things by locale, so legal counsel decides which age limits apply. Items marked `Verify` were not confirmed against a Google page.

Failing these requirements can lead to app removal or suspension.

## Contents

- 6.1 Target audience and Console answers
- 6.2 Requirements
- 6.3 Ads and monetization in child-directed apps
- 6.4 Social apps and features
- 6.5 Families Self-Certified Ads SDK program

## 6.1 Target audience and Console answers

- [ ] Target age groups in Play Console match the app
- [ ] More than one age group is chosen only if the app is designed for and appropriate for all of them. Apps for babies, toddlers, and preschool select only "Ages 5 & Under"
- [ ] Age groups that include both adults and children are chosen only if the app is truly designed for all ages
- [ ] Target Audience and Content, Data safety, and IARC content rating answers are accurate and agree, and are updated when the app changes
- [ ] Imagery and terminology are consistent with the declared audience. Google can override the declared audience after its own review
- [ ] Changes in the Target Audience section may be reviewed before an app update, and an app update is needed before the store reflects them. Google strongly recommends telling users through What's New or in-app notices when the target age group, ads, or in-app purchases change
- [ ] Misrepresentation in Play Console can lead to removal or suspension

**Evidence:** the Target Audience answers, store art and wording (young characters, cartoon style, "for kids"), and the Data safety answers. Per the Console help article: an app not primarily designed for children under 13 whose listing marketing suggests otherwise (youthful animation, young characters in graphic assets) may be rejected. The options are to remove those marketing elements, or to change the target age groups to children under 13 only, which requires meeting the Families policy.

Source: https://support.google.com/googleplay/android-developer/answer/9893335 and https://support.google.com/googleplay/android-developer/answer/9867159

## 6.2 Requirements

- [ ] Content that children can reach is appropriate for children. Content that suits only some regions may be limited to those regions
- [ ] The app is not just a webview of a website, and does not have a primary purpose of driving affiliate traffic to a site without the owner's permission
- [ ] The app collects no personal and sensitive information from children without disclosure, including through APIs and SDKs. Sensitive includes authentication information, microphone and camera data, device data, Android ID, and ad usage data
- [ ] Device phone number is not requested from `TelephonyManager`
- [ ] Bluetooth uses Companion Device Manager unless the app targets only OS versions that do not support it
- [ ] Legal compliance with COPPA, GDPR, and other applicable law, including APIs and SDKs
- [ ] AR content shows a safety warning immediately upon launch of the AR section. It stresses parental supervision and reminds users to watch their physical surroundings. The app does not require a device advised against for children (policy names Daydream and Oculus)
- [ ] Social apps whose main focus is chatting with strangers or anonymous chat (chat roulette, dating, kids-focused open chat rooms, anonymous apps, "blindfold" apps) do not target children (since 2026-08-26)

**Apps that target only children:**

- [ ] Do not transmit the Android advertising ID, SIM Serial, Build Serial, BSSID, MAC, SSID, IMEI, or IMSI
- [ ] Do not request `AD_ID` when targeting API 33 or higher
- [ ] Do not request location permission or collect, use, or transmit precise location
- [ ] Contain only APIs and SDKs approved for use in primarily child-directed services. Example: an OAuth API service whose terms say it is not approved for child-directed services

**Apps that target children and older audiences:**

- [ ] Do not transmit those identifiers from children or users of unknown age
- [ ] Use non-approved APIs and SDKs only behind a neutral age screen or in a way that collects no data from children, and never require them to reach app content
- [ ] The neutral age screen asks for a free-entry birth date. Per the Console help article, presetting the birth date to the required age (for example 13) or indicating that an age is required is a flawed setup

**Evidence:** merged manifest (`AD_ID`, location, phone state), network calls to ad or analytics SDKs, `TelephonyManager` calls, the age-screen UI, SDK list, and the store listing.

**Violations Google lists:** a store listing that promotes play for children but has adult-only content; APIs whose terms forbid child-directed use; glamorizing alcohol, tobacco, or controlled substances; real or simulated gambling; violence, gore, or shocking content; dating services or sexual or marital advice; links to websites that break Play policy; mature ads shown to children.

Source: https://support.google.com/googleplay/android-developer/answer/9893335

## 6.3 Ads and monetization in child-directed apps

Applies to all monetization: ads, cross-promotion of own and third-party apps, in-app purchase offers, and paid product placement. It applies when ads reach children or users of unknown age. Google may reject, remove, or suspend apps for overly aggressive commercial tactics.

- [ ] Only Google Play Families Self-Certified Ads SDKs show ads to those users
- [ ] Apps with mixed audiences use a neutral age screen so children get ads only from self-certified SDK versions
- [ ] No interest-based advertising or remarketing
- [ ] Ad content suits children, and ads follow the Families ad format rules
- [ ] Advertising laws and industry standards for children are met
- [ ] No ads that cover the whole screen or interfere with use without a clear way to dismiss (ad walls)
- [ ] Rewarded or opt-in ads that interfere with use can be closed after 5 seconds. Ads that do not interfere, such as video with integrated ads, may last longer
- [ ] No interstitial immediately upon app launch
- [ ] One ad placement per page: no banner with multiple offers, and no more than one banner or video ad
- [ ] Ads and promotions are clearly distinguishable from app content (no offerwalls or immersive ads that children cannot identify as ads). This includes promos for the developer's other listings
- [ ] No shocking or emotionally manipulative tactics to push ad views or purchases
- [ ] No dismiss button that triggers another ad, and no ads that suddenly appear where users usually tap
- [ ] Virtual game coins are clearly distinguished from real money in purchases
- [ ] No ads that move away from a finger
- [ ] No ads for: age-inappropriate media (TV, film, music), age-inappropriate games or software, alcohol, tobacco, or controlled substances, simulated gambling, contests or sweepstakes (even free), sexually suggestive content, dating or relationship sites, or violent and graphic content

Exceptions from the self-certified SDK rule, per the SDK program page: in-house advertising where SDKs manage cross-promotion of your own apps or owned media, and direct deals with advertisers where an SDK only manages inventory. Ad content and data collection must still meet the User Data and Families policies.

**Evidence:** ad SDK list and its child-directed settings flags, the ad placements in layouts, and the neutral age screen path.

**Violations Google lists:** ads that move away from a finger; no exit after 5 seconds; ads covering most of the screen with no clear close; banners with multiple offers; ads mistaken for app content; own-listing promos indistinguishable from app content.

Source: https://support.google.com/googleplay/android-developer/answer/9893335 and https://support.google.com/googleplay/android-developer/answer/9900633

## 6.4 Social apps and features

Applies when children are in the target audience.

- [ ] Social apps (main focus is sharing freeform content or communicating with large groups) show an in-app reminder to stay safe online and about real-world risk before child users exchange freeform media or information, and require adult action before child users exchange personal information
- [ ] Social features (extra functionality that lets users share freeform content or talk to large groups) give the same reminder and let adults manage them for child users (turn on or off, set levels), and require adult action before enabling personal-information exchange
- [ ] Adult action is a mechanism that verifies the user is not a child and does not encourage children to falsify their age. Examples: adult PIN, password, birthdate, email verification, photo ID, credit card, SSN
- [ ] Sharing or exchange features are disclosed in the content rating questionnaire

**Evidence:** the screen shown before chat or sharing, the parent gate, and the content rating answers.

Source: https://support.google.com/googleplay/android-developer/answer/9893335

## 6.5 Families Self-Certified Ads SDK program

Applies to ads SDKs and mediation platforms in apps in the Families program. For the app auditor, the practical test is the list below. Google says new applicants may join (2026-10-29).

- [ ] Each ads SDK in a child-directed app is a self-certified version listed in the Help Center or SDK Index
- [ ] The SDK is set for child-directed treatment, which disables personalized ads, interest-based ads, and remarketing, on a per-request or per-app basis
- [ ] Mediation uses only certified SDKs, or has safeguards that make mediated ads meet the rules, and passes ad content rating and child-directed treatment information
- [ ] The SDK does not transmit the advertising ID, SIM Serial, Build Serial, BSSID, MAC, SSID, IMEI, or IMSI from children or users of unknown age

SDK provider duties (not checked in the app): ratings of ad creatives with at least Everyone and Mature groups; real-time bidding creatives reviewed and privacy indicators passed to bidders; a visual mark on creatives from its inventory; ad formats that follow the Families rules; an English terms of service, privacy policy, and integration guide; a sample test app APK; compliance with COPPA and GDPR.

**Evidence:** every ads SDK and mediation adapter in the dependency report, plus their version numbers against the certified list.

Source: https://support.google.com/googleplay/android-developer/answer/12918983
