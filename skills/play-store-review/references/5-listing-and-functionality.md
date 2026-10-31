---
name: listing-and-functionality
description: Google Play store listing metadata and asset specs, promotion, ratings and reviews, content ratings, spam, minimum and broken functionality, news apps, and hostile cases
---

# 5. Listing and Functionality

Find listing text in `fastlane/metadata/android/`, `app/src/*/play/`, or ask the user for it. Assets (icon, feature graphic, screenshots, video URL) usually live only in Play Console. If you cannot see an item, list it under "could not verify" rather than passing it.

Policy basis: Developer Program Policy effective 2026-10-29. Dated rules live in `deadlines.md`.

## Contents

- 5.1 Metadata
- 5.2 Store assets and text limits
- 5.3 Promotion
- 5.4 Ratings, reviews, and installs
- 5.5 Content ratings
- 5.6 Spam and minimum functionality
- 5.7 Broken functionality
- 5.8 News and magazines
- 5.9 Hostile cases

## 5.1 Metadata

- [ ] App title is 30 characters or fewer. Count every character, and check each localized title you can see
- [ ] No emojis, emoticons (kaomoji included), or repeated special characters in the title, icon, or developer name
- [ ] No ALL CAPS in those elements unless it is the brand name
- [ ] No text or image in the title, icon, or developer name that indicates store performance or ranking, price or promotion, or a relation to a Google Play program
- [ ] No misleading symbol in the icon, such as a new-message dot with no messages, or a download symbol on an app that is not about downloads
- [ ] No unattributed or anonymous testimonials in the description
- [ ] No data comparison of apps or brands, and no word blocks or vertical or horizontal word lists
- [ ] Title, description, icon, screenshots, and promotional images are accurate, descriptive, relevant, and not excessive or repetitive
- [ ] Nothing in the listing is sexually suggestive, profane, graphically violent (icons, promo images, video), or shows illicit drug use. For drugs, educational or artistic framing does not lift the general-audience rule
- [ ] App category is truthful. Choosing a category to qualify for different quality thresholds is a Metadata violation

**Evidence:** The policy applies the title (30 characters), emoji, ALL CAPS, ranking, price, and program-label bans to the title, icon, and developer name. The wider "misleading, improperly formatted, non-descriptive, irrelevant, excessive" test covers description, developer name, title, icon, screenshots, and promotional images. The category rule comes from the technical quality page FAQ.

**Violations Google lists:** unattributed or anonymous user testimonials; data comparison of apps or brands; word blocks and word lists; ALL CAPS that is not the brand name; irrelevant special character sequences; emoji, emoticon, and special-character use; misleading symbol; misleading text; images or text such as "App of the year", "#1", "Popular", award icons; "10% off", "$50 cash back"; "Editor's choice", "New"; sexually suggestive imagery; profane or vulgar language; prominent graphic violence in icons, promo images, or video; illicit drug use.

**Scope of the ranking, price, and program-label bans.** Both the Metadata and App Promotion policy text, and the Metadata help page, limit them to the app title, icon, and developer name. The asset page repeats them as a requirement for the icon (badges or text suggesting ranking, price, or Play categories), and as "highly recommended" guidance only for the short description, feature graphic, screenshots, and video. The policy's example list of violations names the items ("#1", "10% off", "Editor's choice") without naming where they appear, so it does not widen the rule. Ranking, price, or program text in a screenshot, video, feature graphic, or short description is therefore a risk under the general misleading or excessive metadata test, not a named violation. Say which sentence you relied on. The asset page allows Google Play awards such as "Best Of" in video text.

Source: https://support.google.com/googleplay/android-developer/answer/9898842

## 5.2 Store assets and text limits

Missing or malformed required assets block the listing. The asset page says failing its "Requirements" can lead to removal or suspension.

