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
model: "unsloth/gemma-4-26B-A4B-it-GGUF:UD-Q4_K_M"              # full, unambiguous model id. For local GGUF use the full
                       # Hugging Face path incl. lab/tuner + quant tag, e.g.
                       # "unsloth/gemma-3-27b-it-qat-GGUF:UD-Q4_K_XL"
run_date: "2026-06-30"           # YYYY-MM-DD
submitter: "KFleischer"          # a short tag for your submission, shown on the public
                       # leaderboard: a nickname you are happy to show, or just
                       # 5-6 random letters/digits. Keep it the same when you
                       # re-upload to complete this submission.
server_command: '.\llama-server.exe -hf unsloth/gemma-4-26B-A4B-it-GGUF:UD-Q4_K_M --jinja --chat-template-file C:\llamaCpp\templates\gemma-4-interleaved.jinja --reasoning-format auto -ngl 999 --ctx-size 262144 -np 2 --cache-type-k q8_0 --cache-type-v q8_0 --cache-ram 4096 --ctx-checkpoints 8 --no-context-shift --temp 1.0 --top-p 0.95 --top-k 64 --repeat-penalty 1.0 --port 8080 --host 127.0.0.1'     # the exact start command of your model server, e.g. the
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
    span_days: 3
    recurring: false
  - title: "Anchor Flow Bench01"
    day: Monday
    start: "08:00"
    end: "09:00"
    all_day: false
    recurring: false
  - title: "Harbor Crest Bench08"
    day: Tuesday
    start: "08:00"
    end: "09:00"
    all_day: false
    recurring: false
  - title: "Xenon Bridge Bench24"
    day: Friday
    start: "08:00"
    end: "09:00"
    all_day: false
    recurring: false
  - title: "Birch Wave Bench02"
    day: Monday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Island Grove Bench09"
    day: Tuesday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Prairie Stone Bench16"
    day: Wednesday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Orion Gate Bench15"
    day: Wednesday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Nimbus Tra"
    day: Wednesday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Umbra Valley Bench21"
    day: Thursday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Vertex Harbor Bench22"
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
  - title: "Yonder Creek Bench25"
    day: Friday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Comet Ridge Bench03"
    day: Monday
    start: "10:00"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Zenith Point Bench26"
    day: Friday
    start: "10:00"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Jasper Field Bench10"
    day: Tuesday
    start: "10:00"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Aspen Harbor Bench27"
    day: Friday
    start: "10:00"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Dune Harbor Bench04"
    day: Monday
    start: "11:00"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Boulder Ridge Bench28"
    day: Friday
    start: "11:00"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Cascade Gro"
    day: Friday
    start: "11:00"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Kestrel Bay Bench11"
    day: Tuesday
    start: "11:00"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Drift Valley Bench30"
    day: Friday
    start: "11:00"
    end: "13:00"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Monday
    start: "12:00"
    end: "13:00"
    all_day: false
    recurring: true
  - title: "Tanner Grove Be"
    day: Tuesday
    start: "12:00"
    end: "13:00"
    all_day: false
    recurring: true
  - title: "Tanner Grove Bench20"
    day: Wednesday
    start: "12:00"
    end: "13:00"
    all_day: false
    recurring: true
  - title: "Tanner Grove Bench20"
    day: Thursday
    start: "12:00"
    end: "13:00"
    all_day: false
    recurring: true
  - title: "Tanner Grove Bench20"
    day: Friday
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
  - title: "Ember Field Bench31"
    day: Friday
    start: "13:00"
    end: "14:00"
    all_day: false
    recurring: false
  - title: "Lantern Peak Bench12"
    day: Tuesday
    start: "14:00"
    end: "15:00"
    all_day: false
    recurring: false
  - title: "Quartz Harbor Bench17"
    day: Wednesday
    start: "14:00"
    end: "15:00"
    all_day: false
    recurring: false
  - title: "Raven Point Bench18"
    day: Wednesday
    start: "14:00"
    end: "15:00"
    all_day: false
    recurring: false
  - title: "Forest Trail Bench32"
    day: Friday
    start: "14:00"
    end: "15:00"
    all_day: false
    recurring: false
  - title: "Falcon Point Bench06"
    day: Monday
    start: "15:00"
    end: "16:00"
    all_day: false
    recurring: false
  - title: "Meadow Point Bench13"
    day: Tuesday
    start: "15:00"
    end: "16:00"
    all_day: false
    recurring: false
  - title: "Summit Ridge Bench19"
    day: Thursday
    start: "15:00"
    end: "16:00"
    all_day: false
    recurring: false
  - title: "Granite Harbor Manufacturing Modernization Review Bench33"
    day: Friday
    start: "15:00"
    end: "17:00"
    all_day: false
    recurring: false
  - title: "Glacier Route Bench07"
    day: Monday
    start: "16:00"
    end: "17:00"
    all_day: false
    recurring: false

