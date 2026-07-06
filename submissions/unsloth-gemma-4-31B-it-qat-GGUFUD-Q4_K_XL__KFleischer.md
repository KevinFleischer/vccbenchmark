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
model: "unsloth/gemma-4-31B-it-qat-GGUFUD:Q4_K_XL"              # full, unambiguous model id. For local GGUF use the full
                       # Hugging Face path incl. lab/tuner + quant tag, e.g.
                       # "unsloth/gemma-3-27b-it-qat-GGUF:UD-Q4_K_XL"
run_date: "2026-06-30"           # YYYY-MM-DD
submitter: "KFleischer"          # a short tag for your submission, shown on the public
                       # leaderboard: a nickname you are happy to show, or just
                       # 5-6 random letters/digits. Keep it the same when you
                       # re-upload to complete this submission.
server_command: '.\llama-server.exe -hf unsloth/gemma-4-31B-it-qat-GGUF:UD-Q4_K_XL --device Vulkan0 --fit off -ngl 999 -fa on --ctx-size 180000 -np 2 --cache-type-k q8_0 --cache-type-v q8_0 --cache-ram 0 --ctx-checkpoints 0 --no-context-shift --batch-size 256 --ubatch-size 512 --jinja --reasoning off --temp 1.0 --top-p 0.95 --top-k 64 --repeat-penalty 1.0 --port 8080 --host 127.0.0.1'     # the exact start command of your model server, e.g. the
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
    start: "07:30"
    end: "08:15"
    all_day: false
    recurring: false
  - title: "Birch Wave Bench02"
    day: Monday
    start: "08:15"
    end: "09:15"
    all_day: false
    recurring: false
  - title: "Comet Ridge Bench03"
    day: Monday
    start: "09:15"
    end: "10:30"
    all_day: false
    recurring: false
  - title: "Dune Harbor Bench04"
    day: Monday
    start: "10:30"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Monday
    start: "12:00"
    end: "12:45"
    all_day: false
    recurring: true
  - title: "Elm Sector Bench05"
    day: Monday
    start: "12:45"
    end: "13:30"
    all_day: false
    recurring: false
  - title: "Falcon Point Bench06"
    day: Monday
    start: "13:30"
    end: "15:15"
    all_day: false
    recurring: false
  - title: "Glacier Route Bench07"
    day: Monday
    start: "15:15"
    end: "17:00"
    all_day: false
    recurring: false
  - title: "Harbor Crest Bench08"
    day: Tuesday
    start: "07:30"
    end: "08:45"
    all_day: false
    recurring: false
  - title: "Island Grove Bench09"
    day: Tuesday
    start: "08:45"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Jasper Field Bench10"
    day: Tuesday
    start: "10:00"
    end: "11:30"
    all_day: false
    recurring: false
  - title: "Kestrel Bay Bench11"
    day: Tuesday
    start: "11:30"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Tuesday
    start: "12:00"
    end: "12:45"
    all_day: false
    recurring: true
  - title: "Lantern Peak Bench12"
    day: Tuesday
    start: "12:45"
    end: "14:00"
    all_day: false
    recurring: false
  - title: "Meadow Point Bench13"
    day: Tuesday
    start: "14:00"
    end: "15:45"
    all_day: false
    recurring: false
  - title: "Prairie Stone Bench16"
    day: Wednesday
    start: "08:15"
    end: "10:15"
    all_day: false
    recurring: false
  - title: "Orion Gate Bench15"
    day: Wednesday
    start: "08:15"
    end: "09:30"
    all_day: false
    recurring: false
  - title: "Nimbus Trai"
    day: Wednesday
    start: "08:15"
    end: "09:30"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Wednesday
    start: "12:00"
    end: "12:45"
    all_day: false
    recurring: true
  - title: "Quartz Harbor Bench17"
    day: Wednesday
    start: "13:30"
    end: "14:45"
    all_day: false
    recurring: false
  - title: "Raven Point Bench18"
    day: Wednesday
    start: "14:00"
    end: "15:15"
    all_day: false
    recurring: false
  - title: "Summit Ridge Bench19"
    day: Wednesday
    start: "15:00"
    end: "16:15"
    all_day: false
    recurring: false
  - title: "Umbra Valley Bench21"
    day: Thursday
    start: "08:15"
    end: "09:45"
    all_day: false
    recurring: false
  - title: "Vortex Harbor Bench22"
    day: Thursday
    start: "08:15"
    end: "09:45"
    all_day: false
    recurring: false
  - title: "Willow Crossing Bench23"
    day: Thursday
    start: "08:15"
    end: "09:45"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Thursday
    start: "12:00"
    end: "12:45"
    all_day: false
    recurring: true
  - title: "Xenon Bridge Bench24"
    day: Friday
    start: "07:30"
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
    end: "10:15"
    all_day: false
    recurring: false
  - title: "Boulder Ridge Bench28"
    day: Friday
    start: "10:15"
    end: "11:15"
    all_day: false
    recurring: false
  - title: "Cascade Gro"
    day: Friday
    start: "10:15"
    end: "11:15"
    all_day: false
    recurring: false
  - title: "Drift Valley Bench30"
    day: Friday
    start: "11:15"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Friday
    start: "12:00"
    end: "12:45"
    all_day: false
    recurring: true
  - title: "Ember Field Bench31"
    day: Friday
    start: "12:45"
    end: "13:30"
    all_day: false
    recurring: false
  - title: "Forest Trail Bench32"
    day: Friday
    start: "13:30"
    end: "15:15"
    all_day: false
    recurring: false
  - title: "Granite Harbor Manufacturing Modernization Review Bench33"
    day: Friday
    start: "15:15"
    end: "16:30"
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
    start: "07:30"
    end: "08:30"
    all_day: false
    recurring: false
  - title: "Birch Wave Bench02"
    day: Monday
    start: "08:30"
    end: "09:30"
    all_day: false
    recurring: false
  - title: "Comet Ridge Bench03"
    day: Monday
    start: "09:30"
    end: "10:30"
    all_day: false
    recurring: false
  - title: "Dune Harbor Bench04"
    day: Monday
    start: "10:30"
    end: "11:30"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Monday
    start: "12:00"
    end: "13:00"
    all_day: false
    recurring: true
  - title: "Elm Sector Bench05"
    day: Monday
    start: "13:00"
    end: "14:00"
    all_day: false
    recurring: false
  - title: "Falcon Point Bench06"
    day: Monday
    start: "14:30"
    end: "15:30"
    all_day: false
    recurring: false
  - title: "Glacier Route Bench07"
    day: Monday
    start: "16:00"
    end: "17:00"
    all_day: false
    recurring: false
  - title: "Harbor Crest Bench08"
    day: Tuesday
    start: "07:30"
    end: "08:30"
    all_day: false
    recurring: false
  - title: "Island Grove Bench09"
    day: Tuesday
    start: "08:30"
    end: "09:30"
    all_day: false
    recurring: false
  - title: "Jasper Field Bench10"
    day: Tuesday
    start: "09:30"
    end: "11:30"
    all_day: false
    recurring: false
  - title: "Kestrel Bay Bench11"
    day: Tuesday
    start: "11:30"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Tuesday
    start: "12:00"
    end: "13:00"
    all_day: false
    recurring: true
  - title: "Lantern Peak Bench12"
    day: Tuesday
    start: "13:30"
    end: "14:30"
    all_day: false
    recurring: false
  - title: "Meadow Point Bench13"
    day: Tuesday
    start: "14:30"
    end: "15:30"
    all_day: false
    recurring: false
  - title: "Prairie Stone Bench16"
    day: Wednesday
    start: "08:30"
    end: "11:30"
    all_day: false
    recurring: false
  - title: "Orion Gate Bench15"
    day: Wednesday
    start: "08:30"
    end: "11:30"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Wednesday
    start: "12:00"
    end: "13:00"
    all_day: false
    recurring: true
  - title: "Quartze Harbor Bench17"
    day: Wednesday
    start: "13:30"
    end: "15:00"
    all_day: false
    recurring: false
  - title: "Raven Point Bench18"
    day: Wednesday
    start: "14:00"
    end: "15:30"
    all_day: false
    recurring: false
  - title: "Nimbus Trail"
    day: Thursday
    start: "08:30"
    end: "11:30"
    all_day: false
    recurring: false
  - title: "Umbres Valley Bench21"
    day: Thursday
    start: "08:30"
    end: "11:30"
    all_day: false
    recurring: false
  - title: "Vertex Harbor Bench22"
    day: Thursday
    start: "08:30"
    end: "11:30"
    all_day: false
    recurring: false
  - title: "Willow Crossing Bench23"
    day: Thursday
    start: "08:30"
    end: "11:30"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Thursday
    start: "12:00"
    end: "13:00"
    all_day: false
    recurring: true
  - title: "Summit Ridge Bench19"
    day: Thursday
    start: "14:30"
    end: "15:30"
    all_day: false
    recurring: false
  - title: "Xenon Bridge Bench24"
    day: Friday
    start: "07:30"
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
    start: "10:00"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Drift Valley Bench30"
    day: Friday
    start: "10:00"
    end: "11:30"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Friday
    start: "12:00"
    end: "13:00"
    all_day: false
    recurring: true
  - title: "Ember Field Bench31"
    day: Friday
    start: "13:00"
    end: "14:30"
    all_day: false
    recurring: false
  - title: "Forest Trail Bench32"
    day: Friday
    start: "14:30"
    end: "16:00"
    all_day: false
    recurring: false
  - title: "Granite Harbor Manufacturing Modernization Review Bench33"
    day: Friday
    start: "15:00"
    end: "17:00"
    all_day: false
    recurring: false
