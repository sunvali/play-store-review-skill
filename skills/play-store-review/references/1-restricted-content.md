---
name: restricted-content
description: Google Play Restricted Content (child safety, inappropriate content, age-restricted apps, finance, gambling, UGC, health, blockchain, AI-generated content) and Intellectual Property
---

# 1. Restricted Content

Load this file when the app has user content, chat, AI output, health, finance, crypto, gambling, dating, regulated goods, or third-party brand or media assets. These sections decide whether the app category is allowed at all, so check them before code details.

Items marked `Verify` come from Google help articles that sit behind the policy page and were not confirmed. Confirm them against the linked article before reporting.

## Contents

- 1.1 Child safety
- 1.2 Inappropriate content
- 1.3 Age-restricted content and Age Signals
- 1.4 Financial services
- 1.5 Gambling, games, and contests
- 1.6 User-generated content
- 1.7 AI-generated content
- 1.8 Health content and services
- 1.9 Blockchain content
- 1.10 Intellectual property

## 1.1 Child safety

- [ ] The app does not let users create, upload, or share content that exploits or abuses children. Apps without a prohibition face immediate removal
- [ ] No grooming, sextortion, sexualization of minors, child trafficking, or inappropriate interaction aimed at a child
- [ ] Apps that appeal to children contain no excessive violence, blood, or gore, and no harmful or dangerous activities
- [ ] No entertainment content that shows plastic surgery, weight loss, or other cosmetic changes to a person's appearance (negative body or self image)

**Child Safety Standards** apply to Anonymous Chat, Random Chat, Social, and Dating apps (anonymous and random chat in scope since 2026-08-26). Social and Dating mean an app that declares that category in Play Console. Anonymous and random chat are defined by core function (see 1.3). Whether children use the app, or the app is age-gated or adults-only, is irrelevant. Needs:

- [ ] Public standards (terms of service, community guidelines, or similar) that explicitly prohibit child sexual abuse and exploitation (CSAE)
- [ ] An in-app way to send feedback, concerns, or reports (self-certified)
- [ ] Action, including removal, once the developer has actual knowledge of CSAM (self-certified)
- [ ] A process to report confirmed CSAM to NCMEC or the regional authority, and compliance with child safety laws (self-certified)
- [ ] A designated child safety contact (a named individual, set in Play Console) who can speak to enforcement and review and act on Google Play notices

**Evidence:** terms or community guidelines text, the report control in the UI, and the Console fields. Per the help article, the standards must be a globally accessible web page that loads, covers CSAE or child safety, and names the app or developer as shown on the listing, with its link entered in Play Console. The in-app channel must be reachable without leaving the app (a support email or chat channel inside the app counts).

**Violations Google lists:** no prohibition on child-exploitation content in an app with user content; an app that appeals to children but has adult themes; a weight-loss or cosmetic-surgery entertainment app.

Source: https://support.google.com/googleplay/android-developer/answer/14747720 and https://support.google.com/googleplay/android-developer/answer/9878809

## 1.2 Inappropriate content

- [ ] Sexual content and profanity: none, including pornography, sexual aids or guides, bestiality, and "sugar dating" or escort services. Nudity is allowed only for educational, documentary, scientific, or artistic purpose and not gratuitous. Profanity or adult keywords in the listing count
- [ ] No apps that claim to undress people or see through clothing, even as a prank
- [ ] No non-consensual sexual content, including deepfakes, creepshots, hidden camera, or assault content
- [ ] Catalog apps (books, audiobooks, video) may carry sexual titles only if: they are a minor fraction of the catalog, not actively promoted (history-based recommendations and general price promotions are fine), no child endangerment, porn, or illegal titles, and minors are blocked from them
- [ ] Hate speech: nothing that promotes violence or hatred against groups by race, ethnicity, religion, disability, age, nationality, veteran status, sexual orientation, gender, gender identity, caste, immigration status, or similar. No hate symbols
- [ ] Violence: no gratuitous violence and no self-harm, suicide, eating disorder, or choking-game promotion. Fictional game violence (cartoons, hunting, fishing) is generally allowed
- [ ] Violent extremism: no terrorist or violent-extremist organizations, recruitment, or glorifying attacks. Educational, documentary, scientific, or artistic (EDSA) content needs clear EDSA context
- [ ] Sensitive events (disasters, public health emergencies, conflicts, deaths): no capitalizing on or insensitivity toward them. Content with EDSA value or awareness-raising intent is generally allowed
- [ ] Bullying and harassment: no threats, harassment, bullying, extortion, blackmail, or public humiliation
- [ ] Dangerous products: no facilitating sale of explosives, firearms, ammunition, or restricted accessories (bump stocks, gatling triggers, drop-in auto sears, conversion kits, magazines or belts over 30 rounds). No manufacturing instructions for explosives, firearms, ammunition, restricted accessories, or other weapons
- [ ] Marijuana: no facilitating sale, regardless of legality. Includes cart ordering, delivery or pickup, and THC products such as CBD oil with THC
- [ ] Tobacco, nicotine and alcohol: no facilitating sale of tobacco or nicotine (vapes, pouches). No encouraging illegal or inappropriate use, no showing use or sale to minors, no implying tobacco improves social, sexual, professional, intellectual, or athletic standing, no favorable portrayal of binge or competition drinking, no tobacco ads, banners, categories, or links to sellers. Google may allow limited tobacco sales in grocery or food delivery apps in certain regions with age gating (such as ID check at delivery), and cessation aids with age gating
- [ ] Illegal activity: no facilitating illegal drug sales or purchases, no instructions for growing or making illegal drugs

