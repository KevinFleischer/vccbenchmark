#!/usr/bin/env python3
"""
author_ground_truth.py  --  one-time authoring aid for VCCB.

Holds the canonical benchmark week as a compact table, applies the
documented derivation rules for Recoverable Truth (Extractable Maximum),
and emits reference/ground_truth.yaml as a human-readable, ordered file.

ground_truth.yaml is the SINGLE SOURCE OF TRUTH afterwards:
benchmark-week.ics and benchmark_index.md are generated FROM it.
"""

# ---------------------------------------------------------------------------
# CALIBRATION CONSTANTS  (PROVISIONAL -- measure from the first real photos)
# ---------------------------------------------------------------------------
CAL = {
    "view_start": "08:00",
    "view_end":   "18:00",
    # Durations <= D_CLAMP render at the client's minimum row height and are
    # therefore visually indistinguishable from each other ("short class").
    # MEASURED from first screenshots (2022-01 week):
    #   Outlook: linear region = 1.00 px/min; clamp floor 29 px => ~30 min.
    #   Notes:   clamp floor ~19-20 px => ~30-33 min.
    #   => 15, 20 AND 30 min all render at the floor in BOTH clients.
    "D_clamp_min": 30,
    # "Short class" credit window for clamped events (no precision bonus).
    "clamped_base_band_min": 5,
    "clamped_base_band_max": 30,
    # Absolute tolerances for non-clamped (linear) events.
    "duration_base_tol_min": 15,
    "duration_bonus_tol_min": 5,
    # Start time is read from the TOP edge -> unaffected by height clamping,
    # so a single uniform tolerance applies to every event.
    "start_base_tol_min": 15,
    "start_bonus_tol_min": 5,
}

# ---------------------------------------------------------------------------
# CANONICAL WEEK  (id, title, day, date, start, end, recurrence)
# ---------------------------------------------------------------------------
MON, TUE, WED, THU, FRI = (
    ("Monday", "2022-01-17"), ("Tuesday", "2022-01-18"),
    ("Wednesday", "2022-01-19"), ("Thursday", "2022-01-20"),
    ("Friday", "2022-01-21"),
)

# recurrence=None for single events; for Bench20 a dict describes the series.
EVENTS = [
    # -- Monday: duration coverage --------------------------------------
    ("Bench01", "Anchor Flow Bench01",   MON, "08:00", "08:15", None),
    ("Bench02", "Birch Wave Bench02",    MON, "09:00", "09:20", None),
    ("Bench03", "Comet Ridge Bench03",   MON, "10:00", "10:30", None),
    ("Bench04", "Dune Harbor Bench04",   MON, "11:00", "11:45", None),
    ("Bench05", "Elm Sector Bench05",    MON, "13:00", "13:55", None),
    ("Bench06", "Falcon Point Bench06",  MON, "15:00", "16:00", None),
    ("Bench07", "Glacier Route Bench07", MON, "16:30", "17:35", None),  # moved
    # -- Tuesday: start-time offset coverage ----------------------------
    ("Bench08", "Harbor Crest Bench08",  TUE, "08:05", "09:05", None),
    ("Bench09", "Island Grove Bench09",  TUE, "09:15", "10:15", None),
    ("Bench10", "Jasper Field Bench10",  TUE, "10:30", "11:30", None),
    ("Bench11", "Kestrel Bay Bench11",   TUE, "11:45", "12:45", None),
    ("Bench12", "Lantern Peak Bench12",  TUE, "13:55", "14:55", None),
    ("Bench13", "Meadow Point Bench13",  TUE, "15:05", "16:20", None),
    # -- Wednesday: overlaps --------------------------------------------
    ("Bench14", "Nimbus Trail Bench14",  WED, "09:00", "09:30", None),
    ("Bench15", "Orion Gate Bench15",    WED, "09:00", "10:00", None),
    ("Bench16", "Prairie Stone Bench16", WED, "09:00", "11:00", None),
    ("Bench17", "Quartz Harbor Bench17", WED, "14:00", "16:00", None),
    ("Bench18", "Raven Point Bench18",   WED, "14:30", "15:15", None),
    ("Bench19", "Summit Ridge Bench19",  WED, "15:00", "16:30", None),
    # -- recurring event (collision-free slot 12:45-13:00 Mon-Fri) ------
    ("Bench20", "Tanner Grove Bench20",  MON, "12:45", "13:00",
        {"freq": "WEEKLY", "byday": ["MO", "TU", "WE", "TH", "FR"],
         "count": 5,
         "instances": ["2022-01-17", "2022-01-18", "2022-01-19",
                       "2022-01-20", "2022-01-21"]}),
    # -- Thursday: compression ------------------------------------------
    ("Bench21", "Umbra Valley Bench21",    THU, "09:00", "11:00", None),
    ("Bench22", "Vertex Harbor Bench22",   THU, "09:05", "10:55", None),
    ("Bench23", "Willow Crossing Bench23", THU, "09:10", "11:05", None),
    # -- Friday: dense layout -------------------------------------------
    ("Bench24", "Xenon Bridge Bench24",  FRI, "08:00", "08:30", None),
    ("Bench25", "Yonder Creek Bench25",  FRI, "08:30", "09:00", None),
    ("Bench26", "Zenith Point Bench26",  FRI, "09:00", "09:30", None),
    ("Bench27", "Aspen Harbor Bench27",  FRI, "09:30", "10:00", None),
    ("Bench28", "Boulder Ridge Bench28", FRI, "10:00", "11:00", None),
    ("Bench29", "Cascade Grove Bench29", FRI, "10:15", "10:45", None),
    ("Bench30", "Drift Valley Bench30",  FRI, "10:30", "11:30", None),
    ("Bench31", "Ember Field Bench31",   FRI, "13:55", "14:05", None),
    ("Bench32", "Forest Trail Bench32",  FRI, "14:45", "15:15", None),
    ("Bench33", "Granite Harbor Manufacturing Modernization Review Bench33",
        FRI, "15:05", "17:55", None),
]

