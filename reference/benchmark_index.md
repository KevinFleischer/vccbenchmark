# Visual Calendar Comprehension Benchmark (VCCB) — Benchmark Index

Version 0.1.0 · generated from `reference/ground_truth.yaml`. Human-readable reference of every event: canonical values, per-client Recoverable Truth (Extractable Maximum), rationale, and covered phenomena.

> **Reference material — do NOT expose to evaluated models.** This file lives under `reference/` and reveals the answers and the recoverable bands.

- **Week:** Mon 2022-01-17 → Fri 2022-01-21
- **View window:** 08:00-18:00
- **Canonical events:** 35  ·  **Visible blocks:** Outlook 39, Notes 40, Thunderbird 40
- **Recoverable-truth scope:** per_client

## Client capability profiles

| Property | Outlook | HCL Notes | Thunderbird |
|---|---|---|---|
| Calibration | measured | measured | measured |
| px per minute | 1.0 | 0.8 | 1.26 |
| Precise time indicator | yes | no | no |
| Clamp below (min) | 0 | 30 | 20 |
| Clamped base band | — | 5–30 | 5–20 |
| Duration tol base/bonus | ±15/±5 | ±15/±5 | ±15/±5 |
| Start tol base/bonus | ±5/±2 | ±5/±2 | ±5/±2 |
| Multi-day render | span_bar | per_day_banner | per_day_banner |
| Recurrence icon | yes | no | yes |

**How to read recoverable bands.** *Duration:* a prediction inside the base band earns base credit (80%); inside the bonus band earns full credit (100%). *clamped* = no bonus tier (the render cannot expose finer detail). *Start:* base = within ±base tol; bonus = within ±bonus tol; a ✗ bonus is not reachable (clamp can displace the top edge) and is removed from the denominator. Self-normalization means a perfect extraction of any client's image scores 100%.

---

## Bench01 — Anchor Flow Bench01  (timed)

**Canonical**

- Day: Monday (2022-01-17)
- Start: 08:00  ·  End: 08:15  ·  Duration: 15 min
- Recurrence: none

**Title** — content words: *Anchor Flow*  ·  id token: `Bench01`  ·  truncation expected: false

**Recoverable per client**

| Client | Regime | Duration base | Duration bonus | Start base | Start bonus |
|---|---|---|---|---|---|
| Outlook | linear | 0–30 | 10–20 | ±5 | ±2 |
| HCL Notes | clamped | 5–30 | — | ±5 | ±2 |
| Thunderbird | clamped | 5–20 | — | ±5 | ±2 |

**Purpose** — Duration-coverage anchor: smallest readable block (15 min).

**Phenomena** — duration:15, clamped-regime, sparse-morning

---

## Bench02 — Birch Wave Bench02  (timed)

**Canonical**

- Day: Monday (2022-01-17)
- Start: 09:00  ·  End: 09:20  ·  Duration: 20 min
- Recurrence: none

**Title** — content words: *Birch Wave*  ·  id token: `Bench02`  ·  truncation expected: false

**Recoverable per client**

| Client | Regime | Duration base | Duration bonus | Start base | Start bonus |
|---|---|---|---|---|---|
| Outlook | linear | 5–35 | 15–25 | ±5 | ±2 |
| HCL Notes | clamped | 5–30 | — | ±5 | ±2 |
| Thunderbird | clamped | 5–20 | — | ±5 | ±2 |

**Purpose** — Duration coverage 20 min, still inside the clamped class.

**Phenomena** — duration:20, clamped-regime

---

## Bench03 — Comet Ridge Bench03  (timed)

**Canonical**

- Day: Monday (2022-01-17)
- Start: 10:00  ·  End: 10:30  ·  Duration: 30 min
- Recurrence: none

**Title** — content words: *Comet Ridge*  ·  id token: `Bench03`  ·  truncation expected: false

**Recoverable per client**

| Client | Regime | Duration base | Duration bonus | Start base | Start bonus |
|---|---|---|---|---|---|
| Outlook | linear | 15–45 | 25–35 | ±5 | ±2 |
| HCL Notes | clamped | 5–30 | — | ±5 | ±2 |
| Thunderbird | linear | 15–45 | 25–35 | ±5 | ±2 |

