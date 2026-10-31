---
name: monetization-and-ads
description: Google Play payments, billing programs by region, subscriptions, loot boxes, ads, and Advertising ID
---

# 4. Monetization and Ads

Basis: Developer Program Policy effective 2026-10-29 and the linked help pages. A rule not yet in force carries `(from YYYY-MM-DD)`. Never report those as current violations.

## Contents

- 4.1 Payments (what must use Play billing, steering, AI and chat purchases)
- 4.2 Subscriptions
- 4.3 Ads
- 4.4 Regional billing programs
- 4.5 Play Billing Library versions

## 4.1 Payments

**Establish the facts before flagging.** A non-Play checkout is not automatically a violation. Find out what is sold (digital or physical), where it is sold, and whether the developer is enrolled in a regional program. If you cannot tell, report what needs verifying.

| Sold through the app | Default | Notes |
|---------------------|---------|-------|
| Paid app download | Play billing | |
| Digital goods and features: virtual currency, extra lives, add-ons, characters, ad-free upgrade, new paid features, subscriptions, cloud software and services | Play billing | Unless an enrolled regional program applies (4.4) |
| Physical goods, physical services (transport, airfare, gym membership, food delivery, live-event tickets), credit card or utility bill remittance | Play billing **must not** be used | |
| Peer-to-peer payments, online auctions, tax-exempt donations, online gambling, categories banned by the Payments Center content policy | Play billing **must not** be used | |
| Regulated clinical services (licensed provider, to diagnose or manage a medical condition) | Not Play billing | Example: doctor consult, prescription, treatment plan |
| Insurance, stock trades, investment consulting, tax preparation and filing | Not Play billing | Payments FAQ says these should not use it |
| Digital goods that can only be used outside the Play app | Play billing not required | Example: web-only content never consumed in the app |
| Gift cards sold in app | Play billing not required | |
| Earned or awarded points | Play billing not required | Selling points or virtual currency does require it |
| Tips where 100% goes to the creator and nothing digital is unlocked | Peer-to-peer, not required | If any condition fails, Play billing is required |
| 1:1 live paid service between two individuals, not recorded or replayable in a Play app | Not required | |
| Mixed digital and physical SKU | Play billing for SKUs with more digital than physical content, or marketed as digital | |
| Carrier or cable bill payment for bundled digital goods | Allowed only for eligible providers, in apps for managing the service or for subscribers | Needs Google's form |

**Fact checks.** Play billing is not required in a country where Google Play billing is not available. Tokenized assets such as NFTs bought as in-app digital content still need Play billing.

**Steering.** Outside a regional program, the app must not lead users to another payment method through any of:

- The Play listing
- In-app promotions for purchasable content
- Webviews, buttons, links, messaging, ads, or other calls to action
- UI flows, including sign-up or account creation flows

Allowed: links to administrative pages (account, privacy, help) that do not lead on to an alternate payment. Communication outside the app, such as email or special offers, is allowed. A consumption-only app (nothing can be bought in the app) may show plain text such as "go to our website" with no link.

**AI, chat agents, embedded experiences, and plugins.** If a Play-managed app facilitates purchases of digital goods, services, content, features, or functionality, the Payments policy applies in every implementation. That includes a purchase started in a chat agent, or inside a third-party embedded app experience or plugin. Check for: an assistant that takes payment or links to checkout; an embedded mini-app or plugin with its own checkout; deep links from a chat reply to a web store for digital items.

- [ ] Prices shown match the price in the Play billing screen. If the listing refers to features that cost extra, the listing says payment is required
- [ ] Virtual currency works only in the app or game title it was bought in
- [ ] Odds for randomized items (loot boxes) are disclosed before the purchase, and close to it in time and place
- [ ] The app uses a supported Play Billing Library version (see 4.5)
- [ ] Purchases are acknowledged, and verified on a server when they unlock value: `Verify` against the Play Billing docs. Not covered by the policy text read
- [ ] Enrolled in a program wherever a non-Play payment or outbound link exists (see 4.4)

**Evidence:** checkout code and URLs, webview targets, deep links, store-page links, SKU lists, billing client calls, listing text about paid features, and any agent or plugin that completes a purchase.

**Violations Google lists:**

- An in-app button, link, webview, or sign-up flow that leads to a non-Play payment
- Virtual currency usable in a different title
- Loot box odds missing or shown only after purchase
- In-app price different from the Play billing price

