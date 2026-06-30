#!/usr/bin/env python3
"""
VCCB scorer.

Inputs
  reference/ground_truth.yaml              canonical data + per-client profiles
  reference/evaluation/scoring_rules.yaml  weights, tolerances, formulas
  predictions: one list of extracted events per image, plus the image->client map

Pipeline (per image)
  1. expand ground truth for the image's client (recurrence -> 5 instances;
     multi-day all-day handled per render mode)
  2. stage-1 assignment of predictions to GT (Hungarian, hard constraints)
  3. stage-2 component scoring (start / duration / title) with profile-derived
     bands, every score normalized against the client's EXTRACTABLE MAXIMUM
  4. robustness from EP = 1.0*FN + 1.5*FP ; recurrence recognition
  5. image_score = weighted sum of the five self-normalized sub-scores

Aggregation
  client cell  = mean over the client's images, then mean over repeated runs
  Total        = mean of the client columns that have data
All reported numbers use commercial rounding (half away from zero) to 2 dp.
"""
import math
import os
import hashlib
import difflib
from decimal import Decimal, ROUND_HALF_UP
import yaml

# Default reference paths resolved relative to THIS script's location
# (<root>/reference/evaluation/scorer.py), so the CLI works from any cwd.
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
GT_PATH = os.path.join(_ROOT, "reference", "ground_truth.yaml")
RULES_PATH = os.path.join(_ROOT, "reference", "evaluation", "scoring_rules.yaml")
MANIFEST_PATH = os.path.join(_ROOT, "reference", "benchmark_manifest.yaml")

DAY_INDEX = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4}
DAY_DATE = {"Monday": "2022-01-17", "Tuesday": "2022-01-18",
            "Wednesday": "2022-01-19", "Thursday": "2022-01-20",
            "Friday": "2022-01-21"}

# Capture conditions (orthogonal to the application). Same recoverable bands
# apply to every condition: perspective is an invertible transform, not a loss
# of information, so it is a robustness axis rather than a reduction of the
# extractable maximum.
CONDITIONS = ["frontal_screenshot", "frontal_photo", "perspective_combined"]


# ----------------------------------------------------------------------- utils
def round2(x):
    return float(Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def to_min(hhmm):
    h, m = str(hhmm).split(":")
    return int(h) * 60 + int(m)


def norm_words(title):
    return [w for w in str(title).replace("-", " ").split() if w]


def split_title(title, known_id=None):
    """Return (content_words, id_token-or-None) heuristically."""
    ws = norm_words(title)
    idt = None
    if ws and ws[-1].lower().startswith("bench"):
        idt = ws[-1]
        ws = ws[:-1]
    return ws, idt


# -------------------------------------------------------------- load reference
def load_reference(gt_path=None, rules_path=None):
    gt = yaml.safe_load(open(gt_path or GT_PATH))
    rules = yaml.safe_load(open(rules_path or RULES_PATH))
    return gt, rules


def load_results(path):
    """Parse a filled results-template.md into (meta, {image_id: [events]}).

    meta carries identification/run metadata plus 'extraction_prompt' (the exact
    prompt text the contributor used). image_id is the image name ('A1', ...).
    Each image's events list is the parsed YAML `events:` block; empty/absent
    sections yield [] and are skipped downstream.
    """
    import re
    txt = open(path).read()
    meta = {}
    head = re.split(r"^##\s+Image\s+", txt, maxsplit=1, flags=re.M)[0]
    mh = re.search(r"```yaml\s*(.*?)```", head, flags=re.S)
    if mh:
        try:
            meta = yaml.safe_load(mh.group(1)) or {}
        except yaml.YAMLError:
            meta = {}
    # the exact extraction prompt is wrapped in a 4-backtick fence so it can
    # itself contain ordinary ``` code fences (our prompt has ```yaml examples).
    pm = re.search(r"##\s+Extraction prompt used\b(.*)\Z", head, flags=re.S | re.I)
    if pm:
        fb = re.search(r"`{4}[^\n]*\n(.*?)\n`{4}", pm.group(1), flags=re.S)
        meta["extraction_prompt"] = (fb.group(1) if fb else pm.group(1)).strip()
    images = {}
    for m in re.finditer(r"^##\s+Image\s+(\w+)\s*$(.*?)(?=^##\s+Image\s+|\Z)",
                         txt, flags=re.M | re.S):
        img_id = m.group(1)
        body = m.group(2)
        yb = re.search(r"```yaml\s*(.*?)```", body, flags=re.S)
        events = []
        if yb:
            try:
                data = yaml.safe_load(yb.group(1)) or {}
                events = data.get("events") or []
            except yaml.YAMLError:
                events = []
        images[img_id] = events
    return meta, images


def _norm_text(t):
    """Whitespace-normalize text so trivial formatting differences do not change
    a hash."""
    return " ".join(str(t or "").split())


def prompt_hash(meta):
    p = _norm_text(meta.get("extraction_prompt", ""))
    return hashlib.sha256(p.encode("utf-8")).hexdigest()[:12] if p else "noprompt"


def submission_id(meta):
    """Identity of a submission = hash of its METADATA only (model, submitter,
    run_date, server_command, exact prompt) — never the measurements. The
    submitter tag keeps two people who used the same model and command from
    colliding; re-uploading the same metadata with more images completes the
    same submission instead of double-reporting."""
    key = "\n".join([
        _norm_text(meta.get("model", "")),
        _norm_text(meta.get("submitter", "")),
        _norm_text(meta.get("run_date", "")),
        _norm_text(meta.get("server_command", "")),
        _norm_text(meta.get("extraction_prompt", "")),
    ])
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:12]