```

## Image A3

```yaml
events:
  - title: "Parallel Cloud Bench21"
    all_day: true
    start_day: Monday
    span_days: 1
    recurring: false
  - title: "Multiple Day Event Bench33"
    all_day: true
    start_day: Wednesday
    span_days: 3
    recurring: false
  - title: "Anchor Flow Bench01"
    day: Monday
    start: "08:00"
    end: "09:00"
    all_day: false
    recurring: false
  - title: "Beach Wave Bench02"
    day: Monday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Camel Ridge Bench03"
    day: Monday
    start: "10:00"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Dune-Halter Bench04"
    day: Monday
    start: "11:00"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Monday
    start: "12:00"
    end: "13:00"
    all_day: false
    recurring: true
  - title: "Erin Senior Bench12"
    day: Monday
    start: "13:00"
    end: "14:00"
    all_day: false
    recurring: false
  - title: "Falcon Point Bench04"
    day: Monday
    start: "14:00"
    end: "15:00"
    all_day: false
    recurring: false
  - title: "Glacier State Bench07"
    day: Monday
    start: "15:00"
    end: "16:00"
    all_day: false
    recurring: false
  - title: "Harbor Crest Bench02"
    day: Tuesday
    start: "08:00"
    end: "09:00"
    all_day: false
    recurring: false
  - title: "Island Grove Bench11"
    day: Tuesday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Jasper Falls Bench10"
    day: Tuesday
    start: "10:00"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Kestrel Bay Bench11"
    day: Tuesday
    start: "11:00"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Lantern Peak Bench13"
    day: Tuesday
    start: "13:00"
    end: "14:00"
    all_day: false
    recurring: false
  - title: "Meadow Point Bench11"
    day: Tuesday
    start: "14:00"
    end: "15:00"
    all_day: false
    recurring: false
  - title: "Prairie Dove Bench16"
    day: Wednesday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Orion Star Bench11"
    day: Wednesday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Nimbus Trail Bench11"
    day: Wednesday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Wednesday
    start: "12:00"
    end: "13:00"
    all_day: false
    recurring: true
  - title: "Tanner Grove Bench20"
    day: Wednesday
    start: "13:00"
    end: "14:00"
    all_day: false
    recurring: true
  - title: "Quartz Harbor Bench17"
    day: Wednesday
    start: "14:00"
    end: "15:00"
    all_day: false
    recurring: false
  - title: "Raven Point Bench13"
    day: Wednesday
    start: "14:00"
    end: "15:00"
    all_day: false
    recurring: false
  - title: "Summit Table Bench19"
    day: Wednesday
    start: "15:00"
    end: "16:00"
    all_day: false
    recurring: false
  - title: "Unity Valley Bench21"
    day: Thursday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Vortex Harbor Bench22"
    day: Thursday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Willow Crossing Bench23"
    day: Thursday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Thursday
    start: "12:00"
    end: "13:00"
    all_day: false
    recurring: true
  - title: "Xenon Bridge Bench24"
    day: Friday
    start: "08:00"
    end: "09:00"
    all_day: false
    recurring: false
  - title: "Yonder Creek Bench25"
    day: Friday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Zenith Point Bench26"
    day: Friday
    start: "10:00"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Aspen Harbor Bench27"
    day: Friday
    start: "11:00"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Boulder Ridge Bench28"
    day: Friday
    start: "12:00"
    end: "13:00"
    all_day: false
    recurring: false
  - title: "Cascade Grove"
    day: Friday
    start: "12:00"
    end: "13:00"
    all_day: false
    recurring: false
  - title: "Dark Valley Bench20"
    day: Friday
    start: "12:00"
    end: "13:00"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Friday
    start: "13:00"
    end: "14:00"
    all_day: false
    recurring: true
  - title: "Ember Field Bench31"
    day: Friday
    start: "14:00"
    end: "15:00"
    all_day: false
    recurring: false
  - title: "Forest Trail Bench31"
    day: Friday
    start: "15:00"
    end: "16:00"
    all_day: false
    recurring: false
  - title: "Granite Harbor Manufacturing Modernization Bench33"
    day: Friday
    start: "15:00"
    end: "17:00"
    all_day: false
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
    end: "08:45"
    all_day: false
    recurring: false
  - title: "Birch Wave Bench02"
    day: Monday
    start: "09:00"
    end: "09:45"
    all_day: false
    recurring: false
  - title: "Comet Ridge Bench03"
    day: Monday
    start: "10:00"
    end: "10:45"
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
    start: "13:00"
    end: "13:45"
    all_day: false
    recurring: true
  - title: "Elm Sector Bench05"
    day: Monday
    start: "13:30"
    end: "14:15"
    all_day: false
    recurring: false
  - title: "Falcon Point Bench06"
    day: Monday
    start: "15:00"
    end: "15:45"
    all_day: false
    recurring: false
  - title: "Glacier Route Bench07"
    day: Monday
    start: "16:30"
    end: "17:15"
    all_day: false
    recurring: false
  - title: "Harbor Crest Bench08"
    day: Tuesday
    start: "08:00"
    end: "08:45"
    all_day: false
    recurring: false
  - title: "Island Grove Bench09"
    day: Tuesday
    start: "09:00"
    end: "09:45"
    all_day: false
    recurring: false
  - title: "Jasper Field Bench10"
    day: Tuesday
    start: "10:00"
    end: "10:45"
    all_day: false
    recurring: false
  - title: "Kestrel Bay Bench11"
    day: Tuesday
    start: "11:00"
    end: "11:45"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Tuesday
    start: "13:00"
    end: "13:45"
    all_day: false
    recurring: true
  - title: "Lantern Peak Bench12"
    day: Tuesday
    start: "14:00"
    end: "14:45"
    all_day: false
    recurring: false
  - title: "Meadow Point Bench13"
    day: Tuesday
    start: "15:00"
    end: "15:45"
    all_day: false
    recurring: false
  - title: "Nimbus Trail"
    day: Wednesday
    start: "09:00"
    end: "09:45"
    all_day: false
    recurring: false
  - title: "Orion Gate Bench15"
    day: Wednesday
    start: "09:00"
    end: "09:45"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Wednesday
    start: "13:00"
    end: "13:45"
    all_day: false
    recurring: true
  - title: "Quartz Harbor Bench17"
    day: Wednesday
    start: "14:00"
    end: "15:30"
    all_day: false
    recurring: false
  - title: "Raven Point Bench18"
    day: Wednesday
    start: "15:00"
    end: "15:45"
    all_day: false
    recurring: false
  - title: "Prairie Stone Bench16"
    day: Thursday
    start: "09:00"
    end: "09:45"
    all_day: false
    recurring: false
  - title: "Umbra Valley Bench21"
    day: Thursday
    start: "09:00"
    end: "09:45"
    all_day: false
    recurring: false
  - title: "Vertex Harbor Bench22"
    day: Thursday
    start: "09:00"
    end: "09:45"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Thursday
    start: "13:00"
    end: "13:45"
    all_day: false
    recurring: true
  - title: "Summit Ridge Bench19"
    day: Thursday
    start: "15:00"
    end: "16:30"
    all_day: false
    recurring: false
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
    end: "10:30"
    all_day: false
    recurring: false
  - title: "Cascade"
    day: Friday
    start: "10:30"
    end: "11:00"
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
    start: "13:00"
    end: "13:45"
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
    start: "15:00"
    end: "15:45"
    all_day: false
    recurring: false
  - title: "Granite Harbor Manufacturing Modernization Review Bench33"
    day: Friday
    start: "15:00"
    end: "17:30"
    all_day: false
    recurring: false
  - title: "Willow Crossing Bench23"
    day: Thursday
    start: "09:00"
    end: "09:45"
    all_day: false
    recurring: false