```

## Image A2

```yaml
events:
  - title: "Duration Check Bench34"
    day: Monday
    start: "00:00"
    end: "00:00"
    all_day: true
    start_day: Monday
    span_days: 1
    recurring: false
  - title: "Multiple Day Event Bench35"
    all_day: true
    start_day: Wednesday
    span_days: 1
    recurring: false
  - title: "Anchor Flow Bench01"
    day: Monday
    start: "08:00"
    end: "09:00"
    all_day: false
    recurring: false
  - title: "Harbor Crest Bench08"
    day: Tuesday
    start: "08:00"
    end: "09:00"
    all_day: false
    recurring: false
  - title: "Prairie Stone Bench16"
    day: Wednesday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Nimbus Trail Bench21"
    day: Thursday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Xenon Bridge Bench24"
    day: Friday
    start: "08:00"
    end: "09:00"
    all_day: false
    recurring: false
  - title: "Birch Wave Bench02"
    day: Monday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Island Grove Bench09"
    day: Tuesday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Orion Gate Bench15"
    day: Wednesday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Umbra Valley Bench21"
    day: Thursday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Yonder Creek Bench25"
    day: Friday
    start: "08:00"
    end: "09:00"
    all_day: false
    recurring: false
  - title: "Comet Ridge Bench03"
    day: Monday
    start: "10:00"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Jasper Field Bench10"
    day: Tuesday
    start: "10:00"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Vertex Harbor Bench22"
    day: Thursday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Zenith Point Bench26"
    day: Friday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Dune Harbor Bench04"
    day: Monday
    start: "11:00"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Willow Crossing Bench23"
    day: Thursday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Aspen Harbor Bench27"
    day: Friday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Kestrel Bay Bench11"
    day: Tuesday
    start: "12:00"
    end: "13:00"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Tuesday
    start: "12:00"
    end: "13:00"
    all_day: false
    recurring: true
  - title: "Tanner Grove Bench20"
    day: Wednesday
    start: "12:00"
    end: "13:00"
    all_day: false
    recurring: true
  - title: "Tanner Grove Bench20"
    day: Thursday
    start: "12:00"
    end: "13:00"
    all_day: false
    recurring: true
  - title: "Tanner Grove Bench20"
    day: Friday
    start: "12:00"
    end: "13:00"
    all_day: false
    recurring: true
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
  - title: "Lantern Peak Bench12"
    day: Tuesday
    start: "14:00"
    end: "15:00"
    all_day: false
    recurring: false
  - title: "Quarte Harbor Bench17"
    day: Wednesday
    start: "14:00"
    end: "15:00"
    all_day: false
    recurring: false
  - title: "Boulder Ridge Bench28"
    day: Friday
    start: "10:00"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Cascade Gro Bench30"
    day: Friday
    start: "10:00"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Drift Valley Bench30"
    day: Friday
    start: "11:00"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Falcon Point Bench06"
    day: Monday
    start: "15:00"
    end: "16:00"
    all_day: false
    recurring: false
  - title: "Meadow Point Bench13"
    day: Tuesday
    start: "15:00"
    end: "16:00"
    all_day: false
    recurring: false
  - title: "Raven Point Bench18"
    day: Wednesday
    start: "15:00"
    end: "16:00"
    all_day: false
    recurring: false
  - title: "Forest Trail Bench31"
    day: Friday
    start: "15:00"
    end: "16:00"
    all_day: false
    recurring: false
  - title: "Summit Ridge Bench19"
    day: Wednesday
    start: "16:00"
    end: "17:00"
    all_day: false
    recurring: false
  - title: "Glacier Route Bench07"
    day: Monday
    start: "16:00"
    end: "17:00"
    all_day: false
    recurring: false
  - title: "Embar Field Bench31"
    day: Friday
    start: "13:00"
    end: "14:00"
    all_day: false
    recurring: false
  - title: "Granite Harbor Manufacturing Modernization Review Bench33"
    day: Friday
    start: "16:00"
    end: "17:00"
    all_day: false
    recurring: false

