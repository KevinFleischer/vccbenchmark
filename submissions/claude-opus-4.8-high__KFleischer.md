# VCCB Benchmark Results

Fill in the metadata and the exact prompt you used, then paste each image's model
output into its section. **Run every image in its own fresh session / sub-agent**
(see `README.md` -> *Isolation*).

**Fill in as many images as you can.** Empty sections are simply **skipped**, so
a partial file is valid. If some images are missing, you can re-upload a more
complete copy later: as long as the metadata block is unchanged, it **replaces**
your earlier, less complete submission (already-scored images are not double-
counted). Return the file to the benchmark administrator for evaluation.

```yaml
model: "claude-opus-4.8-high"              # full, unambiguous model id. For local GGUF use the full
                       # Hugging Face path incl. lab/tuner + quant tag, e.g.
                       # "unsloth/gemma-3-27b-it-qat-GGUF:UD-Q4_K_XL"
run_date: "2026-06-30"           # YYYY-MM-DD
submitter: "KFleischer"          # a short tag for your submission, shown on the public
                       # leaderboard: a nickname you are happy to show, or just
                       # 5-6 random letters/digits. Keep it the same when you
                       # re-upload to complete this submission.
server_command: "claude.ai"     # the exact start command of your model server, e.g. the
                       # llama-server / ollama / vLLM command line you used. It
                       # documents quant, context length and sampling in one place.
                       # For a hosted / API model, give the service URL instead.
comments: ""           # optional: anything that helped (observations, tweaks)
runner: ""             # optional: who/what produced these results
```

## Extraction prompt used

Paste the exact prompt text you gave the model between the four-backtick fences
below. It is pre-filled with the shipped prompt; replace it only if you used a
different one.

````text
# Calendar Extraction Prompt

You are given a single image of a calendar **week view** (Monday to Friday).
Your task is to read the calendar and list **every event you can see**, as
structured data.

## What to read

- Read each event's **day**, **start time**, **end time** and **title** (how to
  read the times precisely is in the next section).
- Transcribe each **title as shown**, including any short code at the end. For a
  **recurring** event (the same event appearing on several days), use the **full**
  title — including the end code — taken from a day where it is fully visible, for
  **every** occurrence, even on days where it is cut off. For a **one-off** event
  whose title is genuinely cut off, just write what you can read.
- Events shown in the **strip above the time grid** (the day header band) are
  **all-day events**. They have no clock time.
- If an event shows a **repeat/recurrence indicator**, or the same event clearly
  appears on several days, mark it as recurring.

## How to read the times

Read the times by **measuring each event against the time grid**, not by guessing
a plausible schedule. This is the part models most often get wrong, so work in
this order:

1. **Calibrate.** Find two labelled hour lines on the time axis (for example the
   09:00 and 10:00 marks) and use the gap between the lines as your scale for that
   column.
2. **Use the most precise cue, not just the block outline.** An event's outer
   rectangle is not always exact — an app may pad it or enforce a minimum height,
   so a short event can look taller, and start earlier, than it really is. If the
   event carries a finer indicator — a thin coloured bar or line along one side
   that marks its actual start and end — read the time from **that indicator**,
   not from the outer rectangle. Only when there is no such indicator, use the
   block's **top edge** for the start and its **bottom edge** for the end.
   Interpolate against the calibrated hour lines — not from where neighbouring
   blocks sit, and not from a typical meeting length.
3. **Report what you measured, to the nearest 5 minutes.** Use a round time
   (:00, :15, :30, :45) only when the edge actually lines up with that grid
   position. If the edge sits between the lines, give the off-grid time you
   see (e.g. 08:50, 13:25). Do not round to a neat time out of habit — and
   equally do not invent an off-grid time the image does not support.

Events can begin, end, and last for any number of minutes. Aim for 5-minute
accuracy; a time that is only roughly right is scored as wrong.

## Output format

Output **only** a YAML object with an `events:` list — no explanation, no extra
text. Use 24-hour `HH:MM` times. One list item per visible block.

For a **timed event**:

```yaml
  - title: "<exact title text>"
    day: <Monday|Tuesday|Wednesday|Thursday|Friday>
    start: "HH:MM"
    end: "HH:MM"
    all_day: false
    recurring: <true|false>
```