def results_block(events):
    """Serialize a list of event dicts to the results YAML block (for tooling/tests)."""
    import io
    return yaml.safe_dump({"events": events}, sort_keys=False,
                          default_flow_style=False, allow_unicode=True)


def load_manifest(path):
    """image_id -> {client, condition}. Lives under reference/ (never exposed)."""
    data = yaml.safe_load(open(path)) or {}
    return data.get("images", {})


def measurements_from_results(meta, images, manifest):
    """Combine a parsed results file (meta + {image_id: events}) with the
    manifest into measurements for score_measurements()."""
    model = str(meta.get("model", "?")).strip()
    q = str(meta.get("quantization", "")).strip()   # legacy/optional
    if q and q.lower() not in model.lower():
        model = f"{model} {q}"
    out = []
    for img_id, events in images.items():
        if not events:
            continue  # empty/unfilled section -> skip (partial files are fine)
        info = manifest.get(img_id) or manifest.get(str(img_id))
        if not info:
            continue
        out.append({"model": model, "client": info["client"],
                    "condition": info["condition"], "events": events,
                    "image": img_id})
    return out


def derive_timed_bands(duration_min, profile):
    """Per-client recoverable bands + which bonus tiers are achievable."""
    d, s = profile["duration"], profile["start"]
    clamp = d["clamp_below_min"]
    clamped = (not profile["precise_time_indicator"]) and clamp > 0 and duration_min <= clamp
    if clamped:
        dur = {"regime": "clamped", "base_band": list(d["clamped_base_band"]),
               "bonus_band": None, "bonus_achievable": False}
    else:
        dur = {"regime": "linear",
               "base_band": [duration_min - d["base_tol_min"], duration_min + d["base_tol_min"]],
               "bonus_band": [duration_min - d["bonus_tol_min"], duration_min + d["bonus_tol_min"]],
               "bonus_achievable": True}
    start_bonus = not (clamped and s["clamp_displaces_start"])
    start = {"base_tol_min": s["base_tol_min"], "bonus_tol_min": s["bonus_tol_min"],
             "bonus_achievable": start_bonus}
    return dur, start


# -------------------------------------------------- expand GT for a given image
def expand_gt(gt, client):
    """Return list of GT event dicts for one (whole-week) image of `client`."""
    profile = gt["client_profiles"][client]
    out = []
    for e in gt["events"]:
        c = e["canonical"]
        cw = e["recoverable"]["title"]["content_words"]
        idt = e["recoverable"]["title"]["id_token"]
        trunc = e["recoverable"]["title"].get("truncation_expected", False)
        if e["kind"] == "all_day":
            sday = c["day"]
            span = c["span_days"]
            out.append({
                "id": e["id"], "kind": "all_day",
                "title": c["title"], "content_words": cw, "id_token": idt,
                "truncation_expected": trunc,
                "start_day": sday, "span_days": span,
                "days": [d for d in DAY_INDEX
                         if DAY_INDEX[sday] <= DAY_INDEX[d] < DAY_INDEX[sday] + span],
                "multi_day_render": profile["multi_day_render"],
            })
            continue
        rec = c["recurrence"]
        if rec:
            for inst in rec["instances"]:
                day = [d for d, dt in DAY_DATE.items() if dt == inst][0]
                dur, start = derive_timed_bands(c["duration_min"], profile)
                out.append({
                    "id": e["id"], "kind": "timed", "series_id": e["id"],
                    "recurring": True, "title": c["title"],
                    "content_words": cw, "id_token": idt,
                    "truncation_expected": trunc,
                    "day": day, "start_min": c["start_min"],
                    "duration_min": c["duration_min"],
                    "dur_band": dur, "start_band": start,
                })
        else:
            dur, start = derive_timed_bands(c["duration_min"], profile)
            out.append({
                "id": e["id"], "kind": "timed", "series_id": None,
                "recurring": False, "title": c["title"],
                "content_words": cw, "id_token": idt,
                "truncation_expected": trunc,
                "day": c["day"], "start_min": c["start_min"],
                "duration_min": c["duration_min"],
                "dur_band": dur, "start_band": start,
            })
    return out


# ------------------------------------------------------------- parse prediction
def parse_pred(ev):
    """Normalize one predicted event dict."""
    all_day = bool(ev.get("all_day", False))
    title = ev.get("title", "")
    cw, idt = split_title(title)
    day = ev.get("day")
    p = {"title": title, "content_words": cw, "id_token": idt,
         "all_day": all_day, "day": day, "recurring": bool(ev.get("recurring", False))}
    if all_day:
        p["span_days"] = int(ev.get("span_days", 1))
        sd = ev.get("start_day", day)
        base = DAY_INDEX.get(sd, 0)
        p["days"] = ev.get("days") or [d for d in DAY_INDEX
                                       if base <= DAY_INDEX[d] < base + p["span_days"]]
        p["start_day"] = sd
    else:
        s = ev.get("start")
        p["start_min"] = to_min(s) if s is not None else None
        if ev.get("duration_min") is not None:
            p["duration_min"] = int(ev["duration_min"])
        elif ev.get("end") is not None and s is not None:
            p["duration_min"] = to_min(ev["end"]) - to_min(s)
        else:
            p["duration_min"] = None
    return p


