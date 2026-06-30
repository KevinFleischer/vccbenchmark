# Evaluation — scoring a benchmark run

This folder holds the scoring logic. It is part of `reference/` and **must never
be exposed to evaluated models**. Audience: the benchmark administrator.

## What you need

- Python 3 with `pyyaml` and `scipy` (`pip install pyyaml scipy`).
- A **filled results file**: a returned copy of
  `benchmark/results/results-template.md`, with one YAML block per image and the
  run metadata (model id, settings) at the top. The run produces this; you save
  it anywhere (e.g. a `runs/` folder).
- The reference files in this repo (`ground_truth.yaml`, `scoring_rules.yaml`,
  `benchmark_manifest.yaml`) — used automatically.

## How to score

From the repository root (or anywhere — paths default to this repo's
`reference/` files):

```bash
python reference/evaluation/scorer.py --results path/to/your_results_file.md
```

That is the whole workflow: **hand the filled results file to the script with
`--results`.** The scorer reads the `## Image <name>` sections, looks each image
up in `reference/benchmark_manifest.yaml` to find its application and capture
condition, scores every image against that application's Extractable Maximum, and
prints the result tables.

### Common variations

```bash
# combine several runs / models into one matrix
python reference/evaluation/scorer.py -r runs/model_a.md -r runs/model_b.md

# only the perspective-robustness view
python reference/evaluation/scorer.py -r runs/model_a.md --view condition

# breakdown for one model only
python reference/evaluation/scorer.py -r runs/model_a.md --view breakdown --model "unsloth/…:UD-Q4_K_XL"

# internal consistency check (no results file needed)
python reference/evaluation/scorer.py --selftest

# full option list
python reference/evaluation/scorer.py --help
```

Override the reference files with `--manifest`, `--ground-truth`, `--rules` if
you keep them elsewhere.

## Building the public leaderboard

The leaderboard is a **pure function of the `submissions/` folder** — recompute it
from scratch any time:

```bash
python reference/evaluation/scorer.py --submissions-dir submissions/ --out leaderboard.md
```

This reads every `*.md` in the folder, scores each against the reference, and
writes `leaderboard.md` (application scores, robustness by condition, reliability,
and a submissions index). Rows are grouped by **(model, prompt_hash)**, so two
prompts for the same model stay separate. Because the output depends only on the
files present, removing a faked submission and re-running cleanly erases it.

## Where results are stored (and do they persist?)

Yes — results persist. Each scored image is appended as a row to a **results
store**, by default `reference/evaluation/results_store.yaml`. The matrix is then
rendered from the **whole store**, so:

- **Previous runs are kept.** Score model A today and model B next week (separate
  invocations) and both appear in the matrix. New applications or conditions
  extend the store without invalidating existing cells.
- **Re-scoring is idempotent.** A run is identified by its results-file name (the
  stem, or `--run-id`). Re-running the same file replaces that run's rows instead
  of duplicating them.
- **Repeated runs are averaged.** Two *different* runs of the same model
  (different files / run ids) are averaged per cell.
- **View anytime without scoring:** run with no `--results` to print the current
  accumulated matrix from the store.
- **Don't want to persist?** Add `--no-store` to score the given file(s) ad-hoc
  and print to stdout without touching the store.
- **Manage the store:** `--list-runs` shows what's recorded; `--remove-run ID`
  deletes one run; `--store FILE` points at a different store (e.g. per project).

The store holds only scores and FP/FN counts (no answers); it lives under
`reference/` like everything else here.

## What you get

Three tables plus a reliability report:

1. **Application matrix** — model × application (Outlook / Notes / Thunderbird),
   averaged over capture conditions, with a **Total** = mean of the application
   columns that have data. Adding a new application later does not invalidate
   existing columns.
2. **Condition matrix** — model × capture condition (frontal screenshot, frontal
   photo, combined ~15° perspective), averaged over applications. This is where
   **perspective robustness** shows up: the same recoverable bands apply to every
   condition, so a drop here means the model lost accuracy to capture distortion.
3. **Breakdown** — for each model, condition × application, to locate exactly
   where a model is weak.
4. **Reliability** — any image with a hallucinated event (FP) or a missed event
   (FN). These are treated as serious; the table lists them explicitly so they
   are never hidden behind an average.

All numbers are percentages, self-normalized per application (a flawless
extraction scores 100% on any application), commercially rounded to 2 decimals.

## Notes

- **One run = one results file.** Different settings or prompts for the same
  model are different runs; score them separately (or together with multiple
  `-r`) and compare. The settings/prompt fields in the results metadata document
  what produced each run.
- Repeated runs of the exact same model+application+condition are averaged.
- The scorer matches predictions to ground truth by day, time, duration and
  title similarity — never by on-screen column order, and never requiring the
  `BenchNN` id (which truncates first). See `scoring_rules.yaml` and
  `../benchmark_index.md` for the full per-event reference.