- [ ] App icon: 32-bit PNG with alpha, 512 x 512 px, at most 1024 KB, no badges or text suggesting ranking, price, Play categories, or otherwise misleading
- [ ] Short description present, at most 80 characters
- [ ] Feature graphic present: JPEG or 24-bit PNG with no alpha, 1024 x 500 px
- [ ] At least 2 screenshots across device types: JPEG or 24-bit PNG with no alpha, each side 320 to 3840 px, long side no more than twice the short side. Up to 8 per device type
- [ ] Chromebook and tablet listings: the page advises at least 4 screenshots (not under its Requirements heading), 1080 to 7680 px, 16:9 landscape or 9:16 portrait
- [ ] Wear OS: at least 1 screenshot of the current version, 1:1, at least 384 x 384 px, app UI only, no device frame, no transparency or masking
- [ ] Android TV: at least 1 TV screenshot and a banner, 1280 x 720 px, JPEG or 24-bit PNG with no alpha
- [ ] Android Automotive OS: screenshots required unless the app is in a parked category. If given, at least 2 portrait (800 x 1,280 px) and 2 landscape (1,024 x 768 px), generic system UI, not vehicle or OEM specific
- [ ] Android XR: 4 to 8 screenshots, PNG or JPEG, at most 8 MB each, 8:5 ratio
- [ ] Preview video (optional): one YouTube video URL, not a playlist or channel, no extra parameters such as timecodes. Ads off (monetization off, and no copyright monetization claims), public or unlisted (not private), not age-restricted, embeddable

**Evidence:** Specs are from the Play asset page. Items under its "Highly recommended" heading are eligibility guidance and do not affect the listing page: at least 4 screenshots at 1080 px or more for apps (at least 3 for games) to be eligible for screenshot-based recommendations; taglines under 20% of the image; no calls to action; no fake or empty status bar; no other store badge; no third-party trademarked characters or logos without permission; device imagery discouraged. Report these as advisory.

Text limits (app name 30, short description 80, full description 4,000 characters) are from https://support.google.com/googleplay/android-developer/answer/9859152. Repetitive or irrelevant keywords in any of them can lead to suspension.

Source: https://support.google.com/googleplay/android-developer/answer/9866151

## 5.3 Promotion

- [ ] No deceptive ads on websites, apps, or other properties, including notifications that resemble system notifications or alerts
- [ ] No sexually explicit ads that send users to the Play listing
- [ ] No promotion or install tactics that redirect users to Google Play or download apps without informed user action
- [ ] No unsolicited promotion by SMS
- [ ] The developer answers for its ad networks, affiliates, and ads

**Evidence:** The App Promotion policy bans apps that directly or indirectly engage in, or benefit from, promotion that is deceptive or harmful.

**Violations Google lists:** the first four bullets above, plus the ranking, price, and program-text bullet in 5.1.

Source: https://support.google.com/googleplay/android-developer/answer/9899004

## 5.4 Ratings, reviews, and installs

- [ ] No incentive offered for a rating (for example a discount for a high rating)
- [ ] No fake, repeated, or purchased ratings, reviews, or installs, and no posing as users to influence placement
- [ ] No encouraging reviews that contain affiliates, coupons, game codes, email addresses, or links to sites or other apps
- [ ] The app's main function is not paying users to install other apps
- [ ] Developer replies stay on the issue raised and do not ask for a higher rating

**Evidence:** The policy forbids manipulating placement through ratings, reviews, or install counts by illegitimate means. The reply guidance is listed as a best practice, not as a named violation.

**Verify:** whether a prompt that sends only happy users to the Play listing ("review gating") is penalized. The policy text read lists incentives and fraud, not routing. Use of the In-App Review API is not stated either. Report such a flow as `Verify`.

**Violations Google lists:** rating requests with an incentive; repeatedly submitting ratings as users; reviews containing affiliates, coupons, game codes, emails, or links.

Source: https://support.google.com/googleplay/android-developer/answer/9898684

## 5.5 Content ratings

- [ ] A content rating exists for the app. Apps without one are not allowed and are removed
- [ ] The questionnaire answers match the real content. Misrepresentation can lead to removal or suspension
- [ ] The questionnaire was redone after changes to content or features that affect the answers
- [ ] Ads shown are not significantly more mature than the app's own content
- [ ] A rating dispute goes to the IARC authority through the link in the certificate email, not through a Play appeal

**Evidence:** IARC assigns the rating from the Console questionnaire. The rating covers in-app content, not ads, agreements, or age-specific privacy practices. The 2026-07-15 announcement clarified that unrated apps are not allowed.