Sources: https://support.google.com/googleplay/android-developer/answer/9858738 and https://support.google.com/googleplay/android-developer/answer/10281818

## 4.2 Subscriptions

**When it applies:** the app sells any subscription or free trial.

- [ ] Before purchase, the screen states the offer terms, total cost, billing frequency, automatic renewal, and whether a subscription is needed to use the app. The user does not need to take any extra step to see this
- [ ] Monthly plans say they renew and charge every month
- [ ] Annual or multi-month plans do not headline the monthly equivalent as the main price. The real charge is the most prominent
- [ ] Price and terms are fully localized (language and currency)
- [ ] Promotions make clear the user can reach content without subscribing, when that is true. A clear dismiss button exists
- [ ] The purchase flow does not use several screens or repeated taps in one place that end in an accidental subscribe
- [ ] SKU and offer names are accurate. "Free Trial" is not used for an auto-recurring plan
- [ ] The subscription gives sustained or recurring value. One-time benefits (lump-sum credits or currency, single-use boosters) use in-app products. Bonuses may only add to recurring value. No cutting the benefit after the first period
- [ ] A subscription is not cancelled without the user's request after delivering a one-time benefit
- [ ] Free trial or intro offer: states duration, price after the offer, when and how it converts to paid, how to cancel, and what content is available without the trial. The post-trial charge is easy to read
- [ ] Account settings (or an equivalent page) disclose how to manage or cancel, and give an easy online route: a link to Google Play's Subscription Center, direct access to the app's own cancellation, or both
- [ ] Refund wording matches policy. By default, cancelling gives no refund for the current period, and access continues to period end. Local law can differ. Any more generous refund policy is the developer's to publish, and policy changes must be notified to users
- [ ] (from 2027-01-27) Subscriptions with ongoing eligibility requirements, such as student plans, disclose how eligibility is decided and verified, the non-discounted price or alternate plan the user moves to, and any change in benefits. Eligibility criteria must be clear and valid

**Evidence:** paywall and plan-selection screens in every locale, SKU and base-plan names, trial copy, account settings screen, and the Play Console subscription setup.

**Violations Google lists:**

- Monthly plan that does not say it renews monthly
- Annual plan most prominently showing the monthly cost
- Partly localized pricing and terms
- SKU named "Free Trial" for an auto-billing plan
- Several screens that lead to an accidental subscribe
- Benefit cut sharply after the first period (1,000 gems, then 1)
- No manage or cancel link in account settings
- Trial with unclear length, no auto-enrolment notice, or hard-to-read post-trial charge

Sources: https://support.google.com/googleplay/android-developer/answer/9900533 and the preview https://support.google.com/googleplay/android-developer/answer/18204939

## 4.3 Ads

**When it applies:** the app shows ads or ad-like offers. Ads and their offers count as part of the app. Flag only what code or a captured screen shows, since timing is often set at runtime.

**Content and honesty**

- [ ] Ad content and linked offers suit the app's content rating
- [ ] Ads do not mimic app features, system notifications, or warnings, and it is clear which app serves each ad
- [ ] No ads or offers delivered through system notifications or alerts. System notifications are for the app's integral features
- [ ] No forced ad click or personal data submission before full use of the app
- [ ] Fully dismissible ads: no missing dismiss button, no false dismiss button, no ad that appears where users tap for functions

**Placement and timing**

- [ ] Ads appear only inside the app serving them. None on the home screen, none triggered by home or exit, no overlay, companion, or widgetized ad units, and no interference with other apps, system or device buttons, or ports
- [ ] No unexpected full-screen interstitial, such as after a tap but before the tapped action takes effect
- [ ] No ad at the start of a game level or at the start of a content segment
- [ ] No full-screen video interstitial before the splash or loading screen
- [ ] Full-screen interstitials can be closed within 15 seconds. Opt-in interstitials, and ones that do not interrupt an action (for example after a score screen), may last longer
- [ ] Not subject to the Better Ads items above: rewarded ads the user explicitly opts into, video with integrated ads, and non-full-screen banners
- [ ] No back-to-back interstitials after consecutive user actions (the Made for Ads rule)
- [ ] No lock-screen ads or lock-screen monetization, unless the app's exclusive purpose is a lockscreen

**Fraud**