def expand_recurring_preds(preds, gt_series):
    """If the model gave ONE recurring event instead of enumerating the series,
    expand it to the series instances so the compact answer is not penalised as
    misses. If it already listed enough instances, leave them untouched."""
    if not gt_series:
        return preds
    s0 = gt_series[0]
    n = len(gt_series)

    def is_series(p):
        return ((not p["all_day"]) and p.get("start_min") is not None
                and abs(p["start_min"] - s0["start_min"]) <= 30
                and title_sim(p, s0) >= 0.5)

    series_preds = [p for p in preds if is_series(p)]
    others = [p for p in preds if not is_series(p)]
    if len(series_preds) >= n:
        return preds                      # enough instances already
    rec_rep = next((p for p in series_preds if p.get("recurring")), None)
    if rec_rep is None:
        return preds                      # no recurrence claimed -> missing days = FN
    expanded = []
    for g in gt_series:
        q = dict(rec_rep); q["day"] = g["day"]; q["start_min"] = g["start_min"]
        q["all_day"] = False
        expanded.append(q)
    return others + expanded


def merge_multiday_banners(preds, gt_allday):
    """Merge adjacent same-title all-day predictions into one spanning event
    (the per-day-banner representation) so they are not counted as extra FPs."""
    targets = [g for g in gt_allday if g["span_days"] > 1]
    if not targets:
        return preds
    out, consumed = [], set()
    for g in targets:
        group = [i for i, p in enumerate(preds)
                 if p["all_day"] and i not in consumed
                 and title_sim(p, g) >= 0.5
                 and set(p.get("days", [])) & set(g["days"])]
        if group:
            days = set()
            for i in group:
                days |= set(preds[i].get("days", []))
                consumed.add(i)
            rep = dict(preds[group[0]])
            rep["days"] = sorted(days, key=lambda d: DAY_INDEX[d])
            rep["span_days"] = len(days)
            rep["start_day"] = rep["days"][0]
            out.append(rep)
    out += [p for i, p in enumerate(preds) if i not in consumed]
    return out


# ----------------------------------------------------------------- similarity
def title_sim(pred, gt, fuzzy=0.8):
    """0..1 similarity used for matching cost and title scoring."""
    rec, _ = content_recall(pred.get("content_words", []), gt["content_words"], fuzzy)
    idm = pred.get("id_token") and gt.get("id_token") and \
        pred["id_token"].lower() == gt["id_token"].lower()
    return 0.85 * rec + 0.15 * (1.0 if idm else 0.0)


def content_recall(pred_words, gt_words, fuzzy=0.8):
    if not gt_words:
        return 1.0, True
    pred_l = [w.lower() for w in pred_words]
    hit = 0
    for gw in gt_words:
        g = gw.lower()
        best = max((difflib.SequenceMatcher(None, g, pw).ratio() for pw in pred_l),
                   default=0.0)
        if best >= fuzzy:
            hit += 1
    return hit / len(gt_words), (hit == len(gt_words))


# ------------------------------------------------------------------- matching
def match(preds, gts, rules):
    """Stage 1. Returns (pairs, fp_idx, fn_idx). pairs = list of (pi, gi)."""
    from scipy.optimize import linear_sum_assignment
    import numpy as np
    cw = rules["matching"]["cost_weights"]
    gate = next(h["start_gate_min"] for h in rules["matching"]["hard_constraints"]
                if isinstance(h, dict) and "start_gate_min" in h)
    BIG = 1e6
    n, m = len(preds), len(gts)
    if n == 0 or m == 0:
        return [], list(range(n)), list(range(m))
    C = np.full((n, m), BIG)
    for i, p in enumerate(preds):
        for j, g in enumerate(gts):
            if p["all_day"] != (g["kind"] == "all_day"):
                continue
            if p["all_day"]:
                if not (set(p.get("days", [])) & set(g["days"])):
                    continue
                C[i, j] = cw["title"] * (1 - title_sim(p, g))
            else:
                if p.get("day") != g["day"]:
                    continue
                if p.get("start_min") is None:
                    continue
                ds = abs(p["start_min"] - g["start_min"])
                if ds > gate:
                    continue
                dd = abs((p.get("duration_min") or 0) - g["duration_min"])
                C[i, j] = cw["start"] * ds + cw["duration"] * dd + \
                    cw["title"] * (1 - title_sim(p, g))
    ri, cj = linear_sum_assignment(C)
    pairs, mp, mg = [], set(), set()
    for i, j in zip(ri, cj):
        if C[i, j] < BIG:
            pairs.append((i, j)); mp.add(i); mg.add(j)
    fp = [i for i in range(n) if i not in mp]
    fn = [j for j in range(m) if j not in mg]
    return pairs, fp, fn


# -------------------------------------------------------------- pair scoring
def score_start(p, g, W):
    if g["kind"] == "all_day":
        ach = W
        got = W if (g["start_day"] in p.get("days", []) or p.get("start_day") == g["start_day"]) else 0
        return got, ach
    b = g["start_band"]
    ach = W * (1.0 if b["bonus_achievable"] else 0.8)
    d = abs((p.get("start_min") if p.get("start_min") is not None else 10**9) - g["start_min"])
    if b["bonus_achievable"] and d <= b["bonus_tol_min"]:
        got = W * 1.0
    elif d <= b["base_tol_min"]:
        got = W * 0.8
    else:
        got = 0.0
    return min(got, ach), ach