# ---------------------------------------------------------------------------
# ALL-DAY EVENTS  (rendered in the day-header band, not the time grid)
# (id, title, start_day_name, start_date, end_date_inclusive, span_days, day_names)
# ---------------------------------------------------------------------------
ALL_DAY = [
    ("Bench34", "Duration Check Bench34",
        "Monday", "2022-01-17", "2022-01-17", 1, ["Monday"]),
    ("Bench35", "Multiple Day Event Bench35",
        "Wednesday", "2022-01-19", "2022-01-20", 2, ["Wednesday", "Thursday"]),
]

# ---------------------------------------------------------------------------
# Per-event rationale  (purpose, [phenomena tags])
# ---------------------------------------------------------------------------
RATIONALE = {
    "Bench01": ("Duration-coverage anchor: smallest readable block (15 min).",
                ["duration:15", "clamped-regime", "sparse-morning"]),
    "Bench02": ("Duration coverage 20 min, still inside the clamped class.",
                ["duration:20", "clamped-regime"]),
    "Bench03": ("Duration coverage 30 min; measured at the clamp floor, so it is "
                "visually indistinguishable from 15/20 min (clamped class).",
                ["duration:30", "clamped-regime"]),
    "Bench04": ("Duration coverage 45 min.",
                ["duration:45", "linear-regime"]),
    "Bench05": ("Duration coverage 55 min.",
                ["duration:55", "linear-regime"]),
    "Bench06": ("Duration coverage 60 min, exact one-hour block.",
                ["duration:60", "linear-regime", "hour-aligned"]),
    "Bench07": ("Duration coverage 65 min; moved to 16:30 so its end (17:35) "
                "stays inside the 18:00 view boundary.",
                ["duration:65", "linear-regime", "late-afternoon"]),
    "Bench08": ("Start-offset :05 with a clean 60-min duration.",
                ["start-offset::05", "duration:60", "end::05"]),
    "Bench09": ("Start-offset :15.",
                ["start-offset::15", "duration:60"]),
    "Bench10": ("Start-offset :30.",
                ["start-offset::30", "duration:60"]),
    "Bench11": ("Start-offset :45.",
                ["start-offset::45", "duration:60"]),
    "Bench12": ("Start-offset :55 (cross-hour start at xx:55).",
                ["start-offset::55", "duration:60", "cross-hour"]),
    "Bench13": ("Start-offset :05 plus 75-min duration coverage.",
                ["start-offset::05", "duration:75", "linear-regime"]),
    "Bench14": ("Identical-start overlap (shortest of the 09:00 stack).",
                ["overlap:identical-start", "duration:30"]),
    "Bench15": ("Identical-start overlap (middle of the 09:00 stack).",
                ["overlap:identical-start", "duration:60"]),
    "Bench16": ("Identical-start overlap (longest of the 09:00 stack).",
                ["overlap:identical-start", "duration:120"]),
    "Bench17": ("Offset overlap container (120 min) spanning two shorter events.",
                ["overlap:offset", "duration:120"]),
    "Bench18": ("Offset overlap, short block nested inside the container.",
                ["overlap:offset", "duration:45"]),
    "Bench19": ("Offset overlap, 90-min block crossing the container's end.",
                ["overlap:offset", "duration:90"]),
    "Bench20": ("Recurring event Mon-Fri in a collision-free slot; drives the "
                "recurrence-recognition component.",
                ["recurrence", "duration:15", "clamped-regime"]),
    "Bench21": ("Horizontal-compression block (full 120 min).",
                ["compression", "duration:120", "overlap:offset"]),
    "Bench22": ("Horizontal-compression block (110 min), :05 start.",
                ["compression", "duration:110", "start-offset::05"]),
    "Bench23": ("Horizontal-compression block (115 min), :10 start, :05 end.",
                ["compression", "duration:115", "end::05"]),
    "Bench24": ("Back-to-back chain, slot 1.",
                ["back-to-back", "duration:30"]),
    "Bench25": ("Back-to-back chain, slot 2.",
                ["back-to-back", "duration:30"]),
    "Bench26": ("Back-to-back chain, slot 3.",
                ["back-to-back", "duration:30"]),
    "Bench27": ("Back-to-back chain, slot 4.",
                ["back-to-back", "duration:30"]),
    "Bench28": ("Dense overlap container (60 min).",
                ["overlap:offset", "dense-layout", "duration:60"]),
    "Bench29": ("Dense overlap, short nested block (30 min).",
                ["overlap:offset", "dense-layout", "duration:30"]),
    "Bench30": ("Dense overlap, 60-min block crossing the container's end.",
                ["overlap:offset", "dense-layout", "duration:60"]),
    "Bench31": ("Cross-hour boundary case, 10-min clamped block (13:55-14:05).",
                ["cross-hour", "duration:10", "clamped-regime", "end::05"]),
    "Bench32": ("Cross-hour boundary case, 30-min block (14:45-15:15).",
                ["cross-hour", "duration:30"]),
    "Bench33": ("Multi-hour duration (170 min). Long title: in a tall single "
                "block it wraps and stays fully readable (measured) -- real "
                "truncation is exercised by the compressed overlap events.",
                ["duration:170", "cross-hour", "long-title-wrap"]),
    "Bench34": ("All-day single-day event in the Monday header band; tests the "
                "all-day vs timed distinction (model must not invent a clock time).",
                ["all-day", "single-day", "day-header"]),
    "Bench35": ("All-day event spanning Wed-Thu; tests multi-day span recognition "
                "as a single event across two day columns.",
                ["all-day", "multi-day-span", "day-header"]),
}