- [ ] No hidden or invisible ads, no automatic clicks, no fake install attribution clicks
- [ ] No ads popped up when the user is outside the app
- [ ] No false inventory claims, such as misreporting the platform or package name to an ad network

**Data and identifiers**

- [ ] Location used for ads is clear to the user, written in the privacy policy, and links the relevant ad network privacy policies
- [ ] Location permission is never requested solely for ads
- [ ] Advertising ID rules in 2.1 are met. For ads, the app uses the advertising ID in place of other device identifiers when it is available
- [ ] Apps that update their target to Android 13 (API 33) or higher declare `com.google.android.gms.permission.AD_ID` to read the advertising ID. Ad SDKs such as play-services-ads may add it by manifest merge, so read the merged manifest. Families policy says child-only apps should not request it at API 33+. Without an advertising ID (a deleted ID reads as zeros), a persistent identifier may be a fallback only with a privacy policy shown and lawful handling. For non-ads needs such as analytics and fraud prevention, App Set ID is the intended identifier
- [ ] Apps for children use the Families rules (see 6-families.md)

**Evidence:** ad SDK config and placement calls, interstitial trigger points, screenshots of each ad slot, the manifest, the privacy policy ad section, and the Console content rating.

**Violations Google lists:**

- A Teen-rated ad in an Everyone-rated app
- An ad styled as a feature, such as a question-mark icon that opens a landing page
- Ads that mimic system notifications
- A full-screen ad with no dismiss button, or with a false one
- An ad that appears where users tap for functions
- An ad on the home screen, or one triggered by home or exit
- A static ad at level start, or a video ad at the start of a content segment
- A gameplay interstitial not skippable within 15 seconds
- An interstitial after each of two consecutive taps ("Start app", then "Service")

Sources: https://support.google.com/googleplay/android-developer/answer/9857753 and https://support.google.com/googleplay/android-developer/answer/6048248 (Advertising ID). Ad fraud and system-notification rules: the Ad Fraud and Unauthorized Use or Imitation of System Functionality sections of https://support.google.com/googleplay/android-developer/answer/18258653

## 4.4 Regional billing programs

**When it applies:** the app has a non-Play payment, or an outbound link for digital goods, in a region where programs exist. The Payments policy allows an alternative in-app billing system, and outbound links, in eligible regions only for enrolled developers who accept the program terms.

Label: **from Google's regional program pages, read as raw text on 2026-10-31.** Fee percentages are left out on purpose, because Google's fee schedule is staggered by region and by new or existing install. Look them up when a decision needs them.

| Region | Program | Conditions to check | Dates |
|--------|---------|---------------------|-------|
| US | Alternative billing, External content links | Mobile and tablet, US users. Google says it will not require Play billing in US apps and developers may tell users about other methods. Programs still need enrollment. Alternative billing must stay in the app. Transaction reporting within 24 hours via APIs. Support, dispute, and refund routes. If Play Billing is offered, keep it reliably available. External links: US users and territories only, destination rules, registered external apps for download links, refunds unless clearly non-refundable. Both programs are opt-in | Enrolled developers report transactions and pay fees from 2026-10-01. Enrolled external-link developers have until 2027-02-01 to report successful downloads and pay the download fees. A 2026-03-04 settlement awaits a revised injunction: check the US update page live |
| EEA | Alternative billing, User choice billing, External offers, Billing choice | Business-registered developer for alternative billing and external offers. EEA users only. Required APIs and 24-hour reporting. Alternative billing and external offers: any form factor. External offers: not child-only apps, listing must not mention outside purchases, enrolled apps may use alternative billing without user choice only, not Play Billing. Billing choice (mobile and tablet) offers an in-app alternative with Play Billing beside it. User choice billing and the EEA program stay available | Billing choice and new install-based fees from 2026-06-30. External offers updated fees from 2026-06-04; link-outs to app downloads since 2025-12 |
| UK, Australia | Billing choice | Mobile and tablet. Play Billing is always offered next to alternatives. A custom choice screen only if it follows UX guidelines and is set in Console. Links to own offers only. Integrate the billing choice APIs (information screen, parental controls, 24-hour reporting) | UK from 2026-06-30. Australia from 2026-09-30 |
| Japan | Billing choice. External payments (closed to new enrolment) | External payments: business-registered, mobile and tablet, links shown beside Play Billing, own items only, not for apps aimed only at under-13s, listing must not mention outside purchases. Enrolled apps move to billing choice by 2027-03-31 to keep web links. Separate legal gate: sellers into or out of Japan must finish Japan authorization or payments are held globally | Billing choice from 2026-09-30. External payments closed to new enrolment 2026-09-30 and discontinued after 2027-03-31. Authorization due 2026-12-01 |
| India | Alternative billing alongside Play | Mobile and tablet users in India. PCI DSS certification, fraud reporting route, APIs, 24-hour reporting. May use embedded-webview payments. Play Billing stays offered beside it | API reporting available since 2023-11-14 |
| South Korea | Alternative billing alongside Play | Mobile and tablet users in Korea. APIs mandatory since 2023-08-02. PCI DSS, fraud reporting, 24-hour reporting | Fee changes and new Apps and Games programs scheduled for 2026-12-31. The billing choice page does not list Korea yet |
| Elsewhere | None found | An outbound link or alternative payment for digital goods is a violation unless a program applies | The fees page schedules Rest of World fee changes and expanded billing choice for 2027-09-30. The billing choice page lists no other market yet |