def score_duration(p, g, W):
    if g["kind"] == "all_day":
        ach = W
        got = W if p.get("span_days") == g["span_days"] else 0
        return got, ach
    b = g["dur_band"]
    pd = p.get("duration_min")
    if b["regime"] == "clamped":
        ach = W * 0.8
        got = W * 0.8 if (pd is not None and b["base_band"][0] <= pd <= b["base_band"][1]) else 0.0
    else:
        ach = W * 1.0
        if pd is None:
            got = 0.0
        elif b["bonus_band"][0] <= pd <= b["bonus_band"][1]:
            got = W * 1.0
        elif b["base_band"][0] <= pd <= b["base_band"][1]:
            got = W * 0.8
        else:
            got = 0.0
    return min(got, ach), ach


def _recall_truncated(pred_words, gt_words, fuzzy=0.8):
    """Recall for a title cut off by the rendering. Truncation removes text from
    the end, so the reader is credited for a correct *leading prefix* of the
    title words: each predicted word must match the title word in the same
    position (full fuzzy match, or a >=3-char prefix of it), and the reader may
    legitimately omit only the final word (it is the one most likely off screen).
    Reading the visible prefix correctly scores full; dropping a word that was
    actually visible, or getting an early word wrong, is still penalised."""
    if not gt_words:
        return 1.0, True
    matched = 0
    for i, pw in enumerate(pred_words):
        if i >= len(gt_words):
            break
        g = gt_words[i].lower()
        p = pw.lower()
        if difflib.SequenceMatcher(None, g, p).ratio() >= fuzzy:
            matched += 1
        elif len(p) >= 3 and (g.startswith(p) or p.startswith(g)):
            matched += 1
        else:
            break  # a leading word read wrong breaks the prefix
    need = max(1, len(gt_words) - 1)  # may omit only the final (cut) word
    if matched == len(pred_words) and matched >= need:
        return 1.0, True
    return matched / len(gt_words), False


def score_title(p, g, W, id_achievable=True):
    # A one-off event whose title is expected to truncate has its id code cut off
    # the visible end, so the code is not recoverable: require only the visible
    # content, credited by prefix, and put the full title weight on it.
    if g.get("truncation_expected") and not g.get("recurring"):
        rec, _ = _recall_truncated(p.get("content_words", []), g["content_words"])
        return W * rec, W
    rec, _ = content_recall(p.get("content_words", []), g["content_words"])
    idm = (p.get("id_token") and g.get("id_token")
           and p["id_token"].lower() == g["id_token"].lower())
    ach = W * 0.8 + (W * 0.2 if id_achievable else 0.0)
    got = W * 0.8 * rec + (W * 0.2 if (idm and id_achievable) else 0.0)
    return got, ach


# ------------------------------------------------------------- recurrence score
def recurrence_score(preds, pairs, gts):
    series = [j for j, g in enumerate(gts) if g.get("recurring")]
    if not series:
        return 1.0
    g2p = {j: i for i, j in pairs}
    # explicit recurrence flag on any matched series instance?
    for j in series:
        i = g2p.get(j)
        if i is not None and preds[i].get("recurring"):
            return 1.0
    # implicit: matched instances sharing title+time across distinct days
    key = {}
    for j in series:
        i = g2p.get(j)
        if i is None:
            continue
        p = preds[i]
        k = (tuple(w.lower() for w in p.get("content_words", [])), p.get("start_min"))
        key.setdefault(k, set()).add(g_day(gts[j]))
    best = max((len(v) for v in key.values()), default=0)
    return min(best, len(series)) / len(series)


def g_day(g):
    return g["day"] if g["kind"] == "timed" else g.get("start_day")


# ------------------------------------------------------------- score one image
def score_image(pred_events, client, gt, rules):
    W = rules["weights"]
    gts = expand_gt(gt, client)
    preds = [parse_pred(e) for e in pred_events]
    gt_series = [g for g in gts if g.get("recurring")]
    gt_allday = [g for g in gts if g["kind"] == "all_day"]
    preds = expand_recurring_preds(preds, gt_series)
    preds = merge_multiday_banners(preds, gt_allday)

    pairs, fp, fn = match(preds, gts, rules)

    a_s = p_s = a_d = p_d = a_t = p_t = 0.0
    matched_g = set()
    for pi, gj in pairs:
        matched_g.add(gj)
        gs, ps_ = score_start(preds[pi], gts[gj], W["start"]); a_s += gs; p_s += ps_
        gd, pd_ = score_duration(preds[pi], gts[gj], W["duration"]); a_d += gd; p_d += pd_
        gt_, pt_ = score_title(preds[pi], gts[gj], W["title"]); a_t += gt_; p_t += pt_
    # unmatched GT (FN): achievable counted, achieved 0  -> lowers components too
    for gj in range(len(gts)):
        if gj in matched_g:
            continue
        g = gts[gj]
        if g["kind"] == "all_day":
            p_s += W["start"]; p_d += W["duration"]; p_t += W["title"] * 1.0
        else:
            p_s += W["start"] * (1.0 if g["start_band"]["bonus_achievable"] else 0.8)
            p_d += W["duration"] * (1.0 if g["dur_band"]["regime"] == "linear" else 0.8)
            p_t += W["title"] * 1.0

    S_start = a_s / p_s if p_s else 1.0
    S_dur = a_d / p_d if p_d else 1.0
    S_title = a_t / p_t if p_t else 1.0

    EP = 1.0 * len(fn) + 1.5 * len(fp)
    S_rob = 1.0 / (3 ** EP)
    S_rec = recurrence_score(preds, pairs, gts)

    img = (0.30 * S_start + 0.25 * S_dur + 0.20 * S_title
           + 0.15 * S_rob + 0.10 * S_rec)
    return {
        "image_score": round2(img * 100),
        "S_start": round2(S_start * 100), "S_duration": round2(S_dur * 100),
        "S_title": round2(S_title * 100),
        "robustness": round2(W["robustness"] * S_rob),
        "S_recurrence": round2(S_rec * 100),
        "FP": len(fp), "FN": len(fn), "EP": EP,
        "reliable": (len(fp) == 0 and len(fn) == 0),
    }