```

## Image B2

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
  - title: "Anchor Time Bench01"
    day: Monday
    start: "08:00"
    end: "08:30"
    all_day: false
    recurring: false
  - title: "Birth Wave Bench02"
    day: Monday
    start: "08:30"
    end: "09:15"
    all_day: false
    recurring: false
  - title: "Camel Ridge Bench03"
    day: Monday
    start: "09:15"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "June Harbor Bench04"
    day: Monday
    start: "10:00"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Tunnel Grove Bench20"
    day: Monday
    start: "11:00"
    end: "12:00"
    all_day: false
    recurring: true
  - title: "Salmon Point Bench06"
    day: Monday
    start: "12:00"
    end: "14:00"
    all_day: false
    recurring: false
  - title: "Glacier Route Bench07"
    day: Monday
    start: "14:00"
    end: "16:00"
    all_day: false
    recurring: false
  - title: "Mariner Coast Bench11"
    day: Tuesday
    start: "08:00"
    end: "09:00"
    all_day: false
    recurring: false
  - title: "Island Grove Bench09"
    day: Tuesday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Jasper Field Bench10"
    day: Tuesday
    start: "10:00"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Rabbit Day Bench11"
    day: Tuesday
    start: "11:00"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Tunnel Grove Bench20"
    day: Tuesday
    start: "12:00"
    end: "13:00"
    all_day: false
    recurring: true
  - title: "Lantern Peak Bench17"
    day: Tuesday
    start: "13:00"
    end: "14:00"
    all_day: false
    recurring: false
  - title: "Meadow Point Bench11"
    day: Tuesday
    start: "14:00"
    end: "15:00"
    all_day: false
    recurring: false
  - title: "Fint Sailor Bench05"
    day: Tuesday
    start: "11:00"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "White Trail Bench14"
    day: Wednesday
    start: "08:00"
    end: "09:30"
    all_day: false
    recurring: false
  - title: "Olive Grove Bench15"
    day: Wednesday
    start: "08:00"
    end: "09:30"
    all_day: false
    recurring: false
  - title: "Prairie Zone Bench16"
    day: Wednesday
    start: "08:00"
    end: "09:30"
    all_day: false
    recurring: false
  - title: "Tunnel Grove Bench20"
    day: Wednesday
    start: "11:00"
    end: "12:00"
    all_day: false
    recurring: true
  - title: "Quartz Trail Bench17"
    day: Wednesday
    start: "12:00"
    end: "14:00"
    all_day: false
    recurring: false
  - title: "Raven Point Bench18"
    day: Wednesday
    start: "12:00"
    end: "14:00"
    all_day: false
    recurring: false
  - title: "Summit Ridge Bench19"
    day: Wednesday
    start: "12:00"
    end: "14:00"
    all_day: false
    recurring: false
  - title: "Union Valley Bench21"
    day: Thursday
    start: "08:00"
    end: "09:30"
    all_day: false
    recurring: false
  - title: "Vortex Field Bench22"
    day: Thursday
    start: "08:00"
    end: "09:30"
    all_day: false
    recurring: false
  - title: "Willow County Bench23"
    day: Thursday
    start: "08:00"
    end: "09:30"
    all_day: false
    recurring: false
  - title: "Tunnel Grove Bench20"
    day: Thursday
    start: "11:00"
    end: "12:00"
    all_day: false
    recurring: true
  - title: "Xenon Bridge Bench24"
    day: Friday
    start: "08:00"
    end: "09:00"
    all_day: false
    recurring: false
  - title: "Yonder Crank Bench25"
    day: Friday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Zenith Point Bench26"
    day: Friday
    start: "10:00"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Aspen Harbor Bench27"
    day: Friday
    start: "11:00"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Cedar Ridge Bench28"
    day: Friday
    start: "11:00"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Cascade Bench29"
    day: Friday
    start: "11:00"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "East Valley Bench30"
    day: Friday
    start: "11:00"
    end: "13:00"
    all_day: false
    recurring: false
  - title: "Tunnel Grove Bench20"
    day: Friday
    start: "12:00"
    end: "13:00"
    all_day: false
    recurring: true
  - title: "Enter Field Bench31"
    day: Friday
    start: "13:00"
    end: "14:00"
    all_day: false
    recurring: false
  - title: "Forest Trail Bench32"
    day: Friday
    start: "14:00"
    end: "15:00"
    all_day: false
    recurring: false
  - title: "Granite Harbor Maintenance Review Bench33"
    day: Friday
    start: "15:00"
    end: "17:00"
    all_day: false
    recurring: false

```