# ---------------------------------------------------------------------------
# Derivation
# ---------------------------------------------------------------------------
def to_min(hhmm: str) -> int:
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def derive_duration(dur: int):
    if dur <= CAL["D_clamp_min"]:
        return {
            "canonical_min": dur,
            "regime": "clamped",
            "base_band_min": CAL["clamped_base_band_min"],
            "base_band_max": CAL["clamped_base_band_max"],
            "bonus_band_min": None,
            "bonus_band_max": None,
        }
    return {
        "canonical_min": dur,
        "regime": "linear",
        "base_band_min": dur - CAL["duration_base_tol_min"],
        "base_band_max": dur + CAL["duration_base_tol_min"],
        "bonus_band_min": dur - CAL["duration_bonus_tol_min"],
        "bonus_band_max": dur + CAL["duration_bonus_tol_min"],
    }


def content_words(title: str):
    return title.split()[:-1]   # drop trailing BenchXX token


def id_token(title: str):
    return title.split()[-1]


# ---------------------------------------------------------------------------
# YAML emitter (manual, for full control over readability / ordering)
# ---------------------------------------------------------------------------
def y_list(xs):
    return "[" + ", ".join(f'"{x}"' for x in xs) + "]"


from build_profiles_section import CLIENT_PROFILES, derive_timed