# ------------------------------------------------------------------- aggregate
def score_measurements(measurements, gt, rules):
    """measurements: list of {model, client, condition, events}.
    Returns a cube: {(model, client, condition): [image_score, ...]} (a list,
    so repeated runs of the same cell are kept for averaging)."""
    cube = {}
    for m in measurements:
        s = score_image(m["events"], m["client"], gt, rules)["image_score"]
        cube.setdefault((m["model"], m["client"], m["condition"]), []).append(s)
    return cube


def _mean(xs):
    return round2(sum(xs) / len(xs)) if xs else None


def _present_mean(vals):
    vs = [v for v in vals if v is not None]
    return round2(sum(vs) / len(vs)) if vs else None


def app_matrix(cube, clients=("outlook", "notes", "thunderbird")):
    """Headline view: model x application. Each cell = mean over conditions of
    the per-condition mean (so repeated runs and uneven condition coverage do
    not skew the cell)."""
    models = sorted({k[0] for k in cube})
    rows = []
    for mod in models:
        row = {"model": mod}
        for c in clients:
            per_cond = [_mean(cube[(mod, c, cond)]) for cond in CONDITIONS
                        if cube.get((mod, c, cond))]
            row[c] = _present_mean(per_cond)
        row["Total"] = _present_mean([row[c] for c in clients])
        rows.append(row)
    return rows, list(clients)


def condition_matrix(cube, conditions=tuple(CONDITIONS)):
    """Robustness view: model x capture condition. Each cell = mean over apps of
    the per-app mean."""
    models = sorted({k[0] for k in cube})
    rows = []
    for mod in models:
        row = {"model": mod}
        for cond in conditions:
            per_app = [_mean(cube[(mod, c, cond)])
                       for c in ("outlook", "notes", "thunderbird")
                       if cube.get((mod, c, cond))]
            row[cond] = _present_mean(per_app)
        row["Total"] = _present_mean([row[cond] for cond in conditions])
        rows.append(row)
    return rows, list(conditions)


def breakdown(cube, model, clients=("outlook", "notes", "thunderbird"),
              conditions=tuple(CONDITIONS)):
    """Detail view for one model: rows = condition, cols = application."""
    rows = []
    for cond in conditions:
        row = {"condition": cond}
        for c in clients:
            row[c] = _mean(cube.get((model, c, cond), []))
        row["row_mean"] = _present_mean([row[c] for c in clients])
        rows.append(row)
    return rows, list(clients)


def _fmt(v):
    return "—" if v is None else f"{v:.2f}%"


def render(rows, key, cols, header=None):
    """Generic markdown table renderer. key = first-column field name."""
    head = [header or key] + ["Total"] * ("Total" in rows[0]) + \
           [c.replace("_", " ") for c in cols if c != "Total"]
    # build header preserving Total placement right after the label
    columns = [key] + (["Total"] if "Total" in rows[0] else []) + list(cols)
    titles = [header or key.capitalize()] + \
             (["Total"] if "Total" in rows[0] else []) + \
             [c.replace("_", " ").title() for c in cols]
    out = ["| " + " | ".join(titles) + " |",
           "|" + "|".join(["---"] * len(titles)) + "|"]
    for r in rows:
        cells = [str(r[key])] + ([_fmt(r["Total"])] if "Total" in r else []) + \
                [_fmt(r.get(c)) for c in cols]
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


# ----------------------------------------------------------------------- tests
def _perfect_pred(gt, client):
    """Build a flawless prediction for one image of `client`."""
    gts = expand_gt(gt, client)
    profile = gt["client_profiles"][client]
    preds, seen_series = [], False
    for g in gts:
        if g["kind"] == "all_day":
            if profile["multi_day_render"] == "per_day_banner" and g["span_days"] > 1:
                for d in g["days"]:
                    preds.append({"title": g["title"], "all_day": True,
                                  "start_day": d, "span_days": 1, "days": [d]})
            else:
                preds.append({"title": g["title"], "all_day": True,
                              "start_day": g["start_day"], "span_days": g["span_days"],
                              "days": g["days"]})
        else:
            sm = g["start_min"]
            preds.append({"title": g["title"], "day": g["day"],
                          "start": f"{sm//60:02d}:{sm%60:02d}",
                          "duration_min": g["duration_min"],
                          "recurring": g["recurring"]})
    return preds