- [ ] Each non-Play checkout or outbound link maps to a program the developer has joined, for that region only
- [ ] Link-outs and alternative billing are limited to the eligible users and form factors (mobile and tablet)
- [ ] Link destinations describe where the user is going before the link-out, carry no personal data in the URL unless it is secured or encrypted, do not redirect or mislead, and offer only the developer's own items
- [ ] Reporting and information-screen API calls exist where the program requires them

**Evidence:** Console enrollment status, region gating in code, the information-screen API calls, and reporting jobs.

**Violations Google lists:** none itemised on the pages read. The general steering rule in 4.1 applies where there is no enrollment.

Dates above come from each program page and the fees page. A regional program can change with a court order or settlement, so the live page wins.

Sources: https://support.google.com/googleplay/android-developer/answer/15582165 (US update), https://support.google.com/googleplay/android-developer/answer/16497028 (US alternative billing), https://support.google.com/googleplay/android-developer/answer/16470497 (US external links), https://support.google.com/googleplay/android-developer/answer/12348241 (EEA), https://support.google.com/googleplay/android-developer/answer/14372887 (EEA external offers), https://support.google.com/googleplay/android-developer/answer/17161464 (billing choice), https://support.google.com/googleplay/android-developer/answer/16787536 (Japan external payments), https://support.google.com/googleplay/android-developer/answer/13306652 (India), https://support.google.com/googleplay/android-developer/answer/11222040 (South Korea), https://support.google.com/googleplay/android-developer/answer/16954621 (fees), https://support.google.com/paymentscenter/answer/17595997 (Japan verification)

## 4.5 Play Billing Library versions

**When it applies:** the app uses Play billing. Source is the Play Billing deprecation FAQ, read as raw text on 2026-10-31 (page updated 2026-10-23).

**What the deadlines mean (per that page).** Every library version has a two-year deprecation cycle. The table gives each version two dates: a "new app and update deadline" and an "extension deadline". From the first date, new apps and updates to existing apps may no longer use that version and must use a later supported one. Already-published apps keep working, and unmaintained APKs need no update. The extension deadline is the last date to keep distributing on that version, and only for a developer who requests an extension through the form on the Policy status warning page in Console. A site banner confirms it for 7: by 2026-08-31 new apps and updates must use library 8 or later.

| Version | New app and update deadline | Extension deadline |
|---------|-----------------------------|--------------------|
| 7 | 2026-08-31 (passed) | 2026-11-01 |
| 8 | 2027-08-31 | 2027-11-01 |
| 9 | 2028-08-31 | 2028-11-01 |

Versions 5 and 6 are already past both dates. The dependency shows up only in APKs that require the `com.android.vending.BILLING` permission.

- [ ] The library version is supported for the release date: library 8 or later today. Without an approved extension, an update on library 7 is out of policy now. An approved library 7 extension ends 2026-11-01
- [ ] The manifest keeps the `com.google.android.play.billingclient.version` attribute. If a deprecation warning remains after upgrading, check whether manifest merging removed it
- [ ] Extensions are requested through the form on the warning's details page under Policy status.

**Evidence:** `com.android.billingclient:billing` version in Gradle, the merged manifest, and Policy status in Console.

Source: https://developer.android.com/google/play/billing/deprecation-faq