```

## Image A3

```yaml
events:
  - title: "Bananas Coast Bench01"
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
  - title: "Birch Wave Bench02"
    day: Monday
    start: "09:00"
    end: "10:15"
    all_day: false
    recurring: false
  - title: "Camel Ridge Bench03"
    day: Monday
    start: "10:15"
    end: "11:15"
    all_day: false
    recurring: false
  - title: "Dane-Nalton Bench04"
    day: Monday
    start: "11:15"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench05"
    day: Monday
    start: "12:15"
    end: "13:15"
    all_day: false
    recurring: false
  - title: "Erie Senior Bench06"
    day: Monday
    start: "13:15"
    end: "14:15"
    all_day: false
    recurring: false
  - title: "Falcon Point Bench04"
    day: Monday
    start: "14:15"
    end: "15:15"
    all_day: false
    recurring: false
  - title: "Glacier South Bench07"
    day: Monday
    start: "15:15"
    end: "16:15"
    all_day: false
    recurring: false
  - title: "Parker Coast Bench08"
    day: Tuesday
    start: "08:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Island Grove Bench09"
    day: Tuesday
    start: "10:00"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Jasper Falls Bench10"
    day: Tuesday
    start: "11:00"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Crystal Bay Bench11"
    day: Tuesday
    start: "12:00"
    end: "13:00"
    all_day: false
    recurring: false
  - title: "Larkin Peak Bench12"
    day: Tuesday
    start: "13:15"
    end: "14:15"
    all_day: false
    recurring: false
  - title: "Meadow Point Bench13"
    day: Tuesday
    start: "14:15"
    end: "15:15"
    all_day: false
    recurring: false
  - title: "Prairie Dune Bench15"
    day: Wednesday
    start: "08:00"
    end: "09:00"
    all_day: false
    recurring: false
  - title: "Orion Gate Bench16"
    day: Wednesday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Nimbus Trail Bench17"
    day: Wednesday
    start: "10:00"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Under Valley Bench18"
    day: Wednesday
    start: "11:00"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Vortex Harbor Bench19"
    day: Wednesday
    start: "12:00"
    end: "13:00"
    all_day: false
    recurring: false
  - title: "Willow Crossing Bench20"
    day: Wednesday
    start: "13:00"
    end: "14:00"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench05"
    day: Wednesday
    start: "12:15"
    end: "13:15"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench05"
    day: Wednesday
    start: "13:15"
    end: "14:15"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench05"
    day: Wednesday
    start: "14:15"
    end: "15:15"
    all_day: false
    recurring: false
  - title: "Quartz Harbor Bench17"
    day: Wednesday
    start: "14:15"
    end: "15:15"
    all_day: false
    recurring: false
  - title: "Raven Point Bench18"
    day: Wednesday
    start: "15:15"
    end: "16:15"
    all_day: false
    recurring: false
  - title: "Summit Valley Bench19"
    day: Wednesday
    start: "16:15"
    end: "17:15"
    all_day: false
    recurring: false
  - title: "Under Valley Bench21"
    day: Thursday
    start: "08:00"
    end: "09:00"
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
    start: "10:00"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench05"
    day: Thursday
    start: "12:15"
    end: "13:15"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench05"
    day: Thursday
    start: "13:15"
    end: "14:15"
    all_day: false
    recurring: false
  - title: "Ember Field Bench31"
    day: Thursday
    start: "14:15"
    end: "16:15"
    all_day: false
    recurring: false
  - title: "Forest Trail Bench33"
    day: Thursday
    start: "16:15"
    end: "17:15"
    all_day: false
    recurring: false
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
    start: "12:15"
    end: "13:15"
    all_day: false
    recurring: false
  - title: "Cascade Gro Bench29"
    day: Friday
    start: "13:15"
    end: "14:15"
    all_day: false
    recurring: false
  - title: "Dant Valley Bench30"
    day: Friday
    start: "14:15"
    end: "15:15"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench05"
    day: Friday
    start: "12:15"
    end: "13:15"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench05"
    day: Friday
    start: "13:15"
    end: "14:15"
    all_day: false
    recurring: false
  - title: "Grindite Harbor Manufacturing Modernization Bench33"
    day: Friday
    start: "14:15"
    end: "17:15"
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
    end: "09:00"
    all_day: false
    recurring: false
  - title: "Birch Wave Bench02"
    day: Monday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Comet Ridge Bench03"
    day: Monday
    start: "10:00"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Dune Harbor Bench04"
    day: Monday
    start: "11:00"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Monday
    start: "13:00"
    end: "14:00"
    all_day: false
    recurring: true
  - title: "Falcon Point Bench06"
    day: Monday
    start: "15:00"
    end: "16:00"
    all_day: false
    recurring: false
  - title: "Glacier Route Bench07"
    day: Monday
    start: "17:00"
    end: "18:00"
    all_day: false
    recurring: false
  - title: "Elm Sector Bench05"
    day: Monday
    start: "13:00"
    end: "14:00"
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
  - title: "Kestrel Bay Bench11"
    day: Tuesday
    start: "11:00"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Tuesday
    start: "13:00"
    end: "14:00"
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
    end: "16:00"
    all_day: false
    recurring: false
  - title: "Nimbus Trail"
    day: Wednesday
    start: "09:00"
    end: "10:00"
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
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Umbra Valley Bench21"
    day: Wednesday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Vertex Harbor Bench22"
    day: Wednesday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Willow Crossing Bench23"
    day: Wednesday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
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
  - title: "Raven Point Bench18"
    day: Wednesday
    start: "15:00"
    end: "16:00"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench20"
    day: Thursday
    start: "13:00"
    end: "14:00"
    all_day: false
    recurring: true
  - title: "Summit Ridge Bench19"
    day: Thursday
    start: "15:00"
    end: "16:00"
    all_day: false
    recurring: false
  - title: "Xenon Bridge Bench24"
    day: Friday
    start: "08:00"
    end: "09:00"
    all_day: false
    recurring: false
  - title: "Yonder Creek Bench25"
    day: Friday
    start: "08:00"
    end: "09:00"
    all_day: false
    recurring: false
  - title: "Zenith Point Bench26"
    day: Friday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Aspen Harbor Bench27"
    day: Friday
    start: "09:00"
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
    start: "10:00"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Drift Valley Bench30"
    day: Friday
    start: "10:00"
    end: "11:00"
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
  - title: "Forest Trail Bench32"
    day: Friday
    start: "15:00"
    end: "16:00"
    all_day: false
    recurring: false
  - title: "Granite Harbor Manufacturing Modernization Review Bench33"
    day: Friday
    start: "16:00"
    end: "18:00"
    all_day: false
    recurring: false