def run_selftest():
    gt, rules = load_reference()
    print("=== self-test: perfect extraction should score ~100% per client ===")
    for c in ("outlook", "notes", "thunderbird"):
        r = score_image(_perfect_pred(gt, c), c, gt, rules)
        print(f"  {c:12} image={r['image_score']:.2f}%  start={r['S_start']} "
              f"dur={r['S_duration']} title={r['S_title']} rob={r['robustness']} "
              f"rec={r['S_recurrence']}  FP={r['FP']} FN={r['FN']} reliable={r['reliable']}")

    print("\n=== degraded: drop 1 event, shift 1 start +40min, wrong 1 title ===")
    pred = _perfect_pred(gt, "outlook")
    pred = pred[1:]                              # drop first event -> 1 FN
    for p in pred:
        if p.get("day") == "Monday" and p.get("start") == "10:00":
            p["start"] = "10:40"                 # +40 min on Comet Ridge
        if p.get("title", "").startswith("Falcon Point"):
            p["title"] = "Wrong Title Bench06"   # wrong content words
    r = score_image(pred, "outlook", gt, rules)
    print(f"  outlook image={r['image_score']:.2f}%  start={r['S_start']} "
          f"dur={r['S_duration']} title={r['S_title']} rob={r['robustness']} "
          f"rec={r['S_recurrence']}  FP={r['FP']} FN={r['FN']} reliable={r['reliable']}")

    print("\n=== views over the per-image cube (model x app x condition) ===")
    # synthetic measurements: ModelA perfect everywhere; ModelB perfect on
    # frontal but degrades under perspective (robustness gap).
    meas = []
    perfect = {c: _perfect_pred(gt, c) for c in ("outlook", "notes", "thunderbird")}
    for c in ("outlook", "notes", "thunderbird"):
        for cond in CONDITIONS:
            meas.append({"model": "ModelA-Q4", "client": c, "condition": cond,
                         "events": perfect[c]})
    for c in ("outlook", "notes", "thunderbird"):
        for cond in CONDITIONS:
            ev = perfect[c] if cond in ("frontal_screenshot", "frontal_photo") \
                else pred if c == "outlook" else perfect[c][2:]  # drop 2 -> FN under perspective
            meas.append({"model": "ModelB-Q8", "client": c, "condition": cond,
                         "events": ev})
    cube = score_measurements(meas, gt, rules)

    am, clients = app_matrix(cube)
    print("\n[1] Headline — model x application (mean over conditions):")
    print(render(am, "model", clients, header="Model+Quant"))

    cm, conds = condition_matrix(cube)
    print("\n[2] Robustness — model x capture condition (mean over apps):")
    print(render(cm, "model", conds, header="Model+Quant"))

    bd, clients = breakdown(cube, "ModelB-Q8")
    print("\n[3] Breakdown for ModelB-Q8 — condition x application:")
    print(render(bd, "condition", clients + ["row_mean"], header="Condition"))


# ----------------------------------------------------------------- leaderboard
def dedup_records(records):
    """Keep one record per (submission, image); later occurrences win. Safety net
    for a submissions/ folder that holds more than one file for a submission."""
    seen = {}
    for r in records:
        seen[(r.get("run"), r["image"])] = r
    return list(seen.values())


def _entity_cube(records):
    """cube keyed by ((model, prompt_hash), client, condition) -> [scores]."""
    cube = {}
    for r in records:
        ent = (r["model"], r.get("prompt_hash", "noprompt"))
        cube.setdefault((ent, r["client"], r["condition"]), []).append(r["score"])
    return cube


def _phash_disp(h):
    return "—" if h in (None, "", "noprompt") else h[:8]


def build_leaderboard(records, title="VCCB Leaderboard"):
    """Render the public leaderboard markdown from all submission records. Rows
    are (model, prompt_hash): different prompts for one model stay distinct."""
    from datetime import datetime, timezone
    records = dedup_records(records)
    cube = _entity_cube(records)
    clients = ("outlook", "notes", "thunderbird")
    ents = sorted({(r["model"], r.get("prompt_hash", "noprompt")) for r in records})

    def app_cell(ent, c):
        per = [_mean(cube[(ent, c, cond)]) for cond in CONDITIONS
               if cube.get((ent, c, cond))]
        return _present_mean(per)

    def cond_cell(ent, cond):
        per = [_mean(cube[(ent, c, cond)]) for c in clients
               if cube.get((ent, c, cond))]
        return _present_mean(per)

    rows = []
    for ent in ents:
        apps = {c: app_cell(ent, c) for c in clients}
        rows.append((ent, _present_mean(list(apps.values())), apps))
    rows.sort(key=lambda x: (x[1] is None, -(x[1] or 0)))

    nsub = len({r["run"] for r in records})
    out = [f"# {title}", "",
           f"_Generated {datetime.now(timezone.utc):%Y-%m-%d %H:%M UTC} from "
           f"{len(records)} scored images across {nsub} submission(s)._", "",
           "Scores are self-normalized per application (a flawless extraction = "
           "100%). Rows are kept separate per model **and** per prompt.", ""]

    out += ["## Application scores", "",
            "| Model | Prompt | Total | Outlook | Notes | Thunderbird |",
            "|---|---|---|---|---|---|"]
    for (model, ph), total, apps in rows:
        out.append(f"| {model} | {_phash_disp(ph)} | {_fmt(total)} | "
                   f"{_fmt(apps['outlook'])} | {_fmt(apps['notes'])} | "
                   f"{_fmt(apps['thunderbird'])} |")

    out += ["", "## Robustness by capture condition", "",
            "| Model | Prompt | " + " | ".join(c.replace('_', ' ').title()
                                               for c in CONDITIONS) + " |",
            "|---|---|" + "|".join(["---"] * len(CONDITIONS)) + "|"]
    for ent, _t, _a in rows:
        model, ph = ent
        cells = " | ".join(_fmt(cond_cell(ent, cond)) for cond in CONDITIONS)
        out.append(f"| {model} | {_phash_disp(ph)} | {cells} |")

    bad = [r for r in records if r.get("fp", 0) or r.get("fn", 0)]
    if bad:
        out += ["", "## Reliability — hallucinations (FP) / misses (FN)", "",
                "| Model | Prompt | Image | App | Condition | FP | FN |",
                "|---|---|---|---|---|---|---|"]
        for r in sorted(bad, key=lambda x: (x["model"], x["image"])):
            out.append(f"| {r['model']} | {_phash_disp(r.get('prompt_hash'))} | "
                       f"{r['image']} | {r['client']} | {r['condition']} | "
                       f"{r.get('fp', 0)} | {r.get('fn', 0)} |")

    subs = {}
    for r in records:
        s = subs.setdefault(r["run"], {"model": r["model"],
                                       "prompt_hash": r.get("prompt_hash"),
                                       "submitter": r.get("submitter", ""),
                                       "run_date": r.get("run_date", ""), "n": 0})
        s["n"] += 1
    out += ["", "## Submissions", "",
            "| Submission | Submitter | Model | Prompt | Run date | Images |",
            "|---|---|---|---|---|---|"]
    for sid, s in sorted(subs.items()):
        out.append(f"| `{sid}` | {s['submitter'] or '—'} | {s['model']} | "
                   f"{_phash_disp(s['prompt_hash'])} | {s['run_date'] or '—'} | "
                   f"{s['n']} |")

    return "\n".join(out) + "\n"


