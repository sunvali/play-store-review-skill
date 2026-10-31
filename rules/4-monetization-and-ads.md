---
name: monetization-and-ads
description: Google Play payments, billing programs by region, subscriptions, loot boxes, ads, and Advertising ID
---

# 4. Monetization and Ads

## 4.1 Payments

**Establish the facts before flagging.** A non-Play checkout is not automatically a violation. Determine what is sold (digital or physical), which countries the app sells in, and whether the developer is enrolled in a program. If you cannot tell, report what needs verifying.

| Sold through the app | Default | Exception |
|---------------------|---------|-----------|
| Digital goods, features, subscriptions, in-game currency | Google Play billing | Enrolled alternative billing or external content links program in an eligible region |
| Physical goods and services | **Must not** use Play billing | |
| Peer-to-peer payments, online gambling, regulated clinical transactions | **Must not** use Play billing | |
| Paid app download | Google Play billing | |

**Regional programs**

- **United States:** Play billing is not required on mobile and tablet apps. Developers may use other in-app payment methods, tell users about them, and link out, but must follow the Payments policy and enroll in the alternative billing or external content links program. From 2026-10-01 enrolled developers report transactions and pay service fees. External content links developers have until 2027-02-01 to report downloads and pay related fees.
- **EEA, India, South Korea, and other regions:** programs differ. Verify against the current Payments article before stating eligibility.
- **Worldwide sale:** an unenrolled link-out is a violation wherever no program applies. Solve it per region, or use Play billing.
- **Japan:** developers selling into or out of Japan must complete authorization by 2026-12-01, or their payments are held globally.

**Steering.** Outside enrolled programs, do not steer users to other payment methods through listings, promotions, webviews, or sign-up flows.

**AI purchases.** The Payments policy now covers apps that facilitate digital purchases through AI or agentic experiences. Verify current wording if the app does this.

**Implementation checks**

- [ ] Purchases use a current Play Billing Library version
- [ ] Purchases are acknowledged, and verified on a server when they unlock value
- [ ] Prices shown match the Play billing interface
- [ ] In-app virtual currency works only inside the app that sold it
- [ ] Loot box odds are disclosed before and near the purchase

## 4.2 Subscriptions

- [ ] Price, period, renewal, and any trial end are clear before purchase
- [ ] Users can cancel, and learn how
- [ ] Eligibility-based discounts, such as student plans, disclose eligibility criteria, verification, and post-eligibility pricing. Policy Deadlines lists this for 2027-01-27

## 4.3 Ads

Flag only what the code or a captured screen shows. Ad timing is usually decided at runtime.

- [ ] Ad content suits the app's content rating, and users can tell which app serves each ad
- [ ] Ads never mimic app UI or system notifications
- [ ] No forcing clicks or personal data before use
- [ ] Full-screen interstitials are never unexpected, such as before the splash screen, at level start, or during another task
- [ ] Interstitials can be closed within 15 seconds. Opt-in rewarded ads and non-intrusive banners are exempt
- [ ] No fake dismiss buttons, no ads where users tap for functions, and no ads on exit or home screen
- [ ] No consecutive interstitials triggered by user actions
- [ ] No lock-screen ads, unless the app's exclusive purpose is a lockscreen
- [ ] No ad fraud: invisible ads, automatic clicks, or fake attribution
- [ ] System notifications are for app features, not ads
- [ ] Location is never requested solely for ads, and location used for ads is in the privacy policy

Advertising ID rules are in [Privacy](2-privacy-and-permissions.md#21-user-data). Declare `com.google.android.gms.permission.AD_ID` when targeting API 33 or higher and using the ID. Child-directed ad rules are in [Families](6-families.md).