```

## Image B2

```yaml
events:
  - title: "Duration Check Bench154"
    all_day: true
    start_day: Monday
    span_days: 1
    recurring: false
  - title: "Multiple Day Event Bench153"
    all_day: true
    start_day: Wednesday
    span_days: 1
    recurring: false
  - title: "Multiple Day Event Bench153"
    all_day: true
    start_day: Thursday
    span_days: 1
    recurring: false
  - title: "Andor Pine Bench151"
    day: Monday
    start: "08:00"
    end: "09:00"
    all_day: false
    recurring: false
  - title: "Birch Wave Bench152"
    day: Monday
    start: "09:00"
    end: "10:10"
    all_day: false
    recurring: false
  - title: "Camel Ridge Bench153"
    day: Monday
    start: "10:10"
    end: "11:25"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench155"
    day: Monday
    start: "12:15"
    end: "13:15"
    all_day: false
    recurring: false
  - title: "June River Bench156"
    day: Monday
    start: "13:15"
    end: "14:35"
    all_day: false
    recurring: false
  - title: "Glacier Route Bench157"
    day: Monday
    start: "14:35"
    end: "15:40"
    all_day: false
    recurring: false
  - title: "Mariana Coast Bench155"
    day: Tuesday
    start: "08:00"
    end: "09:10"
    all_day: false
    recurring: false
  - title: "Island Grove Bench159"
    day: Tuesday
    start: "09:10"
    end: "10:15"
    all_day: false
    recurring: false
  - title: "Jasper Field Bench151"
    day: Tuesday
    start: "10:15"
    end: "11:20"
    all_day: false
    recurring: false
  - title: "Kellet Day Bench154"
    day: Tuesday
    start: "11:20"
    end: "12:25"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench153"
    day: Tuesday
    start: "12:25"
    end: "13:40"
    all_day: false
    recurring: false
  - title: "Finn Sailor Bench156"
    day: Tuesday
    start: "12:35"
    end: "13:45"
    all_day: false
    recurring: false
  - title: "Lamert Peak Bench157"
    day: Tuesday
    start: "13:40"
    end: "14:50"
    all_day: false
    recurring: false
  - title: "Meadow Point Bench151"
    day: Tuesday
    start: "14:50"
    end: "15:50"
    all_day: false
    recurring: false
  - title: "Willow Trail Bench151"
    day: Wednesday
    start: "08:00"
    end: "09:10"
    all_day: false
    recurring: false
  - title: "Otter Gain Bench155"
    day: Wednesday
    start: "09:10"
    end: "10:15"
    all_day: false
    recurring: false
  - title: "Prairie June Bench155"
    day: Wednesday
    start: "10:15"
    end: "11:20"
    all_day: false
    recurring: false
  - title: "Quartz Trail Bench157"
    day: Wednesday
    start: "11:20"
    end: "12:25"
    all_day: false
    recurring: false
  - title: "Raven Point Bench158"
    day: Wednesday
    start: "12:25"
    end: "13:40"
    all_day: false
    recurring: false
  - title: "Summit Ridge Bench159"
    day: Wednesday
    start: "13:40"
    end: "14:50"
    all_day: false
    recurring: false
  - title: "Union Valley Bench21"
    day: Thursday
    start: "08:00"
    end: "09:05"
    all_day: false
    recurring: false
  - title: "Vance Creek Bench22"
    day: Thursday
    start: "09:05"
    end: "10:10"
    all_day: false
    recurring: false
  - title: "Willow County Bench23"
    day: Thursday
    start: "10:10"
    end: "11:15"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench21"
    day: Thursday
    start: "11:15"
    end: "12:25"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench21"
    day: Thursday
    start: "12:25"
    end: "13:35"
    all_day: false
    recurring: false
  - title: "Elric Field Bench157"
    day: Thursday
    start: "13:35"
    end: "14:45"
    all_day: false
    recurring: false
  - title: "Summit Trail Bench157"
    day: Thursday
    start: "14:45"
    end: "15:55"
    all_day: false
    recurring: false
  - title: "Xanon Ridge Bench154"
    day: Friday
    start: "08:00"
    end: "09:05"
    all_day: false
    recurring: false
  - title: "Yonder Creek Bench155"
    day: Friday
    start: "09:05"
    end: "10:10"
    all_day: false
    recurring: false
  - title: "Zenith Point Bench157"
    day: Friday
    start: "10:10"
    end: "11:15"
    all_day: false
    recurring: false
  - title: "Aspen Harbor Bench157"
    day: Friday
    start: "11:15"
    end: "12:20"
    all_day: false
    recurring: false
  - title: "Elric Ridge Bench158"
    day: Friday
    start: "12:20"
    end: "13:25"
    all_day: false
    recurring: false
  - title: "Cascade Bench159"
    day: Friday
    start: "12:25"
    end: "13:30"
    all_day: false
    recurring: false
  - title: "Tanner Grove Bench159"
    day: Friday
    start: "13:30"
    end: "14:35"
    all_day: false
    recurring: false
  - title: "Elric Field Bench157"
    day: Friday
    start: "14:35"
    end: "15:40"
    all_day: false
    recurring: false
  - title: "Summit Trail Bench157"
    day: Friday
    start: "15:40"
    end: "16:45"
    all_day: false
    recurring: false
  - title: "Granite Harbor Manufacturing Review Bench153"
    day: Friday
    start: "15:45"
    end: "16:55"
    all_day: false
    recurring: false
  - title: "Little Valley Bench153"
    day: Friday
    start: "12:25"
    end: "13:30"
    all_day: false
    recurring: false