For an **all-day event** (day header band):

```yaml
  - title: "<exact title text>"
    all_day: true
    start_day: <weekday it begins on>
    span_days: <number of day columns it covers, 1 for a single day>
    recurring: <true|false>
```

## Example (format only — not the real calendar)

```yaml
events:
  - title: "Morning Standup"
    day: Monday
    start: "09:05"
    end: "09:35"
    all_day: false
    recurring: true
  - title: "Quarterly Review"
    day: Tuesday
    start: "13:20"
    end: "14:50"
    all_day: false
    recurring: false
  - title: "Company Offsite"
    all_day: true
    start_day: Wednesday
    span_days: 2
    recurring: false
```

## Rules

- List every visible event. Do not omit events, and do not invent events that
  are not shown.
- Do not merge separate blocks, and do not split a single block.
- Output the YAML object and nothing else.
````

---

## Image A1

```yaml
events:
  - title: "Duration Check Bench34"
    all_day: true
    start_day: Monday
    span_days: 1
    recurring: false
  - title: "Multiple Day Event Bench35"
    all_day: true
    start_day: Wednesday
    span_days: 2
    recurring: false
  - title: "Anchor Flow Bench01"
    day: Monday
    start: "08:00"
    end: "08:45"
    all_day: false
    recurring: false
  - title: "Birch Wave Bench02"
    day: Monday
    start: "09:00"
    end: "09:40"
    all_day: false
    recurring: false
  - title: "Comet Ridge Bench03"
    day: Monday
    start: "10:00"
    end: "10:40"
    all_day: false
    recurring: false
  - title: "Dune Harbor Bench04"
    day: Monday
    start: "11:00"
    end: "11:40"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Monday
    start: "12:30"
    end: "13:00"
    all_day: false
    recurring: true
  - title: "Elm Sector Bench05"
    day: Monday
    start: "13:00"
    end: "13:45"
    all_day: false
    recurring: false
  - title: "Falcon Point Bench06"
    day: Monday
    start: "15:00"
    end: "16:25"
    all_day: false
    recurring: false
  - title: "Glacier Route Bench07"
    day: Monday
    start: "16:30"
    end: "17:30"
    all_day: false
    recurring: false
  - title: "Harbor Crest Bench08"
    day: Tuesday
    start: "08:00"
    end: "09:00"
    all_day: false
    recurring: false
  - title: "Island Grove Bench09"
    day: Tuesday
    start: "09:15"
    end: "10:15"
    all_day: false
    recurring: false
  - title: "Jasper Field Bench10"
    day: Tuesday
    start: "10:30"
    end: "11:30"
    all_day: false
    recurring: false
  - title: "Kestrel Bay Bench11"
    day: Tuesday
    start: "11:45"
    end: "12:35"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Tuesday
    start: "12:30"
    end: "13:00"
    all_day: false
    recurring: true
  - title: "Lantern Peak Bench12"
    day: Tuesday
    start: "14:00"
    end: "15:00"
    all_day: false
    recurring: false
  - title: "Meadow Point Bench13"
    day: Tuesday
    start: "15:05"
    end: "16:20"
    all_day: false
    recurring: false
  - title: "Prairie Stone Bench16"
    day: Wednesday
    start: "09:00"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Orion Gate Bench15"
    day: Wednesday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Nimbus Trai"
    day: Wednesday
    start: "09:00"
    end: "09:30"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Wednesday
    start: "12:30"
    end: "13:00"
    all_day: false
    recurring: true
  - title: "Quartz Harbor Bench17"
    day: Wednesday
    start: "14:00"
    end: "15:40"
    all_day: false
    recurring: false
  - title: "Raven Point Bench18"
    day: Wednesday
    start: "14:30"
    end: "15:20"
    all_day: false
    recurring: false
  - title: "Summit Ridge Bench19"
    day: Wednesday
    start: "15:00"
    end: "16:25"
    all_day: false
    recurring: false
  - title: "Umbra Valley Bench21"
    day: Thursday
    start: "09:00"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Vertex Harbor Bench22"
    day: Thursday
    start: "09:25"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Willow Crossing Bench23"
    day: Thursday
    start: "09:30"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Thursday
    start: "12:30"
    end: "13:00"
    all_day: false
    recurring: true
  - title: "Xenon Bridge Bench24"
    day: Friday
    start: "08:00"
    end: "08:30"
    all_day: false
    recurring: false
  - title: "Yonder Creek Bench25"
    day: Friday
    start: "08:30"
    end: "09:00"
    all_day: false
    recurring: false
  - title: "Zenith Point Bench26"
    day: Friday
    start: "09:00"
    end: "09:30"
    all_day: false
    recurring: false
  - title: "Aspen Harbor Bench27"
    day: Friday
    start: "09:30"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Boulder Ridge Bench28"
    day: Friday
    start: "10:00"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Cascade Gro"
    day: Friday
    start: "10:15"
    end: "10:50"
    all_day: false
    recurring: false
  - title: "Drift Valley Bench30"
    day: Friday
    start: "10:30"
    end: "11:30"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Friday
    start: "12:30"
    end: "13:00"
    all_day: false
    recurring: true
  - title: "Ember Field Bench31"
    day: Friday
    start: "13:30"
    end: "14:00"
    all_day: false
    recurring: false
  - title: "Forest Trail Bench32"
    day: Friday
    start: "14:45"
    end: "15:05"
    all_day: false
    recurring: false
  - title: "Granite Harbor Manufacturing Modernization Review Bench33"
    day: Friday
    start: "15:05"
    end: "17:20"
    all_day: false
    recurring: false
```

