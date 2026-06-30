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