```

## Image B3

```yaml
events:
  - title: "Mistletoe Bay Event Bench35"
    all_day: true
    start_day: Monday
    span_days: 5
    recurring: true
  - title: "Jackson Lake Bench34"
    day: Monday
    start: "08:40"
    end: "09:40"
    all_day: false
    recurring: false
  - title: "Cedar Water Bench33"
    day: Monday
    start: "10:15"
    end: "11:45"
    all_day: false
    recurring: false
  - title: "Cedar Wing Bench33"
    day: Monday
    start: "13:45"
    end: "15:30"
    all_day: false
    recurring: false
  - title: "Cedar Lake Bench33"
    day: Monday
    start: "16:45"
    end: "18:00"
    all_day: false
    recurring: false
  - title: "Cedar Grove Bench33"
    day: Monday
    start: "18:15"
    end: "20:00"
    all_day: false
    recurring: false
  - title: "Cedar Point Bench33"
    day: Monday
    start: "20:15"
    end: "21:45"
    all_day: false
    recurring: false
  - title: "Cedar Basin Bench33"
    day: Monday
    start: "22:00"
    end: "23:30"
    all_day: false
    recurring: false
  - title: "Harbor Crest Bench34"
    day: Tuesday
    start: "09:45"
    end: "11:30"
    all_day: false
    recurring: false
  - title: "Adams Grove Bench33"
    day: Tuesday
    start: "12:00"
    end: "13:30"
    all_day: false
    recurring: false
  - title: "Jasper Peak Bench33"
    day: Tuesday
    start: "14:00"
    end: "15:45"
    all_day: false
    recurring: false
  - title: "Harbor Bay Bench33"
    day: Tuesday
    start: "16:15"
    end: "17:45"
    all_day: false
    recurring: false
  - title: "Tennis Grove Bench33"
    day: Tuesday
    start: "18:15"
    end: "19:45"
    all_day: false
    recurring: false
  - title: "Linden Park Bench33"
    day: Tuesday
    start: "20:15"
    end: "21:45"
    all_day: false
    recurring: false
  - title: "Windsor Point Bench33"
    day: Tuesday
    start: "22:00"
    end: "23:30"
    all_day: false
    recurring: false
  - title: "Ambush Train Bench33"
    day: Wednesday
    start: "09:30"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Orange Grove Bench33"
    day: Wednesday
    start: "11:30"
    end: "13:00"
    all_day: false
    recurring: false
  - title: "Prairie Bluff Bench33"
    day: Wednesday
    start: "13:30"
    end: "15:00"
    all_day: false
    recurring: false
  - title: "Timber Grove Bench33"
    day: Wednesday
    start: "15:30"
    end: "17:00"
    all_day: false
    recurring: false
  - title: "Timber Grove Bench33"
    day: Wednesday
    start: "17:30"
    end: "19:00"
    all_day: false
    recurring: false
  - title: "Oatley Ridge Bench33"
    day: Wednesday
    start: "19:30"
    end: "21:00"
    all_day: false
    recurring: false
  - title: "Jasper Point Bench33"
    day: Wednesday
    start: "21:30"
    end: "23:00"
    all_day: false
    recurring: false
  - title: "Jasper Ridge Bench33"
    day: Wednesday
    start: "23:15"
    end: "23:59"
    all_day: false
    recurring: false
  - title: "Umbra Valley Bench33"
    day: Thursday
    start: "10:15"
    end: "11:45"
    all_day: false
    recurring: false
  - title: "Bitter Harbor Bench33"
    day: Thursday
    start: "12:15"
    end: "13:45"
    all_day: false
    recurring: false
  - title: "Willow Creek Bench33"
    day: Thursday
    start: "14:15"
    end: "15:45"
    all_day: false
    recurring: false
  - title: "Tennis Grove Bench33"
    day: Thursday
    start: "16:15"
    end: "17:45"
    all_day: false
    recurring: false
  - title: "Timber Grove Bench33"
    day: Thursday
    start: "18:15"
    end: "19:45"
    all_day: false
    recurring: false
  - title: "Amber Hill Bench33"
    day: Thursday
    start: "20:15"
    end: "21:45"
    all_day: false
    recurring: false
  - title: "Forest Trail Bench33"
    day: Thursday
    start: "22:00"
    end: "23:30"
    all_day: false
    recurring: false
  - title: "Xenon Bridge Bench34"
    day: Friday
    start: "09:15"
    end: "10:45"
    all_day: false
    recurring: false
  - title: "Yarrow Creek Bench35"
    day: Friday
    start: "11:15"
    end: "12:45"
    all_day: false
    recurring: false
  - title: "Cedar Point Bench35"
    day: Friday
    start: "13:15"
    end: "14:45"
    all_day: false
    recurring: false
  - title: "Jasper Ridge Bench35"
    day: Friday
    start: "15:15"
    end: "16:45"
    all_day: false
    recurring: false
  - title: "Boulder Ridge Bench35"
    day: Friday
    start: "17:15"
    end: "18:45"
    all_day: false
    recurring: false
  - title: "Cascade Bench35"
    day: Friday
    start: "19:15"
    end: "20:45"
    all_day: false
    recurring: false
  - title: "Drift Valley Bench35"
    day: Friday
    start: "21:15"
    end: "22:45"
    all_day: false
    recurring: false
  - title: "Tennis Grove Bench35"
    day: Friday
    start: "10:30"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Amber Hill Bench35"
    day: Friday
    start: "12:30"
    end: "14:00"
    all_day: false
    recurring: false
  - title: "Forest Trail Bench35"
    day: Friday
    start: "14:30"
    end: "16:00"
    all_day: false
    recurring: false
  - title: "Granite Harbor Modernization/Revitalization Bench35"
    day: Friday
    start: "16:30"
    end: "23:30"
    all_day: false
    recurring: false