## Image A2

```yaml
events:
  - title: "Duration Check Bench34"
    all_day: true
    start_day: Monday
    span_days: 1
    recurring: false
  - title: "Multiple Day Event Bench35"
    all_day: true
    start_day: Wednesday
    span_days: 2
    recurring: false
  - title: "Anchor Flow Bench01"
    day: Monday
    start: "07:45"
    end: "08:30"
    all_day: false
    recurring: false
  - title: "Birch Wave Bench02"
    day: Monday
    start: "08:45"
    end: "09:35"
    all_day: false
    recurring: false
  - title: "Comet Ridge Bench03"
    day: Monday
    start: "09:45"
    end: "10:20"
    all_day: false
    recurring: false
  - title: "Dune Harbor Bench04"
    day: Monday
    start: "10:45"
    end: "11:45"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Monday
    start: "12:00"
    end: "12:30"
    all_day: false
    recurring: true
  - title: "Elm Sector Bench05"
    day: Monday
    start: "12:45"
    end: "13:45"
    all_day: false
    recurring: false
  - title: "Falcon Point Bench06"
    day: Monday
    start: "14:45"
    end: "15:45"
    all_day: false
    recurring: false
  - title: "Glacier Route Bench07"
    day: Monday
    start: "16:15"
    end: "17:15"
    all_day: false
    recurring: false
  - title: "Harbor Crest Bench08"
    day: Tuesday
    start: "07:45"
    end: "09:00"
    all_day: false
    recurring: false
  - title: "Island Grove Bench09"
    day: Tuesday
    start: "09:00"
    end: "09:50"
    all_day: false
    recurring: false
  - title: "Jasper Field Bench10"
    day: Tuesday
    start: "10:10"
    end: "11:20"
    all_day: false
    recurring: false
  - title: "Kestrel Bay Bench11"
    day: Tuesday
    start: "11:30"
    end: "12:25"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Tuesday
    start: "12:00"
    end: "12:30"
    all_day: false
    recurring: true
  - title: "Lantern Peak Bench12"
    day: Tuesday
    start: "13:40"
    end: "14:55"
    all_day: false
    recurring: false
  - title: "Meadow Point Bench13"
    day: Tuesday
    start: "15:00"
    end: "16:15"
    all_day: false
    recurring: false
  - title: "Nimbus Trai"
    day: Wednesday
    start: "08:50"
    end: "09:15"
    all_day: false
    recurring: false
  - title: "Orion Gate Bench15"
    day: Wednesday
    start: "08:50"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Prairie Stone Bench16"
    day: Wednesday
    start: "08:50"
    end: "10:40"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Wednesday
    start: "12:00"
    end: "12:30"
    all_day: false
    recurring: true
  - title: "Quartz Harbor Bench17"
    day: Wednesday
    start: "13:40"
    end: "14:45"
    all_day: false
    recurring: false
  - title: "Raven Point Bench18"
    day: Wednesday
    start: "14:05"
    end: "15:00"
    all_day: false
    recurring: false
  - title: "Summit Ridge Bench19"
    day: Wednesday
    start: "14:45"
    end: "16:05"
    all_day: false
    recurring: false
  - title: "Umbra Valley Bench21"
    day: Thursday
    start: "08:50"
    end: "10:15"
    all_day: false
    recurring: false
  - title: "Vertex Harbor Bench22"
    day: Thursday
    start: "09:00"
    end: "10:15"
    all_day: false
    recurring: false
  - title: "Willow Crossing Bench23"
    day: Thursday
    start: "09:00"
    end: "10:20"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Thursday
    start: "12:00"
    end: "12:30"
    all_day: false
    recurring: true
  - title: "Xenon Bridge Bench24"
    day: Friday
    start: "07:45"
    end: "08:15"
    all_day: false
    recurring: false
  - title: "Yonder Creek Bench25"
    day: Friday
    start: "08:15"
    end: "08:45"
    all_day: false
    recurring: false
  - title: "Zenith Point Bench26"
    day: Friday
    start: "08:45"
    end: "09:15"
    all_day: false
    recurring: false
  - title: "Aspen Harbor Bench27"
    day: Friday
    start: "09:15"
    end: "09:45"
    all_day: false
    recurring: false
  - title: "Boulder Ridge Bench28"
    day: Friday
    start: "09:45"
    end: "10:35"
    all_day: false
    recurring: false
  - title: "Cascade Gro"
    day: Friday
    start: "09:50"
    end: "10:25"
    all_day: false
    recurring: false
  - title: "Drift Valley Bench30"
    day: Friday
    start: "10:15"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Friday
    start: "12:00"
    end: "12:30"
    all_day: false
    recurring: true
  - title: "Ember Field Bench31"
    day: Friday
    start: "13:05"
    end: "13:40"
    all_day: false
    recurring: false
  - title: "Forest Trail Bench32"
    day: Friday
    start: "14:25"
    end: "14:55"
    all_day: false
    recurring: false
  - title: "Granite Harbor Manufacturing Modernization Review Bench33"
    day: Friday
    start: "14:45"
    end: "17:50"
    all_day: false
    recurring: false
```