**Evidence:** listing text and screenshots, in-app strings, catalog data, and any sale or order flow for the goods above.

**Violations Google lists:** nude or minimally clothed suggestive poses; a hate-group symbol; realistic violence against people or animals; an in-app cart for marijuana; denying a well-documented tragedy; profiting from a sensitive event with no benefit to victims; bullying victims of international or religious conflicts.

Source: https://support.google.com/googleplay/android-developer/answer/9878810

## 1.3 Age-restricted content and Age Signals

Apps in these groups must use the Play Console tools to block minors:

- Real-money gambling, games, and contests
- Core function is matchmaking or dating. Dating as an incidental feature need not block minors if that feature is age-gated with appropriate safeguards
- Core function is randomly connecting users to talk to strangers (random chat in scope since 2026-08-26)
- Core function is anonymous communication where a user's identity is deliberately hidden (anonymous chat in scope since 2026-08-26)

- [ ] Console age restriction is set when the app's core function matches the list
- [ ] Incidental dating features are age-gated, and the gate is not trivially bypassed

**Play Age Signals API** (user age and parental consent data):

- [ ] Data is used only to meet legal or regulatory duties, such as age-appropriate experiences
- [ ] Not used for ads, marketing, personalization, targeted ads, analytics, profiling, or business intelligence
- [ ] Not sold, shared, or sent to any third party unless strictly required by law

**Evidence:** every read of Age Signals data and where it flows (analytics SDK, ad calls, backend). Google's 2026-10-29 announcement says Play Age Signals is launching globally. The developer docs (last updated 2026-07-20) still call the API beta, and their terms limit use to age-appropriate content and experiences, by the requesting app only.

**Violations Google lists:** none. Treat any ad, analytics, or third-party use of Age Signals data as a violation.

Source: https://support.google.com/googleplay/android-developer/answer/16302250 and https://developer.android.com/google/play/age-signals/overview

## 1.4 Financial services