```

## Image C1

```yaml
events:
  - title: "Duration Check Bench03"
    all_day: true
    start_day: Monday
    span_days: 1
    recurring: false
  - title: "Multiple Day Event Bench05"
    all_day: true
    start_day: Wednesday
    span_days: 3
    recurring: false
  - title: "Anchor Flow Bench01"
    day: Monday
    start: "08:15"
    end: "09:00"
    all_day: false
    recurring: false
  - title: "Birch Wave Bench02"
    day: Monday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Comet Ridge Bench03"
    day: Monday
    start: "10:00"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Dune Harbor Bench04"
    day: Monday
    start: "11:00"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Tanner Grow Bench20"
    day: Monday
    start: "13:00"
    end: "14:00"
    all_day: false
    recurring: true
  - title: "Clim Sector Bench05"
    day: Monday
    start: "13:00"
    end: "14:00"
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
    start: "17:00"
    end: "18:00"
    all_day: false
    recurring: false
  - title: "Harbor Cross Bench08"
    day: Tuesday
    start: "08:15"
    end: "09:00"
    all_day: false
    recurring: false
  - title: "Island Grove Bench09"
    day: Tuesday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Lajgar Field Bench10"
    day: Tuesday
    start: "10:00"
    end: "11:00"
    all_day: false
    recurring: false
  - title: "Restrel Bay Bench11"
    day: Tuesday
    start: "11:00"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Tanner Grow Bench20"
    day: Tuesday
    start: "13:00"
    end: "14:00"
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
    end: "16:00"
    all_day: false
    recurring: false
  - title: "Prairie Stone Bench16"
    day: Wednesday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Crion Gate Bench15"
    day: Wednesday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Tanner Grow Bench20"
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
  - title: "Raven Point Bench18"
    day: Wednesday
    start: "15:00"
    end: "16:00"
    all_day: false
    recurring: false
  - title: "Summit Ridge Bench19"
    day: Wednesday
    start: "16:00"
    end: "17:00"
    all_day: false
    recurring: false
  - title: "Umora Valley Bench21"
    day: Thursday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Vambus Trail Bench14"
    day: Thursday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: false
  - title: "Tanner Grow Bench20"
    day: Thursday
    start: "13:00"
    end: "14:00"
    all_day: false
    recurring: true
  - title: "Xenon Bridge Bench24"
    day: Friday
    start: "08:15"
    end: "09:00"
    all_day: false
    recurring: false
  - title: "Yandor Creek Bench25"
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
    start: "11:00"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Coscate Grove Bench29"
    day: Friday
    start: "11:00"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Drift Valley Bench30"
    day: Friday
    start: "11:00"
    end: "12:00"
    all_day: false
    recurring: false
  - title: "Tanner Grow Bench20"
    day: Friday
    start: "13:00"
    end: "14:00"
    all_day: false
    recurring: true
  - title: "Lumber Field Bench31"
    day: Friday
    start: "14:00"
    end: "15:00"
    all_day: false
    recurring: false
  - title: "Forest Trail Bench32"
    day: Friday
    start: "15:00"
    end: "16:00"
    all_day: false
    recurring: false
  - title: "Granite Harbor Manufacturing Modernization Review Bench33"
    day: Friday
    start: "16:00"
    end: "17:00"
    all_day: false
    recurring: false