## Image B3

```yaml
events:
  - title: "Monday Day Event Bench35"
    all_day: true
    start_day: Monday
    span_days: 1
    recurring: false
  - title: "Monday Day Event Bench35"
    all_day: true
    start_day: Tuesday
    span_days: 1
    recurring: true
  - title: "Judder Line Bench1"
    day: Monday
    start: "07:30"
    end: "08:00"
    all_day: false
    recurring: false
  - title: "Sedge Water Bench2"
    day: Monday
    start: "08:15"
    end: "09:00"
    all_day: false
    recurring: false
  - title: "Corner Edge Bench3"
    day: Monday
    start: "09:15"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Sedge Water Bench2"
    day: Monday
    start: "10:15"
    end: "11:00"
    all_day: false
    recurring: true
  - title: "Tanner Grove Bench10"
    day: Monday
    start: "11:15"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Sedge Point Bench11"
    day: Monday
    start: "12:15"
    end: "13:00"
    all_day: false
    recurring: false
  - title: "Flower Road Bench12"
    day: Monday
    start: "13:15"
    end: "14:00"
    all_day: false
    recurring: false
  - title: "Harter Crest Bench4"
    day: Tuesday
    start: "08:15"
    end: "09:00"
    all_day: false
    recurring: false
  - title: "Alder Grove Bench5"
    day: Tuesday
    start: "09:15"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Jasper Peak Bench6"
    day: Tuesday
    start: "10:15"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Harter Bay Bench7"
    day: Tuesday
    start: "11:15"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench10"
    day: Tuesday
    start: "12:15"
    end: "13:00"
    all_day: false
    recurring: true
  - title: "Luster Point Bench8"
    day: Tuesday
    start: "13:15"
    end: "14:00"
    all_day: false
    recurring: false
  - title: "Windrow Point Bench9"
    day: Tuesday
    start: "14:15"
    end: "15:00"
    all_day: false
    recurring: false
  - title: "Amber Bus Bench13"
    day: Wednesday
    start: "09:15"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Orange Grove Bench14"
    day: Wednesday
    start: "09:15"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Prairie Blue Bench15"
    day: Wednesday
    start: "09:15"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench10"
    day: Wednesday
    start: "12:15"
    end: "13:00"
    all_day: false
    recurring: true
  - title: "Delta Ratio Bench16"
    day: Wednesday
    start: "13:15"
    end: "14:00"
    all_day: false
    recurring: false
  - title: "Sedge Point Bench17"
    day: Wednesday
    start: "14:15"
    end: "15:00"
    all_day: false
    recurring: false
  - title: "Sedge Point Bench17"
    day: Thursday
    start: "14:15"
    end: "15:00"
    all_day: false
    recurring: true
  - title: "Umbria Valley Bench18"
    day: Thursday
    start: "09:15"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Winter Willow Bench19"
    day: Thursday
    start: "09:15"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Willow Creeking Bench20"
    day: Thursday
    start: "09:15"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench10"
    day: Thursday
    start: "12:15"
    end: "13:00"
    all_day: false
    recurring: true
  - title: "Sedge Point Bench17"
    day: Friday
    start: "14:15"
    end: "15:00"
    all_day: false
    recurring: true
  - title: "Xenon Bridge Bench24"
    day: Friday
    start: "09:15"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Yonder Creek Bench25"
    day: Friday
    start: "09:15"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Cedar Point Bench26"
    day: Friday
    start: "09:15"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Riverstone Bench27"
    day: Friday
    start: "09:15"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Boulder Bridge Bench28"
    day: Friday
    start: "09:15"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Cascade Lake Bench29"
    day: Friday
    start: "10:15"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Drift Valley Bench30"
    day: Friday
    start: "11:15"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench10"
    day: Friday
    start: "12:15"
    end: "13:00"
    all_day: false
    recurring: true
  - title: "Amber Build Bench31"
    day: Friday
    start: "13:15"
    end: "14:00"
    all_day: false
    recurring: false
  - title: "Forest Trail Bench32"
    day: Friday
    start: "14:15"
    end: "15:00"
    all_day: false
    recurring: false
  - title: "Granite Harbor Modernization Revision Bench33"
    day: Friday
    start: "15:15"
    end: "17:00"
    all_day: false
    recurring: false

```

