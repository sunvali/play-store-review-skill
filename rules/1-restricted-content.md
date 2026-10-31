---
name: restricted-content
description: Google Play Restricted Content (child safety, inappropriate content, age-restricted apps, finance, gambling, UGC, health, blockchain, AI-generated content)
---

# 1. Restricted Content

Load this file when the app has user content, chat, AI output, health, finance, crypto, gambling, dating, or regulated goods. These sections decide whether the app category is allowed at all, so check them before code details.

## 1.1 Child safety

- [ ] No content or feature that facilitates child sexual abuse or exploitation, including grooming and sextortion
- [ ] Apps for children avoid excessive violence, harmful activities, and negative body image content

**Child Safety Standards** apply to social, dating, anonymous chat, and random chat apps. These apps need:

- [ ] Published standards prohibiting child sexual abuse and exploitation
- [ ] An in-app feedback or reporting mechanism (self-certified in Play Console)
- [ ] Action on child sexual abuse material and reporting to the appropriate authority (self-certified)
- [ ] A named child safety point of contact

Anonymous chat apps may not target children (effective 2026-08-26).

## 1.2 Inappropriate content

- [ ] Sexual content: none, except nudity with educational, documentary, scientific, or artistic purpose. Catalog apps have narrow conditions
- [ ] Hate speech: nothing promoting violence or hatred on protected characteristics, no hate symbols
- [ ] Violence: no gratuitous violence, or content promoting self-harm, suicide, eating disorders, or choking games. Fictional game violence is generally fine
- [ ] Violent extremism, sensitive events, bullying and harassment: none
- [ ] Dangerous products: no sale of, or manufacturing instructions for, explosives, firearms, ammunition, or listed accessories
- [ ] Marijuana: no facilitating sale, ordering, or delivery
- [ ] Tobacco and alcohol: no facilitating nicotine sales, no promotion to minors. Age-gated exceptions exist for grocery delivery and cessation aids
- [ ] Illegal activity: no facilitating illegal drug sales or similar

## 1.3 Age-restricted content and functionality

Apps with these features must use Play Console tools to block minors:

- Real-money gambling
- Core dating or matchmaking
- Random connections with strangers
- Anonymous communication where identity is deliberately hidden

Play Age Signals is the privacy-friendly route for age-appropriate features. Use its data only for that purpose. Google announced its global launch in the 2026-10-29 update.

## 1.4 Financial services

Publish from an Organization account (see [Console and release](7-console-and-release.md#77-account-type)). Complete the Financial features declaration.

- [ ] Binary options: not allowed
- [ ] Personal loans: full repayment in 60 days or less is prohibited
- [ ] US personal loans: APR must be below 36%
- [ ] Loans and Earned Wage Access: Finance category, with repayment terms, maximum APR, a representative cost example, and privacy policy in the metadata
- [ ] Earned Wage Access: no interest, repayment via payroll or autopay, limited transparent fees
- [ ] Loan, credit, and Earned Wage Access apps do not request `READ_EXTERNAL_STORAGE`, `WRITE_EXTERNAL_STORAGE`, `READ_MEDIA_IMAGES`, `READ_MEDIA_VIDEO`, `READ_CONTACTS`, `ACCESS_FINE_LOCATION`, `READ_PHONE_NUMBERS`, or `QUERY_ALL_PACKAGES`
- [ ] Country rules checked: licensing or disclosure duties exist for the US, India, Indonesia, Philippines, Nigeria, Kenya, Pakistan, and Thailand

## 1.5 Gambling, games, and contests

- [ ] Real-money gambling only in approved countries, with an application, a valid local license, a free listing, no Play billing, an adult rating, minors and restricted regions blocked, and responsible gambling information
- [ ] All other real-money games and contests are prohibited
- [ ] Daily Fantasy Sports: US-only or approved as gambling, with the separate application and state licensing
- [ ] Gamified loyalty: game apps use fixed-ratio rewards only. Non-game apps may use chance if official rules and odds are published
- [ ] Gambling ads: meet all conditions in the policy, including no ads to minors and no simulated gambling

## 1.6 User-generated content

Applies whenever users publish anything other users can see.

- [ ] Users accept terms before creating or uploading content
- [ ] Terms define and prohibit objectionable content
- [ ] In-app reporting exists for content **and** blocking exists for users
- [ ] Moderation is real and ongoing, and monetization does not reward objectionable behavior
- [ ] Incidental sexual content sits behind at least two user actions, with children blocked by age screening and the content rating answered accurately

**Evidence:** trace the write path, then find the report and block controls in the UI. A `reportContent()` API with no UI does not satisfy this.

## 1.7 AI-generated content

Applies to apps that generate text, images, audio, or video from prompts. Apps that only summarize a user's own content, or use AI as a hidden implementation detail, need judgment: report this as verify, not a violation.

- [ ] Generation of restricted content is prevented, including child exploitation and deceptive content
- [ ] An in-app report or flag control sits at the generated output
- [ ] Reports feed moderation
- [ ] Third-party AI providers are covered by the app's user data disclosures. The developer stays responsible for them (see [Privacy](2-privacy-and-permissions.md#21-user-data))

## 1.8 Health content and services

- [ ] Health apps declaration completed in Play Console
- [ ] Privacy policy in the Console and in the app
- [ ] No misleading health functionality. Required hardware and device compatibility is disclosed
- [ ] Regulated medical devices are declared, with proof of approval available on request
- [ ] Other health apps carry a disclaimer: not a medical device, does not diagnose, treat, cure, or prevent conditions, consult a professional
- [ ] No prescription drug sales without a prescription, no unapproved substances, ephedra, or hCG for weight loss, no health misinformation
- [ ] Health Connect data is treated as sensitive (see [Permissions](2-privacy-and-permissions.md#26-restricted-permissions))
- [ ] Regulated clinical transactions do not use Play billing

Unverifiable clinical or weight-loss claims in the listing or UI are findings here and under [Deceptive behavior](3-security-and-deception.md#33-deceptive-behavior).

## 1.9 Blockchain content

- [ ] Exchanges and wallets use certified services in regulated jurisdictions. Hong Kong also accepts the Virtual Asset Trading Platform license
- [ ] No on-device cryptomining. Remote mining management is allowed
- [ ] Tokenized digital assets are declared in the Financial features form and marked on in-app products
- [ ] No promotion of earnings from playing or trading
- [ ] NFTs of unknown value are not sold for value and are not used for wagering, unless approved as gambling

## 1.10 Intellectual property

- [ ] No copyrighted art, audio, or book content without rights, and no fan art indistinguishable from the original
- [ ] No confusingly similar trademarks, and no counterfeit goods
- [ ] Written permission available for third-party brand assets