```

## Image C2

```yaml
events:
  - title: "Due on Bank Date B5"
    all_day: true
    start_day: Monday
    span_days: 1
    recurring: false
  - title: "Multiple Day Event Bench 25"
    all_day: true
    start_day: Wednesday
    span_days: 1
    recurring: false
  - title: "Multiple Day Event Bench 25"
    all_day: true
    start_day: Thursday
    span_days: 1
    recurring: false
  - title: "Axton Flow Bench 22"
    day: Monday
    start: "08:00"
    end: "09:15"
    all_day: false
    recurring: true
  - title: "Bath Wave Bench 22"
    day: Monday
    start: "09:35"
    end: "10:45"
    all_day: false
    recurring: true
  - title: "Comer Ridge Bench 23"
    day: Monday
    start: "10:00"
    end: "10:45"
    all_day: false
    recurring: true
  - title: "Dune Harbor Bench 24"
    day: Monday
    start: "11:00"
    end: "12:00"
    all_day: false
    recurring: true
  - title: "Tanner Grove"
    day: Monday
    start: "12:10"
    end: "13:30"
    all_day: false
    recurring: true
  - title: "Elm Sector Bench 25"
    day: Monday
    start: "13:35"
    end: "14:55"
    all_day: false
    recurring: true
  - title: "Falcon Point Bench 26"
    day: Monday
    start: "15:00"
    end: "16:10"
    all_day: false
    recurring: true
  - title: "Grater Route Bench 27"
    day: Monday
    start: "16:20"
    end: "17:30"
    all_day: false
    recurring: true
  - title: "Falcon Crest Bench 20"
    day: Tuesday
    start: "08:35"
    end: "09:55"
    all_day: false
    recurring: true
  - title: "Elong Grove Bench 21"
    day: Tuesday
    start: "10:00"
    end: "11:00"
    all_day: false
    recurring: true
  - title: "Hyper Trail Bench 22"
    day: Tuesday
    start: "10:10"
    end: "11:05"
    all_day: false
    recurring: true
  - title: "Gentle Springs Bench 23"
    day: Tuesday
    start: "11:10"
    end: "12:10"
    all_day: false
    recurring: true
  - title: "Tanner Creek Bench 24"
    day: Tuesday
    start: "12:15"
    end: "13:30"
    all_day: false
    recurring: true
  - title: "Tanner Creek Bench 24"
    day: Tuesday
    start: "13:35"
    end: "14:45"
    all_day: false
    recurring: true
  - title: "Tanner Peak Bench 27"
    day: Tuesday
    start: "14:50"
    end: "16:10"
    all_day: false
    recurring: true
  - title: "Meadow Point Bench 11"
    day: Tuesday
    start: "16:15"
    end: "17:30"
    all_day: false
    recurring: true
  - title: "Prairie Stone Bench 6"
    day: Wednesday
    start: "08:40"
    end: "10:00"
    all_day: false
    recurring: true
  - title: "Green Gate Bench 5"
    day: Wednesday
    start: "10:05"
    end: "11:00"
    all_day: false
    recurring: true
  - title: "Tampico Trail Bench 21"
    day: Wednesday
    start: "10:10"
    end: "11:05"
    all_day: false
    recurring: true
  - title: "Tanner Grove Bench 25"
    day: Wednesday
    start: "12:10"
    end: "13:30"
    all_day: false
    recurring: true
  - title: "Quartz Harbor Bench 17"
    day: Wednesday
    start: "14:45"
    end: "16:00"
    all_day: false
    recurring: true
  - title: "Raven Point Bench 16"
    day: Wednesday
    start: "16:05"
    end: "17:20"
    all_day: false
    recurring: true
  - title: "Summit Ridge Bench 18"
    day: Wednesday
    start: "16:20"
    end: "17:30"
    all_day: false
    recurring: true
  - title: "Tanner Creek Bench 22"
    day: Thursday
    start: "09:45"
    end: "10:45"
    all_day: false
    recurring: true
  - title: "Willie Forest Bench 23"
    day: Thursday
    start: "10:50"
    end: "11:50"
    all_day: false
    recurring: true
  - title: "Tanner Grove Bench 25"
    day: Thursday
    start: "12:10"
    end: "13:30"
    all_day: false
    recurring: true
  - title: "Tanner Grove Bench 25"
    day: Thursday
    start: "13:35"
    end: "14:45"
    all_day: false
    recurring: true
  - title: "Elm Sector Bench 25"
    day: Thursday
    start: "15:00"
    end: "16:20"
    all_day: false
    recurring: true
  - title: "Tanner Creek Bench 24"
    day: Friday
    start: "08:45"
    end: "09:55"
    all_day: false
    recurring: true
  - title: "Valley Creek Bench 25"
    day: Friday
    start: "09:55"
    end: "11:05"
    all_day: false
    recurring: true
  - title: "Prairie Point Bench 26"
    day: Friday
    start: "11:05"
    end: "12:15"
    all_day: false
    recurring: true
  - title: "Ashton Harbor Bench 27"
    day: Friday
    start: "12:15"
    end: "13:30"
    all_day: false
    recurring: true
  - title: "Tanner Grove Bench 25"
    day: Friday
    start: "13:35"
    end: "14:45"
    all_day: false
    recurring: true
  - title: "Tanner Grove Bench 25"
    day: Friday
    start: "14:45"
    end: "15:55"
    all_day: false
    recurring: true
  - title: "Elm Sector Bench 25"
    day: Friday
    start: "16:05"
    end: "17:10"
    all_day: false
    recurring: true
  - title: "Tanner Creek Bench 24"
    day: Friday
    start: "16:15"
    end: "17:20"
    all_day: false
    recurring: true
  - title: "Tanner Creek Manufacturing/Expansion Bench 23"
    day: Friday
    start: "16:30"
    end: "17:30"
    all_day: false
    recurring: true

