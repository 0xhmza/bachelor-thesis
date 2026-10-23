# D6 — Which preinstalled (native) health apps enter the sample?

- **Status:** proposed (author's choice 2026-10-22; awaiting supervisor). The methodology states this choice.
- **Affects:** Methodology, App Sampling; walkthroughs (Apple Health needs an iPhone); [D1](D01_sample-size.md)
- **Options considered:**
  1. Exclude preinstalled apps and report the gap.
  2. Let them compete in the store ranking. Rejected: they reach users without a download, so rating count understates their exposure, and Apple Health has no store listing.
  3. **Reserve places for the preinstalled health or fitness trackers of the phone vendors with at least 10 % of German mobile use (proposed).**
  4. A fixed list (Apple, Samsung, Huawei, Google). Rejected: no stated reason for the list.
- **Evidence:**
  - Supervisor meeting of 13 October asked how Apple Health, Samsung Health and Huawei Health could be included ([organized notes](../Meeting-Notes/2026-10-13_Supervisor-Meeting_Organized.md)).
  - German mobile vendor shares, September 2026, by mobile page views: Samsung 39.34 %, Apple 27.63 %, Xiaomi 21.4 %, unknown 3.96 %, Huawei 1.54 %, Google 1.46 % ([StatCounter](https://gs.statcounter.com/vendor-market-share/mobile/germany), checked 2026-10-22). Page views are a proxy for the installed base, not sales.
  - Preinstalled trackers of the three vendors above 10 %:
    - Apple: Apple Health (no App Store listing) and Apple Fitness, available to all iPhone users without an Apple Watch since iOS 16 (secondary coverage, e.g. [iPhone in Canada, 6 June 2022](https://www.iphoneincanada.ca/2022/06/06/ios-16-to-bring-the-fitness-app-to-all-iphones-no-apple-watch-needed/); the Apple newsroom release was not found). Apple Fitness also has an App Store listing (3,012 German ratings in the 20 October trial).
    - Samsung: Samsung Health, also listed in both stores ([sampling report](../../output/research/2026-10-11_germany-download-sampling/sampling_report.tex)).
    - Xiaomi: no preinstalled tracker on international software could be identified. "Mi Health" appeared as a system app in a Chinese MIUI beta ([Beebom](https://beebom.com/mi-health-app-miui-beta/amp)); no source confirms it on current global HyperOS phones.
- **Choice (proposed):** Apple Health, Apple Fitness and Samsung Health take three reserved places. If one of them also appears in a store ranking, it moves to this group and the ranked selection continues to 47 (D1, D2). Huawei Health and Google's apps are excluded by the threshold; Xiaomi contributes none.
- **Reason:** Preinstalled apps are present on most German phones without a choice by the user, which is the strongest form of exposure, yet they escape a download- or rating-based ranking. A share threshold makes the selection follow exposure instead of a hand-picked list, and 10 % separates the three large vendors clearly from the rest (next is Huawei at 1.54 %).
- **Would change if:** a preinstalled tracker on Xiaomi's international phones is confirmed (it would add a fourth place, giving 46 + 4); vendor shares cross the threshold; the supervisor prefers to include Huawei Health anyway; Health Connect (Android's system health store) is judged to be a tracker under the D3 definition.