## Image C1

```yaml
events:
  - title: "Duration Check Bench35"
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
    end: "08:40"
    all_day: false
    recurring: false
  - title: "Birch Wave Bench02"
    day: Monday
    start: "08:40"
    end: "09:40"
    all_day: false
    recurring: false
  - title: "Comet Ridge Bench03"
    day: Monday
    start: "09:40"
    end: "10:50"
    all_day: false
    recurring: false
  - title: "Dune Harbor Bench04"
    day: Monday
    start: "10:50"
    end: "12:20"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Monday
    start: "12:20"
    end: "13:30"
    all_day: false
    recurring: true
  - title: "Clim Sector Bench05"
    day: Monday
    start: "13:30"
    end: "14:10"
    all_day: false
    recurring: false
  - title: "Falcon Point Bench06"
    day: Monday
    start: "14:10"
    end: "15:30"
    all_day: false
    recurring: false
  - title: "Glacier Route Bench07"
    day: Monday
    start: "15:30"
    end: "16:50"
    all_day: false
    recurring: false
  - title: "Harbor Cross Bench08"
    day: Tuesday
    start: "08:00"
    end: "08:40"
    all_day: false
    recurring: false
  - title: "Island Grove Bench09"
    day: Tuesday
    start: "08:40"
    end: "10:30"
    all_day: false
    recurring: false
  - title: "Jagdor Field Bench10"
    day: Tuesday
    start: "10:30"
    end: "11:40"
    all_day: false
    recurring: false
  - title: "Nestrel Bay Bench11"
    day: Tuesday
    start: "11:40"
    end: "12:20"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Tuesday
    start: "12:20"
    end: "13:30"
    all_day: false
    recurring: true
  - title: "Lantern Peak Bench12"
    day: Tuesday
    start: "13:30"
    end: "14:10"
    all_day: false
    recurring: false
  - title: "Meadow Point Bench13"
    day: Tuesday
    start: "14:10"
    end: "15:30"
    all_day: false
    recurring: false
  - title: "Fraine Stone Bench16"
    day: Wednesday
    start: "08:40"
    end: "10:20"
    all_day: false
    recurring: false
  - title: "Orion Gate Bench15"
    day: Wednesday
    start: "08:40"
    end: "10:20"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Wednesday
    start: "12:20"
    end: "13:30"
    all_day: false
    recurring: true
  - title: "Quartz Harbor Bench17"
    day: Wednesday
    start: "13:30"
    end: "15:10"
    all_day: false
    recurring: false
  - title: "Raven Point Bench18"
    day: Wednesday
    start: "15:10"
    end: "16:00"
    all_day: false
    recurring: false
  - title: "Vimbus Trail Bench14"
    day: Thursday
    start: "08:40"
    end: "10:20"
    all_day: false
    recurring: false
  - title: "Umora Valley Bench21"
    day: Thursday
    start: "08:40"
    end: "10:20"
    all_day: false
    recurring: false
  - title: "Venter Harbor Bench22"
    day: Thursday
    start: "08:40"
    end: "10:20"
    all_day: false
    recurring: false
  - title: "Willow Crossing Bench23"
    day: Thursday
    start: "08:40"
    end: "10:20"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Thursday
    start: "12:20"
    end: "13:30"
    all_day: false
    recurring: true
  - title: "Summit Ridge Bench19"
    day: Thursday
    start: "15:10"
    end: "16:00"
    all_day: false
    recurring: false
  - title: "Xenon Bridge Bench24"
    day: Friday
    start: "08:00"
    end: "08:40"
    all_day: false
    recurring: false
  - title: "Yonder Creek Bench25"
    day: Friday
    start: "08:40"
    end: "09:30"
    all_day: false
    recurring: false
  - title: "Zenith Point Bench26"
    day: Friday
    start: "09:30"
    end: "10:10"
    all_day: false
    recurring: false
  - title: "Aspen Harbor Bench27"
    day: Friday
    start: "10:10"
    end: "10:50"
    all_day: false
    recurring: false
  - title: "Boulder Ridge Bench28"
    day: Friday
    start: "10:50"
    end: "11:40"
    all_day: false
    recurring: false
  - title: "Cascade Grove Bench29"
    day: Friday
    start: "11:40"
    end: "12:20"
    all_day: false
    recurring: false
  - title: "Drift Valley Bench30"
    day: Friday
    start: "11:40"
    end: "12:20"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Friday
    start: "12:20"
    end: "13:30"
    all_day: false
    recurring: true
  - title: "Lumber Field Bench31"
    day: Friday
    start: "13:30"
    end: "15:10"
    all_day: false
    recurring: false
  - title: "Forest Trail Bench32"
    day: Friday
    start: "15:10"
    end: "16:00"
    all_day: false
    recurring: false
  - title: "Granite Harbor Manufacturing Modernization Review Bench33"
    day: Friday
    start: "16:00"
    end: "17:30"
    all_day: false
    recurring: false

```