**Purpose** — Duration coverage 30 min; measured at the clamp floor, so it is visually indistinguishable from 15/20 min (clamped class).

**Phenomena** — duration:30, clamped-regime

---

## Bench04 — Dune Harbor Bench04  (timed)

**Canonical**

- Day: Monday (2022-01-17)
- Start: 11:00  ·  End: 11:45  ·  Duration: 45 min
- Recurrence: none

**Title** — content words: *Dune Harbor*  ·  id token: `Bench04`  ·  truncation expected: false

**Recoverable per client**

| Client | Regime | Duration base | Duration bonus | Start base | Start bonus |
|---|---|---|---|---|---|
| Outlook | linear | 30–60 | 40–50 | ±5 | ±2 |
| HCL Notes | linear | 30–60 | 40–50 | ±5 | ±2 |
| Thunderbird | linear | 30–60 | 40–50 | ±5 | ±2 |

**Purpose** — Duration coverage 45 min.

**Phenomena** — duration:45, linear-regime

---

## Bench05 — Elm Sector Bench05  (timed)

**Canonical**

- Day: Monday (2022-01-17)
- Start: 13:00  ·  End: 13:55  ·  Duration: 55 min
- Recurrence: none

**Title** — content words: *Elm Sector*  ·  id token: `Bench05`  ·  truncation expected: false

**Recoverable per client**

| Client | Regime | Duration base | Duration bonus | Start base | Start bonus |
|---|---|---|---|---|---|
| Outlook | linear | 40–70 | 50–60 | ±5 | ±2 |
| HCL Notes | linear | 40–70 | 50–60 | ±5 | ±2 |
| Thunderbird | linear | 40–70 | 50–60 | ±5 | ±2 |

**Purpose** — Duration coverage 55 min.

**Phenomena** — duration:55, linear-regime

---

## Bench06 — Falcon Point Bench06  (timed)

**Canonical**

- Day: Monday (2022-01-17)
- Start: 15:00  ·  End: 16:00  ·  Duration: 60 min
- Recurrence: none

**Title** — content words: *Falcon Point*  ·  id token: `Bench06`  ·  truncation expected: false

**Recoverable per client**

| Client | Regime | Duration base | Duration bonus | Start base | Start bonus |
|---|---|---|---|---|---|
| Outlook | linear | 45–75 | 55–65 | ±5 | ±2 |
| HCL Notes | linear | 45–75 | 55–65 | ±5 | ±2 |
| Thunderbird | linear | 45–75 | 55–65 | ±5 | ±2 |

**Purpose** — Duration coverage 60 min, exact one-hour block.

**Phenomena** — duration:60, linear-regime, hour-aligned

---

## Bench07 — Glacier Route Bench07  (timed)

**Canonical**

- Day: Monday (2022-01-17)
- Start: 16:30  ·  End: 17:35  ·  Duration: 65 min
- Recurrence: none

**Title** — content words: *Glacier Route*  ·  id token: `Bench07`  ·  truncation expected: false

**Recoverable per client**

| Client | Regime | Duration base | Duration bonus | Start base | Start bonus |
|---|---|---|---|---|---|
| Outlook | linear | 50–80 | 60–70 | ±5 | ±2 |
| HCL Notes | linear | 50–80 | 60–70 | ±5 | ±2 |
| Thunderbird | linear | 50–80 | 60–70 | ±5 | ±2 |

**Purpose** — Duration coverage 65 min; moved to 16:30 so its end (17:35) stays inside the 18:00 view boundary.

**Phenomena** — duration:65, linear-regime, late-afternoon

---

## Bench08 — Harbor Crest Bench08  (timed)

**Canonical**

- Day: Tuesday (2022-01-18)
- Start: 08:05  ·  End: 09:05  ·  Duration: 60 min
- Recurrence: none

**Title** — content words: *Harbor Crest*  ·  id token: `Bench08`  ·  truncation expected: false

**Recoverable per client**

| Client | Regime | Duration base | Duration bonus | Start base | Start bonus |
|---|---|---|---|---|---|
| Outlook | linear | 45–75 | 55–65 | ±5 | ±2 |
| HCL Notes | linear | 45–75 | 55–65 | ±5 | ±2 |
| Thunderbird | linear | 45–75 | 55–65 | ±5 | ±2 |

