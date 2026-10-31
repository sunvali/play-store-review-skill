---
name: listing-and-functionality
description: Google Play store listing metadata, ratings and reviews, content ratings, spam, minimum functionality, broken functionality, and news apps
---

# 5. Listing and Functionality

Find listing text in `fastlane/metadata/android/`, `app/src/*/play/`, or ask the user for it. If you cannot see it, list it under "could not verify" rather than passing it.

## 5.1 Metadata

- [ ] App title is 30 characters or fewer (count every character)
- [ ] No emoji, emoticons, or repeated special characters in the title, icon, or developer name
- [ ] No ALL CAPS unless it is the brand name
- [ ] No ranking or award text in the title, icon, or developer name, such as "#1", "Best", or "Popular"
- [ ] No price or promotion text there, such as "Free" or "10% off"
- [ ] No Google Play program labels, such as "Editor's Choice"
- [ ] No misleading icon symbols, such as a fake unread dot
- [ ] No unattributed or anonymous testimonials in any listing text
- [ ] Listing text, images, and video suit a general audience
- [ ] Screenshots and descriptions match the real app

The ranking, price, and program-label bans above are written for the title, icon, and developer name. In the short and full descriptions, report a false claim, such as an award the app does not hold, as misleading under [Deceptive behavior](3-security-and-deception.md#33-deceptive-behavior). Report accurate promotional text there as `Verify`.

## 5.2 Promotion

- [ ] No deceptive promotion, including notifications that mimic system alerts
- [ ] No sexually explicit ads, and no install or redirect tactics without informed action
- [ ] No unsolicited promotional SMS
- [ ] The developer answers for its ad networks and affiliates

## 5.3 Ratings, reviews, and installs

- [ ] No incentives for ratings, and no gating rewards on giving a rating
- [ ] No fake or purchased ratings, reviews, or installs
- [ ] Review replies never ask for a higher rating
- [ ] Prompts use the Play In-App Review API. A custom "rate us" screen that filters or rewards users is the problem. A plain link to the listing is not

## 5.4 Content ratings

- [ ] IARC questionnaire completed. Unrated apps are not allowed
- [ ] Questionnaire resubmitted when content changes
- [ ] Ads are not significantly more mature than the app

## 5.5 Spam and minimum functionality

- [ ] No webview-only app without the website owner's permission, and no affiliate-traffic app
- [ ] No copy of another app without added value
- [ ] Many similar small apps are merged into one
- [ ] No sending messages on the user's behalf without letting them confirm content and recipients
- [ ] Not static-only content, such as a single PDF or wallpaper

## 5.6 Broken functionality

- [ ] No crashes, freezes, or failure to load. Check the pre-launch report
- [ ] Every advertised feature is reachable
- [ ] Offline, denied-permission, and empty states do not dead-end

## 5.7 News and magazines

- [ ] Self-declared in Play Console
- [ ] Article publishers or authors are cited, content is regularly updated, and contact details are easy to find
- [ ] Paid content has an in-app preview
- [ ] Aggregators identify sources, and affiliate or ad revenue is not the primary purpose