## Image C2

```yaml
events:
  - title: "Dates on the Date"
    all_day: true
    start_day: Monday
    span_days: 1
    recurring: false
  - title: "Multiple Day Event Bench 35"
    all_day: true
    start_day: Wednesday
    span_days: 2
    recurring: false
  - title: "A Whit Flo Bench 20"
    day: Monday
    start: "08:00"
    end: "08:30"
    all_day: false
    recurring: false
  - title: "Birch Wave Bench 02"
    day: Monday
    start: "08:30"
    end: "09:30"
    all_day: false
    recurring: false
  - title: "Corner Ridge Bench 11"
    day: Monday
    start: "09:30"
    end: "10:30"
    all_day: false
    recurring: false
  - title: "Curve Harbor Bench 04"
    day: Monday
    start: "10:30"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Tanner Grove"
    day: Monday
    start: "12:00"
    end: "13:30"
    all_day: false
    recurring: true
  - title: "East Sector Bench 05"
    day: Monday
    start: "13:30"
    end: "14:30"
    all_day: false
    recurring: false
  - title: "Falcon Point Bench Line"
    day: Monday
    start: "14:30"
    end: "16:00"
    all_day: false
    recurring: false
  - title: "Grass Route Bench 02"
    day: Monday
    start: "16:00"
    end: "17:00"
    all_day: false
    recurring: false
  - title: "Harbor Crest Bench 08"
    day: Tuesday
    start: "08:00"
    end: "09:00"
    all_day: false
    recurring: false
  - title: "Elaine Grove Bench 09"
    day: Tuesday
    start: "09:00"
    end: "10:30"
    all_day: false
    recurring: false
  - title: "Hyper Trail Bench 07"
    day: Tuesday
    start: "10:30"
    end: "11:30"
    all_day: false
    recurring: false
  - title: "Gentine Ridge Bench 21"
    day: Tuesday
    start: "11:30"
    end: "12:30"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench 20"
    day: Tuesday
    start: "12:30"
    end: "14:00"
    all_day: false
    recurring: true
  - title: "Tanner Peak Bench 17"
    day: Tuesday
    start: "14:00"
    end: "15:00"
    all_day: false
    recurring: false
  - title: "Andean Point Bench 11"
    day: Tuesday
    start: "15:00"
    end: "16:30"
    all_day: false
    recurring: false
  - title: "Granite Stone Bench 6"
    day: Wednesday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Green Gate Bench 5"
    day: Wednesday
    start: "09:00"
    end: "10:30"
    all_day: false
    recurring: false
  - title: "Tampico Trail Bench 14"
    day: Wednesday
    start: "10:30"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench 20"
    day: Wednesday
    start: "12:00"
    end: "13:30"
    all_day: false
    recurring: true
  - title: "Quartz Harbor Bench 17"
    day: Wednesday
    start: "13:30"
    end: "15:00"
    all_day: false
    recurring: false
  - title: "Raven Point Bench 18"
    day: Wednesday
    start: "15:00"
    end: "16:30"
    all_day: false
    recurring: false
  - title: "Umbrella Trail Bench 22"
    day: Thursday
    start: "10:30"
    end: "11:30"
    all_day: false
    recurring: false
  - title: "Velvet Lake Bench 22"
    day: Thursday
    start: "10:30"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Willow Point Bench 21"
    day: Thursday
    start: "11:00"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench 20"
    day: Thursday
    start: "12:00"
    end: "13:30"
    all_day: false
    recurring: true
  - title: "Summit Ridge Bench 18"
    day: Thursday
    start: "14:30"
    end: "16:00"
    all_day: false
    recurring: false
  - title: "Cedar Ridge Bench 26"
    day: Friday
    start: "08:00"
    end: "08:30"
    all_day: false
    recurring: false
  - title: "Andean Crest Bench 11"
    day: Friday
    start: "08:30"
    end: "09:00"
    all_day: false
    recurring: false
  - title: "Andean Point Bench 20"
    day: Friday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Andean Point Bench 27"
    day: Friday
    start: "10:00"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Boulder Ridge Bench 25"
    day: Friday
    start: "11:00"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Cascade Snow Bench 13"
    day: Friday
    start: "11:00"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Jet Way Bench 12"
    day: Friday
    start: "11:00"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench 20"
    day: Friday
    start: "12:00"
    end: "13:30"
    all_day: false
    recurring: true
  - title: "Umbrella Trail Bench 11"
    day: Friday
    start: "13:30"
    end: "15:00"
    all_day: false
    recurring: false
  - title: "Power Trail Bench 10"
    day: Friday
    start: "15:00"
    end: "16:30"
    all_day: false
    recurring: false
  - title: "Satellite Manufacturing Modernization Review Bench 23"
    day: Friday
    start: "15:00"
    end: "17:00"
    all_day: false
    recurring: false

```