**Purpose** — Start-offset :05 with a clean 60-min duration.

**Phenomena** — start-offset::05, duration:60, end::05

---

## Bench09 — Island Grove Bench09  (timed)

**Canonical**

- Day: Tuesday (2022-01-18)
- Start: 09:15  ·  End: 10:15  ·  Duration: 60 min
- Recurrence: none

**Title** — content words: *Island Grove*  ·  id token: `Bench09`  ·  truncation expected: false

**Recoverable per client**

| Client | Regime | Duration base | Duration bonus | Start base | Start bonus |
|---|---|---|---|---|---|
| Outlook | linear | 45–75 | 55–65 | ±5 | ±2 |
| HCL Notes | linear | 45–75 | 55–65 | ±5 | ±2 |
| Thunderbird | linear | 45–75 | 55–65 | ±5 | ±2 |

**Purpose** — Start-offset :15.

**Phenomena** — start-offset::15, duration:60

---

## Bench10 — Jasper Field Bench10  (timed)

**Canonical**

- Day: Tuesday (2022-01-18)
- Start: 10:30  ·  End: 11:30  ·  Duration: 60 min
- Recurrence: none

**Title** — content words: *Jasper Field*  ·  id token: `Bench10`  ·  truncation expected: false

**Recoverable per client**

| Client | Regime | Duration base | Duration bonus | Start base | Start bonus |
|---|---|---|---|---|---|
| Outlook | linear | 45–75 | 55–65 | ±5 | ±2 |
| HCL Notes | linear | 45–75 | 55–65 | ±5 | ±2 |
| Thunderbird | linear | 45–75 | 55–65 | ±5 | ±2 |

**Purpose** — Start-offset :30.

**Phenomena** — start-offset::30, duration:60

---

## Bench11 — Kestrel Bay Bench11  (timed)

**Canonical**

- Day: Tuesday (2022-01-18)
- Start: 11:45  ·  End: 12:45  ·  Duration: 60 min
- Recurrence: none

**Title** — content words: *Kestrel Bay*  ·  id token: `Bench11`  ·  truncation expected: false

**Recoverable per client**

| Client | Regime | Duration base | Duration bonus | Start base | Start bonus |
|---|---|---|---|---|---|
| Outlook | linear | 45–75 | 55–65 | ±5 | ±2 |
| HCL Notes | linear | 45–75 | 55–65 | ±5 | ±2 |
| Thunderbird | linear | 45–75 | 55–65 | ±5 | ±2 |

**Purpose** — Start-offset :45.

**Phenomena** — start-offset::45, duration:60

---

## Bench12 — Lantern Peak Bench12  (timed)

**Canonical**

- Day: Tuesday (2022-01-18)
- Start: 13:55  ·  End: 14:55  ·  Duration: 60 min
- Recurrence: none

**Title** — content words: *Lantern Peak*  ·  id token: `Bench12`  ·  truncation expected: false

**Recoverable per client**

| Client | Regime | Duration base | Duration bonus | Start base | Start bonus |
|---|---|---|---|---|---|
| Outlook | linear | 45–75 | 55–65 | ±5 | ±2 |
| HCL Notes | linear | 45–75 | 55–65 | ±5 | ±2 |
| Thunderbird | linear | 45–75 | 55–65 | ±5 | ±2 |

**Purpose** — Start-offset :55 (cross-hour start at xx:55).

**Phenomena** — start-offset::55, duration:60, cross-hour

---

## Bench13 — Meadow Point Bench13  (timed)

**Canonical**

- Day: Tuesday (2022-01-18)
- Start: 15:05  ·  End: 16:20  ·  Duration: 75 min
- Recurrence: none

**Title** — content words: *Meadow Point*  ·  id token: `Bench13`  ·  truncation expected: false

**Recoverable per client**

| Client | Regime | Duration base | Duration bonus | Start base | Start bonus |
|---|---|---|---|---|---|
| Outlook | linear | 60–90 | 70–80 | ±5 | ±2 |
| HCL Notes | linear | 60–90 | 70–80 | ±5 | ±2 |
| Thunderbird | linear | 60–90 | 70–80 | ±5 | ±2 |

**Purpose** — Start-offset :05 plus 75-min duration coverage.