## Image A3

```yaml
events:
  # ===== Monday 17 Jan 2022 =====
  - title: "Anchor Flow Bench01"
    day: Monday
    start: "08:00"
    end: "08:30"
    all_day: false
    recurring: false
  - title: "Birch Wave Bench02"
    day: Monday
    start: "09:00"
    end: "09:30"
    all_day: false
    recurring: false
  - title: "Comet Ridge Bench03"
    day: Monday
    start: "10:00"
    end: "10:30"
    all_day: false
    recurring: false
  - title: "Dune Harbor Bench04"
    day: Monday
    start: "11:00"
    end: "11:45"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Monday
    start: "12:30"
    end: "13:00"
    all_day: false
    recurring: true
  - title: "Elm Sector Bench05"
    day: Monday
    start: "13:00"
    end: "13:45"
    all_day: false
    recurring: false
  - title: "Falcon Point Bench06"
    day: Monday
    start: "14:55"
    end: "16:00"
    all_day: false
    recurring: false
  - title: "Glacier Route Bench07"
    day: Monday
    start: "16:20"
    end: "17:30"
    all_day: false
    recurring: false

  # ===== Tuesday 18 Jan 2022 =====
  - title: "Harbor Crest Bench08"
    day: Tuesday
    start: "08:00"
    end: "09:00"
    all_day: false
    recurring: false
  - title: "Island Grove Bench09"
    day: Tuesday
    start: "09:15"
    end: "10:15"
    all_day: false
    recurring: false
  - title: "Jasper Field Bench10"
    day: Tuesday
    start: "10:30"
    end: "11:30"
    all_day: false
    recurring: false
  - title: "Kestrel Bay Bench11"
    day: Tuesday
    start: "11:45"
    end: "12:45"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Tuesday
    start: "12:30"
    end: "13:00"
    all_day: false
    recurring: true
  - title: "Lantern Peak Bench12"
    day: Tuesday
    start: "14:00"
    end: "15:00"
    all_day: false
    recurring: false
  - title: "Meadow Point Bench13"
    day: Tuesday
    start: "15:00"
    end: "16:25"
    all_day: false
    recurring: false

  # ===== Wednesday 19 Jan 2022 =====
  - title: "Prairie Stone Bench16"
    day: Wednesday
    start: "09:00"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Orion Gate Bench15"
    day: Wednesday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Nimbus Trail"
    day: Wednesday
    start: "09:00"
    end: "09:30"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Wednesday
    start: "12:30"
    end: "13:00"
    all_day: false
    recurring: true
  - title: "Quartz Harbor Bench17"
    day: Wednesday
    start: "14:00"
    end: "16:00"
    all_day: false
    recurring: false
  - title: "Raven Point Bench18"
    day: Wednesday
    start: "14:45"
    end: "16:50"
    all_day: false
    recurring: false
  - title: "Summit Ridge Bench19"
    day: Wednesday
    start: "15:25"
    end: "16:55"
    all_day: false
    recurring: false

  # ===== Thursday 20 Jan 2022 =====
  - title: "Umbra Valley Bench21"
    day: Thursday
    start: "09:00"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Vertex Harbor Bench22"
    day: Thursday
    start: "09:00"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Willow Crossing Bench23"
    day: Thursday
    start: "09:00"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Thursday
    start: "12:30"
    end: "13:00"
    all_day: false
    recurring: true

  # ===== Friday 21 Jan 2022 =====
  - title: "Xenon Bridge Bench24"
    day: Friday
    start: "08:00"
    end: "08:30"
    all_day: false
    recurring: false
  - title: "Yonder Creek Bench25"
    day: Friday
    start: "08:30"
    end: "09:00"
    all_day: false
    recurring: false
  - title: "Zenith Point Bench26"
    day: Friday
    start: "09:00"
    end: "09:30"
    all_day: false
    recurring: false
  - title: "Aspen Harbor Bench27"
    day: Friday
    start: "09:30"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Boulder Ridge Bench28"
    day: Friday
    start: "10:00"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Cascade Grove Bench29"
    day: Friday
    start: "10:30"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Drift Valley Bench30"
    day: Friday
    start: "11:00"
    end: "11:45"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Friday
    start: "12:30"
    end: "13:00"
    all_day: false
    recurring: true
  - title: "Ember Field Bench31"
    day: Friday
    start: "14:00"
    end: "14:45"
    all_day: false
    recurring: false
  - title: "Forest Trail Bench32"
    day: Friday
    start: "15:30"
    end: "16:00"
    all_day: false
    recurring: false
  - title: "Granite Harbor Manufacturing Modernization Review Bench33"
    day: Friday
    start: "16:00"
    end: "19:00"
    all_day: false
    recurring: false

  # ===== All-day events =====
  - title: "Duration Check Bench34"
    all_day: true
    start_day: Monday
    span_days: 1
    recurring: false
  - title: "Multiple Day Event Bench35"
    all_day: true
    start_day: Wednesday
    span_days: 2
    recurring: false
```