def emit():
    L = []
    a = L.append
    a("# =====================================================================")
    a("# Visual Calendar Comprehension Benchmark (VCCB)")
    a("# reference/ground_truth.yaml  --  SINGLE SOURCE OF TRUTH")
    a("#")
    a("# This file is consumed by the scorer and by the generators for")
    a("# benchmark-week.ics and benchmark_index.md. It MUST NOT be exposed")
    a("# to evaluated models (it lives under reference/).")
    a("#")
    a("# Terminology: 'Recoverable Truth' == 'Extractable Maximum'.")
    a("# =====================================================================")
    a("")
    a("benchmark:")
    a('  name: "Visual Calendar Comprehension Benchmark"')
    a('  abbreviation: "VCCB"')
    a('  version: "0.1.0"')
    a('  view_window: "08:00-18:00"')
    a("  week:")
    a('    monday: "2022-01-17"')
    a('    tuesday: "2022-01-18"')
    a('    wednesday: "2022-01-19"')
    a('    thursday: "2022-01-20"')
    a('    friday: "2022-01-21"')
    a("  canonical_events_count: 35")
    a("  visible_blocks:")
    a("    outlook: 39   # 32 single timed + 5 Bench20 + 2 all-day (Bench35 = one span bar)")
    a("    notes: 40     # same, but Bench35 renders as 2 per-day banners")
    a("    thunderbird: 40   # like Notes: Bench35 renders as 2 per-day banners")
    a('  clients: ["Outlook", "HCL Notes", "Thunderbird"]')
    a("  recoverable_truth_scope: per_client   # derived from client_profiles below")
    a("")
    a("# ---------------------------------------------------------------------")
    a("# Recoverable Truth is DERIVED PER CLIENT from these capability profiles")
    a("# (measured from screenshots). The scorer selects the profile for the")
    a("# client an image belongs to; benchmark_index.md shows the expanded")
    a("# per-client bands per event. Tolerances stay provisional until the")
    a("# final handheld photos are calibrated.")
    a("# ---------------------------------------------------------------------")
    a("client_profiles:")
    for cname, p in CLIENT_PROFILES.items():
        cbb = p["duration"]["clamped_base_band"]
        ri = p["recurrence_icon"]
        a(f"  {cname}:")
        a(f'    calibration_status: "{p["calibration_status"]}"')
        a(f'    px_per_min: {p["px_per_min"] if p["px_per_min"] is not None else "null"}')
        a(f'    min_label_box_px: {p["min_label_box_px"] if p["min_label_box_px"] is not None else "null"}')
        a(f"    precise_time_indicator: {str(p['precise_time_indicator']).lower()}")
        a("    duration:")
        a(f'      clamp_below_min: {p["duration"]["clamp_below_min"]}')
        a(f'      clamped_base_band: {("["+str(cbb[0])+", "+str(cbb[1])+"]") if cbb else "null"}')
        a(f'      base_tol_min: {p["duration"]["base_tol_min"]}')
        a(f'      bonus_tol_min: {p["duration"]["bonus_tol_min"]}')
        a("    start:")
        a(f'      base_tol_min: {p["start"]["base_tol_min"]}')
        a(f'      bonus_tol_min: {p["start"]["bonus_tol_min"]}')
        a(f"      clamp_displaces_start: {str(p['start']['clamp_displaces_start']).lower()}")
        a(f'    multi_day_render: {p["multi_day_render"]}')
        a(f'    recurrence_icon: {str(ri).lower() if isinstance(ri, bool) else ri}')
    a("")
    a("derivation: >")
    a("  Per client: if precise_time_indicator is false AND duration <=")
    a("  clamp_below_min, the event is 'clamped' -> duration earns base credit for")
    a("  any value in clamped_base_band and NO precision bonus; start earns base")
    a("  credit only (clamping can displace the top edge). Otherwise 'linear' ->")
    a("  duration/start base = canonical +/- base_tol_min, bonus = canonical +/-")
    a("  bonus_tol_min. Outlook's accent bar makes ALL durations linear")
    a("  (precise_time_indicator=true) -- short events stay precisely recoverable")
    a("  there; Notes/Thunderbird clamp at 30 min. Multi-day all-day events: span")
    a("  is directly recoverable where multi_day_render=span_bar (Outlook);")
    a("  per_day_banner clients (Notes) also accept the adjacent-banners answer.")
    a("")
    a("events:")

    for (eid, title, (day, date), start, end, rec) in EVENTS:
        smin, emin = to_min(start), to_min(end)
        dur = emin - smin
        cw = content_words(title)
        idt = id_token(title)
        # Long titles in dense, narrow overlap columns get cut off (id code at the
        # end is not visible); Bench33's long title sits in a wide block and wraps,
        # so it stays readable and is NOT marked truncating.
        TRUNCATING = {"Bench14", "Bench29"}
        trunc = "true" if eid in TRUNCATING else "false"
        purpose, phen = RATIONALE[eid]

        a(f"  - id: {eid}")
        a("    kind: timed")
        a("    canonical:")
        a(f'      title: "{title}"')
        if rec is None:
            a(f"      day: {day}")
            a(f"      date: {date}")
        else:
            a(f'      day: "recurring (Mon-Fri)"')
            a(f"      date: {date}    # first instance")
        a(f'      start: "{start}"')
        a(f'      end: "{end}"')
        a(f"      start_min: {smin}")
        a(f"      duration_min: {dur}")
        if rec is None:
            a("      recurrence: null")
        else:
            a("      recurrence:")
            a(f'        freq: {rec["freq"]}')
            a(f'        byday: {y_list(rec["byday"])}')
            a(f'        count: {rec["count"]}')
            a(f'        instances: {y_list(rec["instances"])}')
        a("    recoverable:")
        a("      timing: derived_per_client   # duration/start bands from client_profiles")
        a("      title:")
        a(f"        content_words: {y_list(cw)}")
        a(f'        id_token: "{idt}"')
        a(f"        truncation_expected: {trunc}")
        a("    rationale:")
        a(f'      purpose: "{purpose}"')
        a(f"      phenomena: {y_list(phen)}")
        a("")

    # ---- all-day events -------------------------------------------------
    for (eid, title, sday, sdate, edate_incl, span, daynames) in ALL_DAY:
        cw = content_words(title)
        idt = id_token(title)
        purpose, phen = RATIONALE[eid]
        a(f"  - id: {eid}")
        a("    kind: all_day")
        a("    canonical:")
        a(f'      title: "{title}"')
        a(f"      day: {sday}")
        a(f"      start_date: {sdate}")
        a(f"      end_date_inclusive: {edate_incl}")
        a(f"      span_days: {span}")
        a("      all_day: true")
        a("      recurrence: null")
        a("    recoverable:")
        a("      region: day-header        # rendered in the header band, not the time grid")
        a(f"      start_day: {sday}         # exact match required")
        a(f"      span_days: {span}              # exact match required")
        if span > 1:
            a("      span_recoverable:         # MEASURED: clients differ")
            a('        accept: ["single_multi_day_bar", "adjacent_same_title_banners"]')
            a("        note: >")
            a("          Outlook renders one bar spanning all columns (span directly")
            a("          readable); Notes renders one all-day banner per day. Both a")
            a(f"          single {span}-day event and {span} adjacent same-title all-day")
            a("          events count as fully correct.")
        a("      start: null               # all-day: no clock start time")
        a("      duration: null            # all-day: no minute duration")
        a("      title:")
        a(f"        content_words: {y_list(cw)}")
        a(f'        id_token: "{idt}"')
        a("        truncation_expected: false")
        a("    rationale:")
        a(f'      purpose: "{purpose}"')
        a(f"      phenomena: {y_list(phen)}")
        a("")

    return "\n".join(L) + "\n"


if __name__ == "__main__":
    out = emit()
    with open("reference/ground_truth.yaml", "w") as f:
        f.write(out)
    print(f"wrote reference/ground_truth.yaml ({len(out)} bytes)")