**Phenomena** — start-offset::05, duration:75, linear-regime

---

## Bench14 — Nimbus Trail Bench14  (timed)

**Canonical**

- Day: Wednesday (2022-01-19)
- Start: 09:00  ·  End: 09:30  ·  Duration: 30 min
- Recurrence: none

**Title** — content words: *Nimbus Trail*  ·  id token: `Bench14`  ·  truncation expected: false

**Recoverable per client**

| Client | Regime | Duration base | Duration bonus | Start base | Start bonus |
|---|---|---|---|---|---|
| Outlook | linear | 15–45 | 25–35 | ±5 | ±2 |
| HCL Notes | clamped | 5–30 | — | ±5 | ±2 |
| Thunderbird | linear | 15–45 | 25–35 | ±5 | ±2 |

**Purpose** — Identical-start overlap (shortest of the 09:00 stack).

**Phenomena** — overlap:identical-start, duration:30

---

## Bench15 — Orion Gate Bench15  (timed)

**Canonical**

- Day: Wednesday (2022-01-19)
- Start: 09:00  ·  End: 10:00  ·  Duration: 60 min
- Recurrence: none

**Title** — content words: *Orion Gate*  ·  id token: `Bench15`  ·  truncation expected: false

**Recoverable per client**

| Client | Regime | Duration base | Duration bonus | Start base | Start bonus |
|---|---|---|---|---|---|
| Outlook | linear | 45–75 | 55–65 | ±5 | ±2 |
| HCL Notes | linear | 45–75 | 55–65 | ±5 | ±2 |
| Thunderbird | linear | 45–75 | 55–65 | ±5 | ±2 |

**Purpose** — Identical-start overlap (middle of the 09:00 stack).

**Phenomena** — overlap:identical-start, duration:60

---

## Bench16 — Prairie Stone Bench16  (timed)

**Canonical**

- Day: Wednesday (2022-01-19)
- Start: 09:00  ·  End: 11:00  ·  Duration: 120 min
- Recurrence: none

**Title** — content words: *Prairie Stone*  ·  id token: `Bench16`  ·  truncation expected: false

**Recoverable per client**

| Client | Regime | Duration base | Duration bonus | Start base | Start bonus |
|---|---|---|---|---|---|
| Outlook | linear | 105–135 | 115–125 | ±5 | ±2 |
| HCL Notes | linear | 105–135 | 115–125 | ±5 | ±2 |
| Thunderbird | linear | 105–135 | 115–125 | ±5 | ±2 |

**Purpose** — Identical-start overlap (longest of the 09:00 stack).

**Phenomena** — overlap:identical-start, duration:120

---

## Bench17 — Quartz Harbor Bench17  (timed)

**Canonical**

- Day: Wednesday (2022-01-19)
- Start: 14:00  ·  End: 16:00  ·  Duration: 120 min
- Recurrence: none

**Title** — content words: *Quartz Harbor*  ·  id token: `Bench17`  ·  truncation expected: false

**Recoverable per client**

| Client | Regime | Duration base | Duration bonus | Start base | Start bonus |
|---|---|---|---|---|---|
| Outlook | linear | 105–135 | 115–125 | ±5 | ±2 |
| HCL Notes | linear | 105–135 | 115–125 | ±5 | ±2 |
| Thunderbird | linear | 105–135 | 115–125 | ±5 | ±2 |

**Purpose** — Offset overlap container (120 min) spanning two shorter events.

**Phenomena** — overlap:offset, duration:120

---

## Bench18 — Raven Point Bench18  (timed)

**Canonical**

- Day: Wednesday (2022-01-19)
- Start: 14:30  ·  End: 15:15  ·  Duration: 45 min
- Recurrence: none

**Title** — content words: *Raven Point*  ·  id token: `Bench18`  ·  truncation expected: false

**Recoverable per client**

| Client | Regime | Duration base | Duration bonus | Start base | Start bonus |
|---|---|---|---|---|---|
| Outlook | linear | 30–60 | 40–50 | ±5 | ±2 |
| HCL Notes | linear | 30–60 | 40–50 | ±5 | ±2 |
| Thunderbird | linear | 30–60 | 40–50 | ±5 | ±2 |

**Purpose** — Offset overlap, short block nested inside the container.

