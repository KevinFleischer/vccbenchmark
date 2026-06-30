# Submissions

Every file here is one benchmark submission: a filled copy of
`benchmark/results/results-template.md`. The leaderboard is generated **only**
from this folder, so it is fully reproducible and a faked entry can be removed by
deleting its file and recomputing.

- Name files `<model-slug>__<submitter>.md` (e.g. `qwen2-vl-7b-q8__alice.md`). One file per
  submission; edit it in place to complete or correct a run.
- The maintainer regenerates the leaderboard with:

  ```bash
  python reference/evaluation/scorer.py --submissions-dir submissions/ --out leaderboard.md
  ```

See `../CONTRIBUTING.md` for how to produce and send a valid submission.
