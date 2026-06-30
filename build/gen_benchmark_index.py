#!/usr/bin/env python3
"""
gen_benchmark_index.py
Generate reference/benchmark_index.md FROM reference/ground_truth.yaml.

Human-readable reference: for every event it lists canonical values, the
per-client Recoverable Truth (Extractable Maximum) expanded from the client
profiles, the rationale, and the covered phenomena.

The per-client band derivation is imported from scorer.py so this document
always matches exactly what the scorer applies. DO NOT expose to evaluated
models (lives under reference/).
"""
import sys
import yaml

sys.path.insert(0, "reference/evaluation")
from scorer import derive_timed_bands  # noqa: E402  (single source for bands)

GT_PATH = "reference/ground_truth.yaml"
OUT = "reference/benchmark_index.md"

CLIENT_ORDER = ["outlook", "notes", "thunderbird"]
CLIENT_NAME = {"outlook": "Outlook", "notes": "HCL Notes",
               "thunderbird": "Thunderbird"}


def band(b):
    return "—" if b is None else f"{b[0]}–{b[1]}"


def emit():
    gt = yaml.safe_load(open(GT_PATH))
    profiles = gt["client_profiles"]
    bm = gt["benchmark"]
    L = []
    a = L.append

    a(f"# {bm['name']} ({bm['abbreviation']}) — Benchmark Index")
    a("")
    a(f"Version {bm['version']} · generated from `reference/ground_truth.yaml`. "
      "Human-readable reference of every event: canonical values, per-client "
      "Recoverable Truth (Extractable Maximum), rationale, and covered phenomena.")
    a("")
    a("> **Reference material — do NOT expose to evaluated models.** "
      "This file lives under `reference/` and reveals the answers and the "
      "recoverable bands.")
    a("")
    a(f"- **Week:** Mon {bm['week']['monday']} → Fri {bm['week']['friday']}")
    a(f"- **View window:** {bm['view_window']}")
    a(f"- **Canonical events:** {bm['canonical_events_count']}  ·  "
      f"**Visible blocks:** Outlook {bm['visible_blocks']['outlook']}, "
      f"Notes {bm['visible_blocks']['notes']}, "
      f"Thunderbird {bm['visible_blocks']['thunderbird']}")
    a(f"- **Recoverable-truth scope:** {bm['recoverable_truth_scope']}")
    a("")

    # --- client profile summary ---
    a("## Client capability profiles")
    a("")
    a("| Property | Outlook | HCL Notes | Thunderbird |")
    a("|---|---|---|---|")

    def prow(label, fn):
        a(f"| {label} | " + " | ".join(fn(profiles[c]) for c in CLIENT_ORDER) + " |")

    prow("Calibration", lambda p: str(p["calibration_status"]).split("(")[0].strip())
    prow("px per minute", lambda p: str(p["px_per_min"]))
    prow("Precise time indicator", lambda p: "yes" if p["precise_time_indicator"] else "no")
    prow("Clamp below (min)", lambda p: str(p["duration"]["clamp_below_min"]))
    prow("Clamped base band", lambda p: band(p["duration"]["clamped_base_band"]))
    prow("Duration tol base/bonus", lambda p: f"±{p['duration']['base_tol_min']}/±{p['duration']['bonus_tol_min']}")
    prow("Start tol base/bonus", lambda p: f"±{p['start']['base_tol_min']}/±{p['start']['bonus_tol_min']}")
    prow("Multi-day render", lambda p: p["multi_day_render"])
    prow("Recurrence icon", lambda p: "yes" if p["recurrence_icon"] else "no")
    a("")
    a("**How to read recoverable bands.** *Duration:* a prediction inside the "
      "base band earns base credit (80%); inside the bonus band earns full "
      "credit (100%). *clamped* = no bonus tier (the render cannot expose finer "
      "detail). *Start:* base = within ±base tol; bonus = within ±bonus tol; a "
      "✗ bonus is not reachable (clamp can displace the top edge) and is removed "
      "from the denominator. Self-normalization means a perfect extraction of "
      "any client's image scores 100%.")
    a("")
    a("---")
    a("")

    # --- per event ---
    for e in gt["events"]:
        c = e["canonical"]
        rcv = e["recoverable"]
        kind = e["kind"]
        a(f"## {e['id']} — {c['title']}  ({'all-day' if kind == 'all_day' else 'timed'})")
        a("")

        # canonical block
        a("**Canonical**")
        a("")
        if kind == "all_day":
            a(f"- Day(s): {c['day']} → +{c['span_days']-1} "
              f"(span {c['span_days']} days, {c['start_date']} … {c['end_date_inclusive']})")
            a("- All-day event (header band; no clock time)")
        else:
            rec = c["recurrence"]
            day = c["day"] if not rec else "recurring " + str(rec["byday"])
            a(f"- Day: {day}" + ("" if rec else f" ({c['date']})"))
            a(f"- Start: {c['start']}  ·  End: {c['end']}  ·  Duration: {c['duration_min']} min")
            if rec:
                a(f"- Recurrence: {rec['freq']} on {','.join(rec['byday'])}, "
                  f"count {rec['count']} (instances {rec['instances'][0]} … {rec['instances'][-1]})")
            else:
                a("- Recurrence: none")
        a("")

        # title (client-independent)
        tt = rcv["title"]
        a(f"**Title** — content words: *{' '.join(tt['content_words'])}*  ·  "
          f"id token: `{tt['id_token']}`  ·  "
          f"truncation expected: {str(tt['truncation_expected']).lower()}")
        a("")

        # recoverable per client
        a("**Recoverable per client**")
        a("")
        if kind == "all_day":
            a("| Client | Render | Start-day | Span | Accepted span forms |")
            a("|---|---|---|---|---|")
            for cl in CLIENT_ORDER:
                render = profiles[cl]["multi_day_render"]
                if c["span_days"] > 1:
                    forms = ("one span bar" if render == "span_bar"
                             else f"one {c['span_days']}-day event OR "
                                  f"{c['span_days']} adjacent same-title banners")
                else:
                    forms = "single-day banner"
                a(f"| {CLIENT_NAME[cl]} | {render} | {c['day']} (exact) | "
                  f"{c['span_days']} day(s) (exact) | {forms} |")
        else:
            a("| Client | Regime | Duration base | Duration bonus | Start base | Start bonus |")
            a("|---|---|---|---|---|---|")
            for cl in CLIENT_ORDER:
                dur, start = derive_timed_bands(c["duration_min"], profiles[cl])
                sb = f"±{start['bonus_tol_min']}" if start["bonus_achievable"] else "✗"
                a(f"| {CLIENT_NAME[cl]} | {dur['regime']} | "
                  f"{band(dur['base_band'])} | {band(dur['bonus_band'])} | "
                  f"±{start['base_tol_min']} | {sb} |")
        a("")

        # rationale
        rat = e["rationale"]
        a(f"**Purpose** — {rat['purpose']}")
        a("")
        a(f"**Phenomena** — {', '.join(rat['phenomena'])}")
        a("")
        a("---")
        a("")

    # --- phenomena coverage summary ---
    a("## Covered phenomena (summary)")
    a("")
    pheno = {}
    for e in gt["events"]:
        for p in e["rationale"]["phenomena"]:
            pheno.setdefault(p, []).append(e["id"])
    a("| Phenomenon | Events |")
    a("|---|---|")
    for p in sorted(pheno):
        a(f"| {p} | {', '.join(pheno[p])} |")
    a("")

    return "\n".join(L) + "\n"


if __name__ == "__main__":
    out = emit()
    with open(OUT, "w") as f:
        f.write(out)
    print(f"wrote {OUT} ({len(out)} bytes)")