**Phenomena** — overlap:offset, duration:45

---

## Bench19 — Summit Ridge Bench19  (timed)

**Canonical**

- Day: Wednesday (2022-01-19)
- Start: 15:00  ·  End: 16:30  ·  Duration: 90 min
- Recurrence: none

**Title** — content words: *Summit Ridge*  ·  id token: `Bench19`  ·  truncation expected: false

**Recoverable per client**

| Client | Regime | Duration base | Duration bonus | Start base | Start bonus |
|---|---|---|---|---|---|
| Outlook | linear | 75–105 | 85–95 | ±5 | ±2 |
| HCL Notes | linear | 75–105 | 85–95 | ±5 | ±2 |
| Thunderbird | linear | 75–105 | 85–95 | ±5 | ±2 |

**Purpose** — Offset overlap, 90-min block crossing the container's end.

**Phenomena** — overlap:offset, duration:90

---

## Bench20 — Tanner Grove Bench20  (timed)

**Canonical**

- Day: recurring ['MO', 'TU', 'WE', 'TH', 'FR']
- Start: 12:45  ·  End: 13:00  ·  Duration: 15 min
- Recurrence: WEEKLY on MO,TU,WE,TH,FR, count 5 (instances 2022-01-17 … 2022-01-21)

**Title** — content words: *Tanner Grove*  ·  id token: `Bench20`  ·  truncation expected: false

**Recoverable per client**

| Client | Regime | Duration base | Duration bonus | Start base | Start bonus |
|---|---|---|---|---|---|
| Outlook | linear | 0–30 | 10–20 | ±5 | ±2 |
| HCL Notes | clamped | 5–30 | — | ±5 | ±2 |
| Thunderbird | clamped | 5–20 | — | ±5 | ±2 |

**Purpose** — Recurring event Mon-Fri in a collision-free slot; drives the recurrence-recognition component.

**Phenomena** — recurrence, duration:15, clamped-regime

---

## Bench21 — Umbra Valley Bench21  (timed)

**Canonical**

- Day: Thursday (2022-01-20)
- Start: 09:00  ·  End: 11:00  ·  Duration: 120 min
- Recurrence: none

**Title** — content words: *Umbra Valley*  ·  id token: `Bench21`  ·  truncation expected: false

**Recoverable per client**

| Client | Regime | Duration base | Duration bonus | Start base | Start bonus |
|---|---|---|---|---|---|
| Outlook | linear | 105–135 | 115–125 | ±5 | ±2 |
| HCL Notes | linear | 105–135 | 115–125 | ±5 | ±2 |
| Thunderbird | linear | 105–135 | 115–125 | ±5 | ±2 |

**Purpose** — Horizontal-compression block (full 120 min).

**Phenomena** — compression, duration:120, overlap:offset

---

## Bench22 — Vertex Harbor Bench22  (timed)

**Canonical**

- Day: Thursday (2022-01-20)
- Start: 09:05  ·  End: 10:55  ·  Duration: 110 min
- Recurrence: none

**Title** — content words: *Vertex Harbor*  ·  id token: `Bench22`  ·  truncation expected: false

**Recoverable per client**

| Client | Regime | Duration base | Duration bonus | Start base | Start bonus |
|---|---|---|---|---|---|
| Outlook | linear | 95–125 | 105–115 | ±5 | ±2 |
| HCL Notes | linear | 95–125 | 105–115 | ±5 | ±2 |
| Thunderbird | linear | 95–125 | 105–115 | ±5 | ±2 |

**Purpose** — Horizontal-compression block (110 min), :05 start.

**Phenomena** — compression, duration:110, start-offset::05

---

## Bench23 — Willow Crossing Bench23  (timed)

**Canonical**

- Day: Thursday (2022-01-20)
- Start: 09:10  ·  End: 11:05  ·  Duration: 115 min
- Recurrence: none

**Title** — content words: *Willow Crossing*  ·  id token: `Bench23`  ·  truncation expected: false

**Recoverable per client**

| Client | Regime | Duration base | Duration bonus | Start base | Start bonus |
|---|---|---|---|---|---|
| Outlook | linear | 100–130 | 110–120 | ±5 | ±2 |
| HCL Notes | linear | 100–130 | 110–120 | ±5 | ±2 |
| Thunderbird | linear | 100–130 | 110–120 | ±5 | ±2 |

