# Contributing results

Thanks for running the Visual Calendar Comprehension Benchmark (VCCB)! This page
explains how to produce a valid submission and how to send it in.

## How to run

1. Get the `benchmark/` folder (clone this repo or download a release).
2. Read `benchmark/README.md` — especially **Isolation**: every image must be
   read in its own fresh session / sub-agent, with no information carried over
   from any other image. The same week is shown in every image, so a shared
   context lets a model copy answers from an easier image and invalidates the
   result.
3. Copy `benchmark/results/results-template.md`, fill in the metadata and the
   exact prompt you used, and paste each image's YAML output into its section.
   Fill in as many images as you can; partial submissions are welcome.

## What makes a submission valid

- **Isolation respected** — one independent run per image.
- **Real model output** — paste what the model produced. Do not hand-transcribe
  the calendar yourself, and do not edit the times afterwards.
- **Honest metadata** — the real `model` id (full Hugging Face path incl.
  lab/tuner + quant tag for local models), the real `server_command` (or service
  URL for hosted models), the **exact** prompt text you used, and a `submitter`
  tag (a public nickname, or a few random letters/digits if you prefer to stay
  anonymous).

Because the prompt and model are part of every submission, anyone can reproduce
your run. Submissions that cannot be reproduced, or that look implausible for
today's models (e.g. near-perfect minute-accurate starts on the 15° perspective
photos), may be flagged or removed.

## How to submit

Pick whichever is easier:

- **Pull request:** add your filled file to `submissions/` named
  `<model-slug>__<submitter>.md` (e.g. `qwen2-vl-7b-q8__alice.md`) so several
  people can submit results for the same model, and open a PR.
- **Issue:** open an issue and attach or paste your filled results file.

You do not compute your own score — the maintainer scores every submission
against the reference and regenerates `leaderboard.md`.

## Updating or completing a submission

To add the images you skipped, or to fix a run, **edit the same file** (keep the
metadata block unchanged) and submit again. A submission is identified by a hash
of its metadata — `model`, `submitter`, `run_date`, `server_command` and the
exact prompt — so a more complete file replaces your earlier one for those images
without double-counting what you already reported. The `submitter` tag is what
keeps two people who happened to use the same model and command from colliding
into one entry, so please set it. Changing any of those metadata fields makes it
a new, separate submission.

## Scope of a run

The official set is one fixed benchmark week rendered in three calendar
applications, captured as a frontal screenshot, a frontal photo, and a combined
~15° perspective photo per application (9 images). The combined perspective photo
is taken with the camera roughly **15° to the right of and 15° above the screen's
normal** (i.e. shooting the screen from the upper right). Scores are
self-normalized per application, so a flawless extraction reaches 100% regardless
of how much an application's rendering compresses.