## Image C3

```yaml
events:
  - title: "Duration Check Bench 31"
    all_day: true
    start_day: Monday
    span_days: 1
    recurring: false
  - title: "Multi-day Event Bench 35"
    all_day: true
    start_day: Wednesday
    span_days: 2
    recurring: false
  - title: "Arthur Fine Bench 1"
    day: Monday
    start: "08:00"
    end: "08:30"
    all_day: false
    recurring: false
  - title: "Beach Wave Bench 02"
    day: Monday
    start: "08:30"
    end: "09:30"
    all_day: false
    recurring: false
  - title: "Corner Hedge Bench 03"
    day: Monday
    start: "09:30"
    end: "10:30"
    all_day: false
    recurring: false
  - title: "Dune Hidden Bench 04"
    day: Monday
    start: "10:30"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Tanner Grove"
    day: Monday
    start: "12:00"
    end: "14:00"
    all_day: false
    recurring: false
  - title: "Elm Sector Bench 05"
    day: Monday
    start: "13:00"
    end: "14:00"
    all_day: false
    recurring: false
  - title: "Fisher Point Bench 06"
    day: Monday
    start: "14:00"
    end: "16:00"
    all_day: false
    recurring: false
  - title: "Quarter Round Bench 07"
    day: Monday
    start: "16:00"
    end: "17:30"
    all_day: false
    recurring: false
  - title: "Harper Crest Bench 08"
    day: Tuesday
    start: "08:00"
    end: "09:00"
    all_day: false
    recurring: false
  - title: "Island Grove Bench 09"
    day: Tuesday
    start: "09:00"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Jasper Hole Bench 10"
    day: Tuesday
    start: "11:00"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Kestrel Key Bench 11"
    day: Tuesday
    start: "12:00"
    end: "13:00"
    all_day: false
    recurring: false
  - title: "Tunnel Grove Bench 12"
    day: Tuesday
    start: "13:00"
    end: "14:00"
    all_day: false
    recurring: false
  - title: "Lantern Peak Bench 13"
    day: Tuesday
    start: "14:00"
    end: "15:00"
    all_day: false
    recurring: false
  - title: "Marble Point Bench 14"
    day: Tuesday
    start: "15:00"
    end: "16:30"
    all_day: false
    recurring: false
  - title: "Pearls Sea Leaf Bench 16"
    day: Wednesday
    start: "08:30"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Ocean Gale Bench 15"
    day: Wednesday
    start: "08:30"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Amber Leaf Bench 17"
    day: Wednesday
    start: "09:30"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Emerald Grove Bench 18"
    day: Wednesday
    start: "12:00"
    end: "13:00"
    all_day: false
    recurring: false
  - title: "Quartz Harbor Bench 19"
    day: Wednesday
    start: "14:00"
    end: "15:30"
    all_day: false
    recurring: false
  - title: "Silver Pine Bench 20"
    day: Wednesday
    start: "14:30"
    end: "16:00"
    all_day: false
    recurring: false
  - title: "Sapphire Bay Bench 21"
    day: Wednesday
    start: "15:00"
    end: "16:30"
    all_day: false
    recurring: false
  - title: "Amber Leaf Bench 17"
    day: Thursday
    start: "09:30"
    end: "12:00"
    all_day: false
    recurring: true
  - title: "Silver Sector Bench 22"
    day: Thursday
    start: "09:30"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Willow Crossing Bench 23"
    day: Thursday
    start: "09:30"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Lavender Lane Bench 24"
    day: Thursday
    start: "13:00"
    end: "14:00"
    all_day: false
    recurring: false
  - title: "Xenon Bridge Bench 24"
    day: Friday
    start: "08:00"
    end: "09:00"
    all_day: false
    recurring: false
  - title: "Yonder Creek Bench 25"
    day: Friday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Zenith Point Bench 26"
    day: Friday
    start: "10:00"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Auburn Harbor Bench 27"
    day: Friday
    start: "11:00"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Boulder Ridge Bench 28"
    day: Friday
    start: "12:00"
    end: "13:00"
    all_day: false
    recurring: false
  - title: "Cascade Grove Bench 29"
    day: Friday
    start: "12:00"
    end: "13:00"
    all_day: false
    recurring: false
  - title: "Drift Valley Bench 30"
    day: Friday
    start: "12:00"
    end: "13:00"
    all_day: false
    recurring: false
  - title: "Ivory Grove Bench 20"
    day: Friday
    start: "13:00"
    end: "14:00"
    all_day: false
    recurring: false
  - title: "Ember Field Bench 31"
    day: Friday
    start: "14:00"
    end: "15:00"
    all_day: false
    recurring: false
  - title: "Forest Trail Bench 32"
    day: Friday
    start: "15:00"
    end: "16:00"
    all_day: false
    recurring: false
  - title: "Granite Harbor Manufacturing Modernization Review Bench 33"
    day: Friday
    start: "16:00"
    end: "18:00"
    all_day: false
    recurring: false

```