**Purpose** — Horizontal-compression block (115 min), :10 start, :05 end.

**Phenomena** — compression, duration:115, end::05

---

## Bench24 — Xenon Bridge Bench24  (timed)

**Canonical**

- Day: Friday (2022-01-21)
- Start: 08:00  ·  End: 08:30  ·  Duration: 30 min
- Recurrence: none

**Title** — content words: *Xenon Bridge*  ·  id token: `Bench24`  ·  truncation expected: false

**Recoverable per client**

| Client | Regime | Duration base | Duration bonus | Start base | Start bonus |
|---|---|---|---|---|---|
| Outlook | linear | 15–45 | 25–35 | ±5 | ±2 |
| HCL Notes | clamped | 5–30 | — | ±5 | ±2 |
| Thunderbird | linear | 15–45 | 25–35 | ±5 | ±2 |

**Purpose** — Back-to-back chain, slot 1.

**Phenomena** — back-to-back, duration:30

---

## Bench25 — Yonder Creek Bench25  (timed)

**Canonical**

- Day: Friday (2022-01-21)
- Start: 08:30  ·  End: 09:00  ·  Duration: 30 min
- Recurrence: none

**Title** — content words: *Yonder Creek*  ·  id token: `Bench25`  ·  truncation expected: false

**Recoverable per client**

| Client | Regime | Duration base | Duration bonus | Start base | Start bonus |
|---|---|---|---|---|---|
| Outlook | linear | 15–45 | 25–35 | ±5 | ±2 |
| HCL Notes | clamped | 5–30 | — | ±5 | ±2 |
| Thunderbird | linear | 15–45 | 25–35 | ±5 | ±2 |

**Purpose** — Back-to-back chain, slot 2.

**Phenomena** — back-to-back, duration:30

---

## Bench26 — Zenith Point Bench26  (timed)

**Canonical**

- Day: Friday (2022-01-21)
- Start: 09:00  ·  End: 09:30  ·  Duration: 30 min
- Recurrence: none

**Title** — content words: *Zenith Point*  ·  id token: `Bench26`  ·  truncation expected: false

**Recoverable per client**

| Client | Regime | Duration base | Duration bonus | Start base | Start bonus |
|---|---|---|---|---|---|
| Outlook | linear | 15–45 | 25–35 | ±5 | ±2 |
| HCL Notes | clamped | 5–30 | — | ±5 | ±2 |
| Thunderbird | linear | 15–45 | 25–35 | ±5 | ±2 |

**Purpose** — Back-to-back chain, slot 3.

**Phenomena** — back-to-back, duration:30

---

## Bench27 — Aspen Harbor Bench27  (timed)

**Canonical**

- Day: Friday (2022-01-21)
- Start: 09:30  ·  End: 10:00  ·  Duration: 30 min
- Recurrence: none

**Title** — content words: *Aspen Harbor*  ·  id token: `Bench27`  ·  truncation expected: false

**Recoverable per client**

| Client | Regime | Duration base | Duration bonus | Start base | Start bonus |
|---|---|---|---|---|---|
| Outlook | linear | 15–45 | 25–35 | ±5 | ±2 |
| HCL Notes | clamped | 5–30 | — | ±5 | ±2 |
| Thunderbird | linear | 15–45 | 25–35 | ±5 | ±2 |

**Purpose** — Back-to-back chain, slot 4.

**Phenomena** — back-to-back, duration:30

---

## Bench28 — Boulder Ridge Bench28  (timed)

**Canonical**

- Day: Friday (2022-01-21)
- Start: 10:00  ·  End: 11:00  ·  Duration: 60 min
- Recurrence: none

**Title** — content words: *Boulder Ridge*  ·  id token: `Bench28`  ·  truncation expected: false

**Recoverable per client**

| Client | Regime | Duration base | Duration bonus | Start base | Start bonus |
|---|---|---|---|---|---|
| Outlook | linear | 45–75 | 55–65 | ±5 | ±2 |
| HCL Notes | linear | 45–75 | 55–65 | ±5 | ±2 |
| Thunderbird | linear | 45–75 | 55–65 | ±5 | ±2 |