Applies to apps that manage or invest money or cryptocurrency, including personalized advice. Any app with financial features completes the **Financial features declaration** in Play Console. Google must be able to link licenses and documents to the developer account. The Play Console requirements policy requires an Organization account for financial products and services such as banking, loans, stock trading, investment funds, and crypto wallets or exchanges (see [Console and release](7-console-and-release.md#710-account-type-and-developer-verification)).

- [ ] Binary options trading: not allowed
- [ ] Personal loans (nonrecurring loans to an individual, not for a fixed asset or education; includes payday, peer-to-peer, and title loans; excludes mortgages, car loans, revolving credit): app category is Finance, and the metadata gives minimum and maximum repayment period, maximum APR, a representative total-cost example, and a privacy policy
- [ ] No promotion of loans that must be repaid in full in 60 days or less from issue
- [ ] Earned Wage Access (EWA): Finance category, and metadata gives repayment terms, all fees, a representative total-cost example, and a privacy policy
- [ ] EWA features: repayment by payroll deduction or autopay with no extra interest, penalties, or fees if autopay fails; access limited to wages already earned this pay period; no interest; a low flat or percentage fee (roughly $1 to $5 per transaction or 1% to 5% of the advance); typically not reported to credit bureaus
- [ ] The loan rules above also cover lead generators and apps that connect users to third-party lenders
- [ ] Personal loan, lead generator, line-of-credit, loan calculator or guide, and EWA apps do not declare `READ_EXTERNAL_STORAGE`, `WRITE_EXTERNAL_STORAGE`, `READ_MEDIA_IMAGES`, `READ_MEDIA_VIDEO`, `READ_CONTACTS`, `ACCESS_FINE_LOCATION`, `READ_PHONE_NUMBERS`, or `QUERY_ALL_PACKAGES`
- [ ] Country rules checked for apps targeting:
  - United States: personal loan APR below 36% (36% or higher is banned), and maximum APR displayed, calculated consistently with TILA
  - India: only apps on the RBI list of digital lending apps deployed by regulated entities may submit loan apps. Platform-only apps say so in the declaration and name every NBFC and bank prominently in the description
  - Indonesia: valid license copy for lending under OJK Regulation 77/POJK.01/2016
  - Philippines: SEC registration number and Certificate of Authority, plus Corporate Name and Business Name, all in the app description. Lending crowdfunding such as P2P goes through PSEC-registered CF intermediaries
  - Nigeria: FCCPC approval letter for digital money lenders. Loan aggregators give documents and contacts for each partner lender
  - Kenya: CBK Digital Credit Provider license copy, accepted only if listed in the CBK directory. Platform-only apps provide the partner's license
  - Pakistan: one digital lending app per NBFC lender (more risks account termination), proof of SECP approval, and no short-term loan apps barring rare legal exceptions
  - Thailand: at interest of 15% or more, a BoT license or an MoF Pico or Pico-plus license. The listing names the licensed provider, the developer's legal entity, and maximum rates and fees. Below 15% the listing also carries the statement "This is a non-regulated loan provider under the BoT/FPO"

**Evidence:** the merged manifest of the release build, listing metadata for APR and repayment text, and the Console declaration.

Source: https://support.google.com/googleplay/android-developer/answer/9876821

## 1.5 Gambling, games, and contests

**Real-money gambling apps** are allowed only for these product types: online casino, sports betting, horse racing (where separately licensed), lotteries, and daily fantasy sports.

- [ ] Developer completed the gambling application process and is an approved governmental operator or a licensed operator in each country or state where distributed
- [ ] No gambling product beyond the license scope
- [ ] Under-age users are prevented from using the app
- [ ] Use is blocked in countries, states, and areas the license does not cover
- [ ] Not a paid app and no Google Play billing; free to download
- [ ] Rated AO (Adult Only) or the IARC equivalent
- [ ] App and listing show responsible gambling information
- [ ] All other apps do not accept real money (including in-app items bought with money) for a chance at a prize of real-world value. No online casinos, sports betting, or lotteries outside the approved path

**Daily Fantasy Sports (DFS):**

- [ ] Distributed only in the US, or approved under the gambling process elsewhere
- [ ] DFS application accepted, free, no Google Play billing, rated AO or equivalent, responsible gambling information shown
- [ ] Valid license for each US state or territory that requires one, use blocked where unlicensed or illegal, and under-age wagering prevented

**Gamified loyalty programs** (where lawful and not subject to gambling licensing):

- [ ] Rewards are supplementary to a genuine, separate qualifying purchase. No part of that purchase is a fee or wager, and no price uplift
- [ ] Game apps: rewards earned and redeemed at a fixed ratio documented in the app and in public official rules. No wagering, and no game performance or chance changes the reward
- [ ] Non-game apps: official rules in the app. Chance-based rewards disclose the odds (fixed odds) or the selection method. Drawings and sweepstakes state a fixed number of winners, an entry deadline, and a prize date. Any fixed ratio is documented in the app and terms

**Ads for gambling or real-money games** run only if all hold: legal in every location shown; local ad licensing met; no ads to known under-18 users; app not in Designed for Families; app does not target under-18s; responsible gambling information on the landing page, listing, or in-app; no simulated gambling (social casino, virtual slot machines); no companion function for wagering, payouts, odds or score tracking, or managing participation funds; and app content does not promote or direct users to real-money gambling.

**Evidence:** menu items, tabs, buttons, or webviews with calls to action such as "BET!", "REGISTER!", or "COMPETE!" for cash prizes; deposit, wager, or winnings flows; ad SDK category settings.

**Violations Google lists:** games that accept money for a chance at a physical or monetary prize; a cash-tournament call to action; apps that accept or manage wagers, in-app currency, winnings, or deposits; a children's app with gambling ads; a simulated casino pointing to real casinos; a sports-odds tracker with betting-site ads; gambling ads styled as buttons or icons.

Source: https://support.google.com/googleplay/android-developer/answer/9877032

## 1.6 User-generated content

Applies whenever users publish content that other users can see. Includes specialized browsers or clients that direct users to a UGC platform.

- [ ] Users accept the app terms or user policy before creating or uploading content
- [ ] Terms define objectionable content and behavior and prohibit it
- [ ] Moderation is real and ongoing, with action taken against content and users
- [ ] Monetization does not encourage objectionable behavior
- [ ] In-app tools match the UGC type:
  - Publicly accessible UGC (social networks, blogs): report content and users, and block users
  - Any 1:1 interaction (direct messages, tagging, mentions): block users
  - Closed, identified groups (a school or company): report content and users
- [ ] AR apps moderate objectionable AR content and sensitive anchoring locations (a military base, private property)

**Incidental sexual content** (a UGC app that mostly offers non-sexual content and does not promote sexual content) is allowed only if: hidden by default behind filters needing at least two user actions to fully disable; children are blocked by a neutral age screen or a legally appropriate system; content rating answers are accurate. Illegal and child endangerment content is never incidental.

**Evidence:** trace the write path, then find the report and block controls in the UI. A `reportContent()` API with no UI does not satisfy this. Also look for removal paths and a way to act on complaints.

**Violations Google lists:** promoting sexually explicit UGC, including paid features that principally encourage objectionable sharing; no safeguards against threats or harassment, especially of minors; posts meant to ridicule someone; continually ignoring complaints. Apps whose main use is objectionable UGC, or that gain that reputation, are removed.

Source: https://support.google.com/googleplay/android-developer/answer/9876937

## 1.7 AI-generated content

Applies to apps whose content comes from generative models based on user prompts. Policy examples: chatbots where chatting is a central feature, and images or videos generated from text, image, or voice prompts. Apps that only summarize a user's own content, or use AI as a hidden implementation detail, are not named in policy: report as `Verify`, not a violation.

- [ ] The app prohibits and prevents generating restricted content, such as child exploitation and deceptive content
- [ ] An in-app control lets users report or flag offensive output to the developer without leaving the app
- [ ] Reports feed filtering and moderation (policy says developers should)
- [ ] Third-party AI providers are covered by user data disclosures. The developer stays responsible (see [Privacy](2-privacy-and-permissions.md#21-user-data))

**Evidence:** the report or flag control in the UI, input and output filters, and a path from reports to moderation.

Source: https://support.google.com/googleplay/android-developer/answer/13985936

## 1.8 Health content and services

Applies to apps with health features or information, or that read health data to support non-health features (games, insurance).

- [ ] Health apps declaration completed on the App content page. All developers complete it, even apps with no health features
- [ ] Privacy policy link in the Console field, and a link or text in the app. The URL is active, public, non-geofenced, not a PDF, and non-editable
- [ ] Policy and in-app disclosures cover access, collection, use, and sharing of personal and sensitive data. Dangerous or runtime permissions meet prominent disclosure and consent rules
- [ ] No permission that the core health function does not need. Remove unused permissions
- [ ] Non-health apps that read health data make the link to the core function clear to users, and the policy reflects the limited use
- [ ] No misleading or potentially harmful health or medical function
- [ ] Apps that need external hardware (such as a glucose monitor) say so in the description and do not imply they work without it
- [ ] Apps that use device sensors (such as the camera for oximetry) state device compatibility in the description
- [ ] Regulated medical devices are declared (shown as "Medical Device") and proof of approval, clearance, or certification is available on request
- [ ] Other health apps carry a clear description disclaimer that the app is not a medical device and does not diagnose, treat, cure, or prevent any condition, and remind users to consult a healthcare professional
- [ ] No sale of prescription drugs without a prescription
- [ ] No unapproved substances: ephedra, hCG tied to weight loss or control, supplements with active pharmaceutical or dangerous ingredients, products under government action, names confusingly similar to controlled drugs, or false claims of equivalence to prescription drugs. Google points to LegitScript
- [ ] No health misinformation: claims that contradict medical consensus or can harm users
- [ ] Health Connect data is personal and sensitive data (see [Permissions](2-privacy-and-permissions.md#26-restricted-permissions))
- [ ] Regulated clinical service transactions should not use Google Play billing

**Designations:**

- [ ] Government-affiliated health apps submit proof through the Advance Notice Form
- [ ] Contact tracing or health status apps select "Disease Prevention and Public Health" and use the form
- [ ] Human subjects research: informed consent (parent or guardian for minors) and IRB or equivalent ethics approval unless exempt, with proof on request

**Evidence:** Console declaration, description text, permissions in the merged manifest. Permissions in scope of health data per the help article: `ACCESS_FINE_LOCATION`, `ACCESS_COARSE_LOCATION`, `ACCESS_BACKGROUND_LOCATION`, `ACTIVITY_RECOGNITION`, `BODY_SENSORS`, `BODY_SENSORS_BACKGROUND`, `BLUETOOTH_SCAN`, `BLUETOOTH_CONNECT`, `BLUETOOTH_ADVERTISE`, `CAMERA`, `RECORD_AUDIO`, `READ_CALENDAR`, `WRITE_CALENDAR`, `READ_SMS`, `SEND_SMS`. Google calls the list non-exhaustive. Health apps (medical and human subjects research) must also register as an Organization. Unverifiable clinical or weight-loss claims are findings here and under [Deceptive behavior](3-security-and-deception.md#33-deceptive-behavior).

**Violations Google lists:** an app claiming to cure cancer; claims that vaccines alter DNA; advocacy of unapproved treatments or conversion therapy; products with ephedra or hCG for weight loss.

Source: https://support.google.com/googleplay/android-developer/answer/16679511 and https://support.google.com/googleplay/android-developer/answer/13996367

## 1.9 Blockchain content

Applies to apps with tokenized digital assets secured on a blockchain.

- [ ] Buying, holding, or exchanging crypto goes through certified services in regulated jurisdictions. The app is not published where its services are prohibited. Google may request licenses. Hong Kong now also accepts the Virtual Asset Trading Platform license, and an "Additional Options" section covers regulatory exemptions (announced 2026-10-29). The country license table is in a separate help article not checked here (`Verify`)
- [ ] No on-device cryptomining. Remote management of mining is allowed
- [ ] Apps that sell tokenized digital assets or let users earn them declare this in the Financial features declaration
- [ ] In-app products for tokenized assets say so in their product details
- [ ] No promotion or glamorizing of earnings from playing or trading
- [ ] Gambling apps that integrate NFTs complete the gambling application
- [ ] Other apps accept nothing of monetary value for a chance at an NFT of unknown value. Purchased NFTs are used in the game. NFTs are never wagered or staked for real-world-value prizes, including other NFTs

**Violations Google lists:** selling NFT bundles without disclosing contents and values; pay-to-play social casino games that reward NFTs.

Source: https://support.google.com/googleplay/android-developer/answer/13607354

## 1.10 Intellectual property

Applies to the app, the listing, and the developer account. Google acts on clear copyright notices (DMCA), counterfeit notices, and trademark complaints.

- [ ] No copyrighted content without rights. Modifying it can still violate. Google may ask for proof of rights
- [ ] No cover art, marketing images, or artwork from albums, games, books, movies, TV, comics, or music videos
- [ ] No college or professional sports team logos
- [ ] No photos from a public figure's social media, or professional images of public figures
- [ ] No fan art indistinguishable from the original
- [ ] No soundboards of copyrighted clips
- [ ] No full copies or translations of books not in the public domain
- [ ] The app and listing do not encourage or induce infringement, including unauthorized download of copyrighted content in features, description, or screenshots
- [ ] No identical or similar trademarks likely to cause confusion, and no sale or promotion of counterfeit goods
- [ ] Written permission for third-party brand names, logos, and graphics exists. Contact the Google Play team before submission to avoid rejection

**Evidence:** bundled assets in `res/`, `assets/`, and raw audio or video; listing graphics; app name and icon; third-party content feeds.

**Violations Google lists:** streaming apps that let users download copyrighted content; a listing description or screenshot that urges unauthorized download; album, game, or book cover art; team logos.

Source: https://support.google.com/googleplay/android-developer/answer/9888072