# --------------------------------------------------------------- results store
def load_store(path):
    """Persistent per-image score log. Returns a list of records."""
    if not os.path.exists(path):
        return []
    data = yaml.safe_load(open(path)) or {}
    return data.get("measurements", [])


def save_store(path, records):
    with open(path, "w") as fh:
        yaml.safe_dump({"measurements": records}, fh, sort_keys=False,
                       allow_unicode=True)


def upsert_run(records, run_id, new_records):
    """Replace any existing records of run_id with new_records (idempotent
    re-ingestion); other runs are kept and later averaged into the cells."""
    kept = [r for r in records if r.get("run") != run_id]
    return kept + new_records


def merge_records(records, new_records):
    """Merge new records into the store per (submission, image): a re-upload of
    the same submission completes/updates its own images and never duplicates an
    already-reported value, while other submissions stay untouched."""
    incoming = {(r["run"], r["image"]) for r in new_records}
    kept = [r for r in records if (r.get("run"), r.get("image")) not in incoming]
    return kept + new_records


def records_to_cube(records):
    cube = {}
    for r in records:
        cube.setdefault((r["model"], r["client"], r["condition"]), []).append(r["score"])
    return cube


def score_to_records(paths, manifest, gt, rules, run_id=None):
    """Score results file(s) into per-image records. The submission identity
    ('run') is the metadata hash, so re-uploads with the same metadata complete
    the same submission per image instead of double-reporting."""
    out = []
    for p in paths:
        meta, images = load_results(p)
        rid = run_id or submission_id(meta)
        phash = prompt_hash(meta)
        meas = measurements_from_results(meta, images, manifest)
        if not meas:
            print(f"  ! {p}: no filled image sections matched the manifest — skipped.")
        for m in meas:
            res = score_image(m["events"], m["client"], gt, rules)
            out.append({"model": m["model"], "image": m["image"],
                        "client": m["client"], "condition": m["condition"],
                        "score": res["image_score"], "fp": res["FP"],
                        "fn": res["FN"], "run": rid, "prompt_hash": phash,
                        "run_date": _norm_text(meta.get("run_date", "")),
                        "submitter": _norm_text(meta.get("submitter", "")),
                        "source": os.path.basename(p)})
    return out


# ----------------------------------------------------------------------- CLI
DEFAULT_STORE = os.path.join(_HERE, "results_store.yaml")


def _print_views(cube, view, model=None):
    if view in ("app", "all"):
        am, cl = app_matrix(cube)
        print("\n## Application matrix  (model × application, mean over conditions)\n")
        print(render(am, "model", cl, header="Model"))
    if view in ("condition", "all"):
        cm, cd = condition_matrix(cube)
        print("\n## Condition matrix  (model × capture condition, mean over apps)\n")
        print(render(cm, "model", cd, header="Model"))
    if view in ("breakdown", "all"):
        for mod in ([model] if model else sorted({k[0] for k in cube})):
            bd, cl = breakdown(cube, mod)
            print(f"\n## Breakdown — {mod}  (condition × application)\n")
            print(render(bd, "condition", cl + ["row_mean"], header="Condition"))