**Purpose** — Dense overlap container (60 min).

**Phenomena** — overlap:offset, dense-layout, duration:60

---

## Bench29 — Cascade Grove Bench29  (timed)

**Canonical**

- Day: Friday (2022-01-21)
- Start: 10:15  ·  End: 10:45  ·  Duration: 30 min
- Recurrence: none

**Title** — content words: *Cascade Grove*  ·  id token: `Bench29`  ·  truncation expected: false

**Recoverable per client**

| Client | Regime | Duration base | Duration bonus | Start base | Start bonus |
|---|---|---|---|---|---|
| Outlook | linear | 15–45 | 25–35 | ±5 | ±2 |
| HCL Notes | clamped | 5–30 | — | ±5 | ±2 |
| Thunderbird | linear | 15–45 | 25–35 | ±5 | ±2 |

**Purpose** — Dense overlap, short nested block (30 min).

**Phenomena** — overlap:offset, dense-layout, duration:30

---

## Bench30 — Drift Valley Bench30  (timed)

**Canonical**

- Day: Friday (2022-01-21)
- Start: 10:30  ·  End: 11:30  ·  Duration: 60 min
- Recurrence: none

**Title** — content words: *Drift Valley*  ·  id token: `Bench30`  ·  truncation expected: false

**Recoverable per client**

| Client | Regime | Duration base | Duration bonus | Start base | Start bonus |
|---|---|---|---|---|---|
| Outlook | linear | 45–75 | 55–65 | ±5 | ±2 |
| HCL Notes | linear | 45–75 | 55–65 | ±5 | ±2 |
| Thunderbird | linear | 45–75 | 55–65 | ±5 | ±2 |

**Purpose** — Dense overlap, 60-min block crossing the container's end.

**Phenomena** — overlap:offset, dense-layout, duration:60

---

## Bench31 — Ember Field Bench31  (timed)

**Canonical**

- Day: Friday (2022-01-21)
- Start: 13:55  ·  End: 14:05  ·  Duration: 10 min
- Recurrence: none

**Title** — content words: *Ember Field*  ·  id token: `Bench31`  ·  truncation expected: false

**Recoverable per client**

| Client | Regime | Duration base | Duration bonus | Start base | Start bonus |
|---|---|---|---|---|---|
| Outlook | linear | -5–25 | 5–15 | ±5 | ±2 |
| HCL Notes | clamped | 5–30 | — | ±5 | ±2 |
| Thunderbird | clamped | 5–20 | — | ±5 | ±2 |

**Purpose** — Cross-hour boundary case, 10-min clamped block (13:55-14:05).

**Phenomena** — cross-hour, duration:10, clamped-regime, end::05

---

## Bench32 — Forest Trail Bench32  (timed)

**Canonical**

- Day: Friday (2022-01-21)
- Start: 14:45  ·  End: 15:15  ·  Duration: 30 min
- Recurrence: none

**Title** — content words: *Forest Trail*  ·  id token: `Bench32`  ·  truncation expected: false

**Recoverable per client**

| Client | Regime | Duration base | Duration bonus | Start base | Start bonus |
|---|---|---|---|---|---|
| Outlook | linear | 15–45 | 25–35 | ±5 | ±2 |
| HCL Notes | clamped | 5–30 | — | ±5 | ±2 |
| Thunderbird | linear | 15–45 | 25–35 | ±5 | ±2 |

**Purpose** — Cross-hour boundary case, 30-min block (14:45-15:15).

**Phenomena** — cross-hour, duration:30

---

## Bench33 — Granite Harbor Manufacturing Modernization Review Bench33  (timed)

**Canonical**

- Day: Friday (2022-01-21)
- Start: 15:05  ·  End: 17:55  ·  Duration: 170 min
- Recurrence: none

**Title** — content words: *Granite Harbor Manufacturing Modernization Review*  ·  id token: `Bench33`  ·  truncation expected: false

**Recoverable per client**

| Client | Regime | Duration base | Duration bonus | Start base | Start bonus |
|---|---|---|---|---|---|
| Outlook | linear | 155–185 | 165–175 | ±5 | ±2 |
| HCL Notes | linear | 155–185 | 165–175 | ±5 | ±2 |
| Thunderbird | linear | 155–185 | 165–175 | ±5 | ±2 |