Source: https://support.google.com/googleplay/android-developer/answer/9898843

## 5.6 Spam and minimum functionality

- [ ] Not a webview of a website, or an affiliate-traffic app, unless the site owner or administrator gave permission. Earning sign-up or purchase credit on another site as the primary purpose is the violation
- [ ] Not a copy of other apps' content without original value, and not a set of highly similar small apps that should be one app
- [ ] No SMS, email, or other messages sent for the user without letting them confirm content and recipients
- [ ] Has app-specific functionality. Static text-only or PDF apps, very thin single-wallpaper apps, and apps that do nothing are limited-functionality violations

**Evidence:** Spam, Functionality, and User Experience policy.

**Violations Google lists:** share button that sends messages unconfirmed; app whose primary purpose is a webview of a site without permission; copying content without added value; multiple highly similar apps; static text or PDF apps; single-wallpaper apps; apps designed to do nothing.

Source: https://support.google.com/googleplay/android-developer/answer/9899034

## 5.7 Broken functionality

- [ ] The app installs, loads, and responds. No crashes, force closes, freezes, or abnormal behavior on the screens a reviewer reaches first
- [ ] Pre-launch report, if available, has no Errors (crashes, ANRs, defective libraries, restricted unsupported API use)
- [ ] Sign-in, onboarding, and permission-denied paths do not dead-end

**Evidence:** The policy lists apps that do not install, install but do not load, and load but are not responsive. The pre-launch page does not say its issues block publishing. Its errors cover crashes, ANRs, defective libraries, and restricted unsupported APIs. Warnings cover slow startup, sign-in or crawl problems, memory issues, and not-yet-restricted unsupported APIs. Crashes found in the report come from test devices and do not change your crash statistics, and Google says the report cannot catch every issue. The publishing block is the release "Errors summary" in 7.1. Dead-end states are advisory, not named policy.

**Violations Google lists:** apps that do not install; apps that install but do not load; apps that load but are not responsive.

Source: https://support.google.com/googleplay/android-developer/answer/9898783 and https://support.google.com/googleplay/android-developer/answer/9844487

## 5.8 News and magazines

- [ ] The app declares itself as News or Magazine in Play Console, with the self-declaration completed. An app also counts if it sits in the News and Magazine category and calls itself news or magazine in title, icon, developer name, or description
- [ ] Each article names its original publisher or author
- [ ] Content is updated regularly, not static
- [ ] Current contact information is clear and easy to reach
- [ ] Aggregators say who published third-party content
- [ ] A membership or subscription app shows an in-app preview before purchase
- [ ] Affiliate marketing or ad revenue is not the primary purpose

**Evidence:** News and Magazines section of the policy.

Source: https://support.google.com/googleplay/android-developer/answer/9935326

## 5.9 Hostile cases

- [ ] A localized listing, translated title, or video you cannot see: list as could not verify, not as passing
- [ ] "Free", "New", "Best", or "Sale" in the short description or screenshots: the asset page lists these as advisory for those assets. Policy-level violation only in title, icon, developer name. Report as a risk, not a named violation (see 5.1)
- [ ] YouTube video is private, age-restricted, monetized, or hits a copyright claim that adds ads: the video can fail to show
- [ ] Screenshot shows another store's badge, a fake notification bar, or third-party characters: advisory on the asset page, and a trademark problem can also be an Intellectual Property issue
- [ ] Feature graphic or screenshot exported with an alpha channel: fails the no-alpha requirement
- [ ] Thin webview wrapper of the developer's own site: the owner-permission test is met, but limited functionality (5.6) still applies
- [ ] App behaves differently by geography or device and the listing does not say so, or changes significantly between versions without a What's new note and listing update: Deceptive Behavior examples
- [ ] Code or flags that change app behavior when a reviewer runs it: the policy lists apps that modify or obfuscate behavior during review, and forbids manipulating Play review. Treat as high severity
- [ ] App claims a function a phone cannot do, or calls itself a prank or "for entertainment": the policy does not exempt it
- [ ] Rating prompt that filters users: `Verify` (5.4)

**Evidence:** Deceptive Behavior policy, with the 2026-10-29 clarification about manipulating the review process.

Source: https://support.google.com/googleplay/android-developer/answer/17006354
