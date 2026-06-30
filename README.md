# Visual Calendar Comprehension Benchmark (VCCB)

How well can a multimodal model read a **calendar week view**? VCCB gives a model
fixed screenshots and photos of the same week rendered in Outlook, HCL Notes and
Thunderbird, and scores how accurately it extracts each event's **title, start,
end/duration, overlaps, recurrence and all-day/multi-day spans** — measured
against what a careful human could actually recover from each image, per
application.

It is image-based: a model receives fixed images and returns structured data.
Everything here is open — images, prompt, scorer and answer key — so you can run
it and check any number on the board yourself.

## Try it in 3 steps

1. Get the `benchmark/` folder.
2. Run your model on each image **in its own isolated session** (see
   `benchmark/README.md`) and fill in a copy of
   `benchmark/results/results-template.md`.
3. Score it: `python reference/evaluation/scorer.py --results your_file.md`

## Contribute to the leaderboard

Send your filled results file as a pull request into `submissions/` or as an
issue — see [`CONTRIBUTING.md`](CONTRIBUTING.md). The maintainer scores every
submission against the reference and regenerates [`leaderboard.md`](leaderboard.md).
Because the prompt and model are part of every submission, every number on the
board is reproducible — anyone with the same model and setup can re-run and check
it.

## What's here

```text
benchmark/      images, the extraction prompt, the results template   (what you run)
reference/      the answer key, manifest, scorer and scoring rules     (how it's scored)
submissions/    every submitted results file                           (the data)
leaderboard.md  generated from submissions/                            (the board)
CONTRIBUTING.md how to submit
```

`benchmark/` never contains the answers inline, so a model under test only ever
sees the image and the prompt — even though the answer key in `reference/` is
public. To score, you need `reference/`; to be ranked, you submit and the
maintainer scores centrally.

## What makes the scoring fair

- **Self-normalized per application:** a flawless extraction is 100% no matter
  how lossy an application's rendering is. Outlook clamps nothing but hides a
  short event's true start behind a precise accent bar; Notes/Thunderbird enforce
  a minimum block height. Each image is scored against its own *recoverable
  maximum*.
- **Robustness axis:** the same recoverable bands apply to the frontal and the
  ~15° perspective shots, so the perspective columns measure how much a model
  loses to capture distortion — not a change in what is there.
- **Hallucinations and misses (FP/FN)** are reported per image, never hidden in
  an average.

## Scope

**In scope:** week / work-week views; calendar screenshots and photographs;
title, start, end/duration extraction; overlap and recurrence interpretation;
all-day and multi-day events; perspective-distortion handling.

**Out of scope:** month and multi-week views; OCR-robustness benchmarking;
multilingual text; attendee / room / organizer extraction; calendar editing;
calendar rendering or generation.

## The dataset

One fixed benchmark week (Monday–Friday, dates far in the past to avoid clashes
with real calendars), shown in a 08:00–18:00 window, rendered in three
applications: **A = MS Outlook, B = HCL Notes, C = Mozilla Thunderbird**. Each
application is captured three ways, so the 9 images are named `A1…C3`:

1. a frontal screenshot,
2. a frontal photo of the screen,
3. a combined ~15° perspective photo — camera roughly **15° to the right of and
   15° above the screen's normal**.

The application/condition behind each filename lives in
`reference/benchmark_manifest.yaml`; the image filenames themselves carry only a
letter and a number, so a model under test is never told which app it is looking
at. To regenerate the images, import `reference/benchmark-week.ics` into each
app, set the week view and the 08:00–18:00 window, and capture the three shots.

The events are designed to exercise, as visual phenomena: a range of **durations**
from very short to multi-hour; minute-level **start offsets**; **identical-start**
and **offset overlaps**; **back-to-back** chains and dense vs sparse regions;
**horizontally compressed** overlaps; **cross-hour** boundaries; a **long,
truncating** title; a **recurring** event; and **all-day** single- and multi-day
events.

## Status

Research preview, one fixed week (9 images). The benchmark is generated from a
single source, so fresh, uncontaminated weeks can be minted later if the public
set ever needs rotating.

## License

See [`LICENSE`](LICENSE). Code is provided under the MIT license; the benchmark
images and reference data are provided under CC BY 4.0 (please confirm/adjust
before publishing).