**Purpose** — Multi-hour duration (170 min). Long title: in a tall single block it wraps and stays fully readable (measured) -- real truncation is exercised by the compressed overlap events.

**Phenomena** — duration:170, cross-hour, long-title-wrap

---

## Bench34 — Duration Check Bench34  (all-day)

**Canonical**

- Day(s): Monday → +0 (span 1 days, 2022-01-17 … 2022-01-17)
- All-day event (header band; no clock time)

**Title** — content words: *Duration Check*  ·  id token: `Bench34`  ·  truncation expected: false

**Recoverable per client**

| Client | Render | Start-day | Span | Accepted span forms |
|---|---|---|---|---|
| Outlook | span_bar | Monday (exact) | 1 day(s) (exact) | single-day banner |
| HCL Notes | per_day_banner | Monday (exact) | 1 day(s) (exact) | single-day banner |
| Thunderbird | per_day_banner | Monday (exact) | 1 day(s) (exact) | single-day banner |

**Purpose** — All-day single-day event in the Monday header band; tests the all-day vs timed distinction (model must not invent a clock time).

**Phenomena** — all-day, single-day, day-header

---

## Bench35 — Multiple Day Event Bench35  (all-day)

**Canonical**

- Day(s): Wednesday → +1 (span 2 days, 2022-01-19 … 2022-01-20)
- All-day event (header band; no clock time)

**Title** — content words: *Multiple Day Event*  ·  id token: `Bench35`  ·  truncation expected: false

**Recoverable per client**

| Client | Render | Start-day | Span | Accepted span forms |
|---|---|---|---|---|
| Outlook | span_bar | Wednesday (exact) | 2 day(s) (exact) | one span bar |
| HCL Notes | per_day_banner | Wednesday (exact) | 2 day(s) (exact) | one 2-day event OR 2 adjacent same-title banners |
| Thunderbird | per_day_banner | Wednesday (exact) | 2 day(s) (exact) | one 2-day event OR 2 adjacent same-title banners |

**Purpose** — All-day event spanning Wed-Thu; tests multi-day span recognition as a single event across two day columns.

**Phenomena** — all-day, multi-day-span, day-header

---

## Covered phenomena (summary)

| Phenomenon | Events |
|---|---|
| all-day | Bench34, Bench35 |
| back-to-back | Bench24, Bench25, Bench26, Bench27 |
| clamped-regime | Bench01, Bench02, Bench03, Bench20, Bench31 |
| compression | Bench21, Bench22, Bench23 |
| cross-hour | Bench12, Bench31, Bench32, Bench33 |
| day-header | Bench34, Bench35 |
| dense-layout | Bench28, Bench29, Bench30 |
| duration:10 | Bench31 |
| duration:110 | Bench22 |
| duration:115 | Bench23 |
| duration:120 | Bench16, Bench17, Bench21 |
| duration:15 | Bench01, Bench20 |
| duration:170 | Bench33 |
| duration:20 | Bench02 |
| duration:30 | Bench03, Bench14, Bench24, Bench25, Bench26, Bench27, Bench29, Bench32 |
| duration:45 | Bench04, Bench18 |
| duration:55 | Bench05 |
| duration:60 | Bench06, Bench08, Bench09, Bench10, Bench11, Bench12, Bench15, Bench28, Bench30 |
| duration:65 | Bench07 |
| duration:75 | Bench13 |
| duration:90 | Bench19 |
| end::05 | Bench08, Bench23, Bench31 |
| hour-aligned | Bench06 |
| late-afternoon | Bench07 |
| linear-regime | Bench04, Bench05, Bench06, Bench07, Bench13 |
| long-title-wrap | Bench33 |
| multi-day-span | Bench35 |
| overlap:identical-start | Bench14, Bench15, Bench16 |
| overlap:offset | Bench17, Bench18, Bench19, Bench21, Bench28, Bench29, Bench30 |
| recurrence | Bench20 |
| single-day | Bench34 |
| sparse-morning | Bench01 |
| start-offset::05 | Bench08, Bench13, Bench22 |
| start-offset::15 | Bench09 |
| start-offset::30 | Bench10 |
| start-offset::45 | Bench11 |
| start-offset::55 | Bench12 |

