---
name: families
description: Google Play Families policies, target audience, child-directed data and ads rules
---

# 6. Families

Load this file when the target audience includes under-13s, **or** the listing, art, or wording appeals to children. Google can treat an app as child-directed from its imagery and terminology, whatever the Console says. "Works great for kids" in a listing is enough to raise this.

## 6.1 Target audience

- [ ] Target age groups in Play Console match the app
- [ ] Mixed-age groups are chosen only if the app is truly designed for them
- [ ] Target Audience, Data safety, and IARC answers agree

## 6.2 Requirements

- [ ] Content children can reach is appropriate
- [ ] No webview-only app, and affiliate traffic is not the primary purpose
- [ ] AR content shows a safety warning at launch

**Child-only apps must not:**

- [ ] Transmit Advertising ID, SIM or Build Serial, BSSID, MAC, SSID, IMEI, or IMSI
- [ ] Request `AD_ID` when targeting API 33 or higher
- [ ] Request location or precise location
- [ ] Request the phone number via `TelephonyManager`

Use Companion Device Manager for Bluetooth. APIs and SDKs must be approved for child-directed services.

**Social features** need an in-app online safety reminder, adult controls, and an adult action before personal information can be exchanged.

Comply with COPPA, GDPR, and other applicable law.

## 6.3 Ads in child-directed apps

- [ ] Only Families Self-Certified Ads SDKs
- [ ] No interest-based ads or remarketing
- [ ] Ads are child-appropriate and closeable within 5 seconds where they interfere with use
- [ ] One ad placement per page
