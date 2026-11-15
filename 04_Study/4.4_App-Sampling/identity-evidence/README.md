# Evidence for the identity register

Archived on 28 October 2026 for the decisions in [`../identity.csv`](../identity.csv)
(rule I1–I5 in [D2](../../../00_Notes/Archive/Decisions/D02_ranking-and-rating-floor.md)).
Every other decision rests on the listing fields of the frozen collections in
`05_Data/App Sampling/26. Oct/Raw/`.

| File | Content | Used for |
|---|---|---|
| `web_akrura.ltd_2026-10-28.html` | AKRURA product page; links App Store id1609021075 and Google Play `heartratemonitor.heartrate.pulse.pulseapp` | Herzfrequenzmesser - Puls |
| `web_heartrate.deepthought.industries_2026-10-28.html` | Play developer website of the same app; links only the Play listing | Herzfrequenzmesser - Puls |
| `web_komorebi-studio.com_2026-10-28.html` | Komorebi app list; links id1573133915 and `com.komorebi.roulette` | Roulette + |
| `web_macropinch.com_cardiograph_2026-10-28.html` | Cardiograph page; links id1073907652 and `com.macropinch.hydra.android`; Classic is separate | Kardiograph |
| `web_simpledesign.ltd_2026-10-28.html` | Simple Design: Period Tracker, Lose Weight in 30 Days, Step Counter Free with their Play links | Simple Design / ABISHKKING |
| `web_abishkking.com_2026-10-28.html` | ABISHKKING: the same three products with App Store links 896501514, 1266612768, 1286965867 | Simple Design / ABISHKKING |
| `web_leap.app_2026-10-28.html`, `web_fasting.leap.app_2026-10-28.html` | Leap Fitness pages; Google Play links only | Leap Fitness (no store link to the App Store) |
| `web_ito-technologies.com_2026-10-28.html` | ITO Technologies; links id1027151285 and `com.tayu.tau.pedometer` | Schrittzähler & Pedometer |
| `web_ladytimer.com_iphone_eisprungkalender_2026-10-28.html`, `web_ladytimer.com_android_2026-10-28.html` | Ladytimer ovulation calendar: id406762826 and `com.ladytimer.ovulationcalendar` | Ladytimer |
| `apple-lookup-us_leap_2026-10-28.json`, `apple-lookup-us_abishkking_2026-10-28.json`, `apple-lookup-us_text-pairs_2026-10-28.json`, `apple-lookup-us_selected_2026-10-28.json` | Apple lookup API, US storefront: English store names, bundle IDs, sellers | `en-name` evidence |
| `play-titles-en_2026-10-28.json` | English titles of 46 Google Play product pages (`hl=en`, `gl=us`); full pages not kept | `en-name` evidence |

Pages were read with `curl` (user agent `Mozilla/5.0`) and saved unchanged.