def cli():
    import argparse
    ap = argparse.ArgumentParser(
        prog="scorer.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="VCCB scorer — score filled results file(s) into the results "
                    "matrix. Scores accumulate in a persistent store.",
        epilog=(
            "WHERE RESULTS ARE STORED\n"
            "  Per-image scores are appended to the results store (default:\n"
            "  reference/evaluation/results_store.yaml). The matrix is rendered\n"
            "  from the whole store, so earlier runs are kept and new models /\n"
            "  applications / conditions extend it without invalidating anything.\n"
            "  Re-scoring a file reuses its run id (the file stem) and REPLACES\n"
            "  that run's rows; different runs of one model are averaged per cell.\n\n"
            "WHERE THE RESULTS FILE COMES FROM\n"
            "  A run fills a copy of benchmark/results/results-template.md and\n"
            "  returns it. Save it anywhere and pass its path with --results.\n\n"
            "EXAMPLES\n"
            "  # score a run, store it, print the accumulated matrix\n"
            "  python reference/evaluation/scorer.py --results runs/gemma_q4.md\n\n"
            "  # just view the current standings (no new scoring)\n"
            "  python reference/evaluation/scorer.py\n\n"
            "  # score without persisting (ad-hoc, stdout only)\n"
            "  python reference/evaluation/scorer.py -r runs/gemma_q4.md --no-store\n\n"
            "  # store management\n"
            "  python reference/evaluation/scorer.py --list-runs\n"
            "  python reference/evaluation/scorer.py --remove-run gemma_q4\n"))
    ap.add_argument("-r", "--results", action="append", metavar="FILE",
                    help="A filled results file. Repeat to score several at once.")
    ap.add_argument("--submissions-dir", metavar="DIR",
                    help="Recompute a leaderboard from every *.md in DIR (fresh, "
                         "ignores the store) and write it to --out.")
    ap.add_argument("--out", metavar="FILE", default="leaderboard.md",
                    help="Leaderboard output path for --submissions-dir "
                         "(default: leaderboard.md).")
    ap.add_argument("--run-id", metavar="ID",
                    help="Run id for the given results file(s) "
                         "(default: each file's name without extension).")
    ap.add_argument("--store", default=DEFAULT_STORE, metavar="FILE",
                    help="results store (default: reference/evaluation/results_store.yaml)")
    ap.add_argument("--no-store", action="store_true",
                    help="do not read or write the store; score the given files only")
    ap.add_argument("--list-runs", action="store_true",
                    help="list the runs currently in the store and exit")
    ap.add_argument("--remove-run", metavar="ID",
                    help="delete a run from the store and exit")
    ap.add_argument("--manifest", default=MANIFEST_PATH, metavar="FILE")
    ap.add_argument("--ground-truth", dest="gt", default=GT_PATH, metavar="FILE")
    ap.add_argument("--rules", default=RULES_PATH, metavar="FILE")
    ap.add_argument("--view", choices=["app", "condition", "breakdown", "all"],
                    default="all", help="which table(s) to print (default: all)")
    ap.add_argument("--model", metavar="NAME",
                    help="restrict the breakdown view to one model")
    ap.add_argument("--selftest", action="store_true",
                    help="run internal tests instead of scoring")
    args = ap.parse_args()

    if args.selftest:
        run_selftest()
        return

    if args.submissions_dir:
        import glob
        gt, rules = load_reference(args.gt, args.rules)
        manifest = load_manifest(args.manifest)
        files = sorted(glob.glob(os.path.join(args.submissions_dir, "*.md")))
        if not files:
            print(f"No *.md files in {args.submissions_dir}.")
            return
        recs = dedup_records(score_to_records(files, manifest, gt, rules))
        if not recs:
            print(f"No scorable submissions in {args.submissions_dir} "
                  "(every file was empty or unmatched).")
            return
        md = build_leaderboard(recs)
        with open(args.out, "w") as fh:
            fh.write(md)
        print(md)
        print(f"\nWrote {args.out} — {len(recs)} scored images across "
              f"{len({r['run'] for r in recs})} submission(s).")
        return

    records = [] if args.no_store else load_store(args.store)

    if args.list_runs:
        runs = {}
        for r in records:
            runs.setdefault(r["run"], set()).add(
                f'{r["model"]}  [prompt {r.get("prompt_hash", "?")}]')
        if not runs:
            print(f"Store is empty ({args.store}).")
        else:
            print(f"Submissions in {args.store}:")
            for rid, models in sorted(runs.items()):
                print(f"  {rid}: {', '.join(sorted(models))}")
        return

    if args.remove_run:
        before = len(records)
        records = [r for r in records if r.get("run") != args.remove_run]
        save_store(args.store, records)
        print(f"Removed run '{args.remove_run}' "
              f"({before - len(records)} rows). Store now has {len(records)} rows.")
        return

    if args.results:
        gt, rules = load_reference(args.gt, args.rules)
        manifest = load_manifest(args.manifest)
        new = score_to_records(args.results, manifest, gt, rules, run_id=args.run_id)
        if not new:
            print("No measurements produced. Check that the '## Image <name>' "
                  "sections match the manifest keys "
                  f"({', '.join(sorted(manifest)[:5])}…).")
            return
        if args.no_store:
            records = new
        else:
            records = merge_records(records, new)
            save_store(args.store, records)
            subs = ", ".join(sorted({r["run"] for r in new}))
            print(f"Stored {len(new)} image score(s) for submission(s): {subs}.")
            print(f"Store now holds {len(records)} rows at {args.store}.")
    elif not records:
        ap.print_help()
        print("\nNothing to score and the store is empty: pass --results FILE.")
        return

    cube = records_to_cube(records)
    _print_views(cube, args.view, args.model)

    bad = [r for r in records if r.get("fp", 0) or r.get("fn", 0)]
    if bad:
        print("\n## Reliability — images with hallucinations (FP) or misses (FN)\n")
        print("| Model | Run | Image | App | Condition | FP | FN |")
        print("|---|---|---|---|---|---|---|")
        for d in sorted(bad, key=lambda x: (x["model"], x["run"], x["image"])):
            print(f"| {d['model']} | {d['run']} | {d['image']} | {d['client']} | "
                  f"{d['condition']} | {d.get('fp', 0)} | {d.get('fn', 0)} |")
    else:
        print("\nAll scored images were reliable (no FP/FN).")


if __name__ == "__main__":
    cli()