```

## Image C3

```yaml
events:
  - title: "Quaker Creek Bench34"
    all_day: true
    start_day: Monday
    span_days: 1
    recurring: false
  - title: "Multi-Day Event Bench35"
    all_day: true
    start_day: Wednesday
    span_days: 2
    recurring: false
  - title: "Multi-Day Event Bench35"
    all_day: true
    start_day: Thursday
    span_days: 1
    recurring: false
  - title: "Auður Finn Bench31"
    day: Monday
    start: "08:00"
    end: "09:00"
    all_day: false
    recurring: true
  - title: "Harbor Creek Bench31"
    day: Tuesday
    start: "08:00"
    end: "10:00"
    all_day: false
    recurring: true
  - title: "Xenon Bridge Bench34"
    day: Friday
    start: "08:00"
    end: "09:00"
    all_day: false
    recurring: true
  - title: "Yonder Creek Bench35"
    day: Friday
    start: "08:00"
    end: "09:00"
    all_day: false
    recurring: true
  - title: "Birch Wave Bench32"
    day: Monday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: true
  - title: "Island Grove Bench30"
    day: Tuesday
    start: "09:00"
    end: "10:30"
    all_day: false
    recurring: true
  - title: "Zenith Point Bench36"
    day: Friday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: true
  - title: "Auður Finn Bench31"
    day: Friday
    start: "09:00"
    end: "10:00"
    all_day: false
    recurring: true
  - title: "Kamur Hodge Bench33"
    day: Monday
    start: "10:00"
    end: "11:00"
    all_day: false
    recurring: true
  - title: "Klein 5-leaf Bench36"
    day: Wednesday
    start: "10:00"
    end: "11:00"
    all_day: false
    recurring: true
  - title: "Dunn Gate Bench35"
    day: Wednesday
    start: "10:00"
    end: "11:00"
    all_day: false
    recurring: true
  - title: "Timber Fall Bench31"
    day: Wednesday
    start: "10:00"
    end: "11:00"
    all_day: false
    recurring: true
  - title: "Lumber Yard Bench32"
    day: Thursday
    start: "10:00"
    end: "11:00"
    all_day: false
    recurring: true
  - title: "Xenon Bridge Bench34"
    day: Thursday
    start: "10:00"
    end: "11:00"
    all_day: false
    recurring: true
  - title: "Willow Crossing Bench32"
    day: Thursday
    start: "10:00"
    end: "11:00"
    all_day: false
    recurring: true
  - title: "Dune Haden Bench34"
    day: Monday
    start: "11:00"
    end: "12:00"
    all_day: false
    recurring: true
  - title: "Leijen Holz Bench30"
    day: Tuesday
    start: "11:00"
    end: "12:00"
    all_day: false
    recurring: true
  - title: "Islander Bridge Bench38"
    day: Friday
    start: "11:00"
    end: "12:00"
    all_day: false
    recurring: true
  - title: "Cascade Grove Bench39"
    day: Friday
    start: "11:00"
    end: "12:00"
    all_day: false
    recurring: true
  - title: "Birch Valley Bench30"
    day: Friday
    start: "11:00"
    end: "12:00"
    all_day: false
    recurring: true
  - title: "Koppen Clay Bench31"
    day: Tuesday
    start: "12:00"
    end: "13:00"
    all_day: false
    recurring: true
  - title: "Tanner Grove"
    day: Monday
    start: "13:00"
    end: "14:00"
    all_day: false
    recurring: true
  - title: "Elm Sector Bench36"
    day: Monday
    start: "13:00"
    end: "14:00"
    all_day: false
    recurring: true
  - title: "Tanner Grove Bench30"
    day: Tuesday
    start: "13:00"
    end: "14:00"
    all_day: false
    recurring: true
  - title: "Lumber Yard Bench32"
    day: Wednesday
    start: "13:00"
    end: "14:00"
    all_day: false
    recurring: true
  - title: "Lumber Yard Bench32"
    day: Thursday
    start: "13:00"
    end: "14:00"
    all_day: false
    recurring: true
  - title: "Lanner Grove Bench30"
    day: Friday
    start: "13:00"
    end: "14:00"
    all_day: false
    recurring: true
  - title: "Fossen Point Bench30"
    day: Monday
    start: "14:00"
    end: "15:00"
    all_day: false
    recurring: true
  - title: "Lanner Peak Bench32"
    day: Tuesday
    start: "14:00"
    end: "15:00"
    all_day: false
    recurring: true
  - title: "Quaker Harbor Bench31"
    day: Wednesday
    start: "14:00"
    end: "15:00"
    all_day: false
    recurring: true
  - title: "Quaker Harbor Bench31"
    day: Thursday
    start: "14:00"
    end: "15:00"
    all_day: false
    recurring: true
  - title: "Fossen Point Bench30"
    day: Friday
    start: "14:00"
    end: "15:00"
    all_day: false
    recurring: true
  - title: "Lamber Holz Bench31"
    day: Friday
    start: "14:00"
    end: "15:00"
    all_day: false
    recurring: true
  - title: "Fossen Point Bench30"
    day: Monday
    start: "15:00"
    end: "16:00"
    all_day: false
    recurring: true
  - title: "Moskiew Point Bench31"
    day: Tuesday
    start: "15:00"
    end: "16:00"
    all_day: false
    recurring: true
  - title: "Quaker Harbor Bench31"
    day: Wednesday
    start: "15:00"
    end: "16:00"
    all_day: false
    recurring: true
  - title: "Quaker Harbor Bench31"
    day: Thursday
    start: "15:00"
    end: "16:00"
    all_day: false
    recurring: true
  - title: "Forest Trail Bench32"
    day: Friday
    start: "15:00"
    end: "16:00"
    all_day: false
    recurring: true
  - title: "Quaker Woods Bench37"
    day: Monday
    start: "16:00"
    end: "17:00"
    all_day: false
    recurring: true
  - title: "Quaker Harbor Manufacturing Review Bench33"
    day: Friday
    start: "16:00"
    end: "17:30"
    all_day: false
    recurring: false

```