## Image B1

```yaml
events:
  - title: "Duration Check Bench34"
    all_day: true
    start_day: Monday
    span_days: 1
    recurring: false
  - title: "Multiple Day Event Bench35"
    all_day: true
    start_day: Wednesday
    span_days: 2
    recurring: false
  - title: "Anchor Flow Bench01"
    day: Monday
    start: "08:00"
    end: "08:30"
    all_day: false
    recurring: false
  - title: "Birch Wave Bench02"
    day: Monday
    start: "09:00"
    end: "09:30"
    all_day: false
    recurring: false
  - title: "Comet Ridge Bench03"
    day: Monday
    start: "10:00"
    end: "10:30"
    all_day: false
    recurring: false
  - title: "Dune Harbor Bench04"
    day: Monday
    start: "11:00"
    end: "11:30"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Monday
    start: "12:50"
    end: "13:35"
    all_day: false
    recurring: true
  - title: "Elm Sector Bench05"
    day: Monday
    start: "13:05"
    end: "13:50"
    all_day: false
    recurring: false
  - title: "Falcon Point Bench06"
    day: Monday
    start: "15:00"
    end: "16:00"
    all_day: false
    recurring: false
  - title: "Glacier Route Bench07"
    day: Monday
    start: "16:30"
    end: "17:30"
    all_day: false
    recurring: false
  - title: "Harbor Crest Bench08"
    day: Tuesday
    start: "08:20"
    end: "08:50"
    all_day: false
    recurring: false
  - title: "Island Grove Bench09"
    day: Tuesday
    start: "09:20"
    end: "10:15"
    all_day: false
    recurring: false
  - title: "Jasper Field Bench10"
    day: Tuesday
    start: "10:40"
    end: "11:30"
    all_day: false
    recurring: false
  - title: "Kestrel Bay Bench11"
    day: Tuesday
    start: "11:50"
    end: "12:45"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Tuesday
    start: "12:50"
    end: "13:35"
    all_day: false
    recurring: true
  - title: "Lantern Peak Bench12"
    day: Tuesday
    start: "13:55"
    end: "14:50"
    all_day: false
    recurring: false
  - title: "Meadow Point Bench13"
    day: Tuesday
    start: "15:10"
    end: "16:10"
    all_day: false
    recurring: false
  - title: "Nimbus Trail"
    day: Wednesday
    start: "09:00"
    end: "10:40"
    all_day: false
    recurring: false
  - title: "Orion Gate Bench15"
    day: Wednesday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Prairie Stone Bench16"
    day: Wednesday
    start: "09:00"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Wednesday
    start: "12:50"
    end: "13:35"
    all_day: false
    recurring: true
  - title: "Quartz Harbor Bench17"
    day: Wednesday
    start: "14:00"
    end: "16:00"
    all_day: false
    recurring: false
  - title: "Raven Point Bench18"
    day: Wednesday
    start: "14:35"
    end: "15:15"
    all_day: false
    recurring: false
  - title: "Summit Ridge Bench19"
    day: Wednesday
    start: "15:15"
    end: "16:20"
    all_day: false
    recurring: false
  - title: "Umbra Valley Bench21"
    day: Thursday
    start: "09:00"
    end: "10:40"
    all_day: false
    recurring: false
  - title: "Vertex Harbor Bench22"
    day: Thursday
    start: "09:00"
    end: "10:40"
    all_day: false
    recurring: false
  - title: "Willow Crossing Bench23"
    day: Thursday
    start: "09:00"
    end: "10:40"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Thursday
    start: "12:50"
    end: "13:35"
    all_day: false
    recurring: true
  - title: "Xenon Bridge Bench24"
    day: Friday
    start: "08:00"
    end: "08:30"
    all_day: false
    recurring: false
  - title: "Yonder Creek Bench25"
    day: Friday
    start: "08:30"
    end: "09:00"
    all_day: false
    recurring: false
  - title: "Zenith Point Bench26"
    day: Friday
    start: "09:00"
    end: "09:30"
    all_day: false
    recurring: false
  - title: "Aspen Harbor Bench27"
    day: Friday
    start: "09:30"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Boulder Ridge Bench28"
    day: Friday
    start: "10:00"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Cascade"
    day: Friday
    start: "10:20"
    end: "10:50"
    all_day: false
    recurring: false
  - title: "Drift Valley Bench30"
    day: Friday
    start: "10:40"
    end: "11:30"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Friday
    start: "12:50"
    end: "13:35"
    all_day: false
    recurring: true
  - title: "Ember Field Bench31"
    day: Friday
    start: "14:00"
    end: "14:30"
    all_day: false
    recurring: false
  - title: "Forest Trail Bench32"
    day: Friday
    start: "14:50"
    end: "15:15"
    all_day: false
    recurring: false
  - title: "Granite Harbor Manufacturing Modernization Review Bench33"
    day: Friday
    start: "15:15"
    end: "18:00"
    all_day: false
    recurring: false
```

## Image B2

```yaml
events: []
```

## Image B3

```yaml
events: []
```

## Image C1

```yaml
events: []
```

## Image C2

```yaml
events: []
```

## Image C3

```yaml
events: []
```
