# Helper module: client capability profiles + per-client recoverable derivation.
# Imported by author_ground_truth.py (v2) and reusable by scorer/benchmark_index.
#
# START TIME is a TOP-EDGE reading and is precisely recoverable in ALL clients
# (measured: Bench20 clamped top accurate to <1 min in Notes and Thunderbird;
# Outlook displaces the box top but the accent bar shows the true start). Hence
# start tolerances are tight (base +/-5, bonus +/-2) and clamp_displaces_start
# is False everywhere. The precise_time_indicator (Outlook accent bar) matters
# for DURATION of short events, not for start.

CLIENT_PROFILES = {
    "outlook": {
        "calibration_status": "measured (2022-01 screenshot)",
        "px_per_min": 1.0,
        "min_label_box_px": 29,
        # Left accent bar encodes TRUE start + TRUE duration at ALL durations,
        # independent of the (text-padded) label box. Measured: Bench31 10-min
        # event -> 9 px accent at the true start, while its box is padded.
        "precise_time_indicator": True,
        "duration": {"clamp_below_min": 0, "clamped_base_band": None,
                     "base_tol_min": 15, "bonus_tol_min": 5},
        "start": {"base_tol_min": 5, "bonus_tol_min": 2,
                  "clamp_displaces_start": False},
        "multi_day_render": "span_bar",          # one bar across columns
        "recurrence_icon": True,                  # native repeat glyph shown
    },
    "notes": {
        "calibration_status": "measured (2022-01 screenshot)",
        "px_per_min": 0.8,
        "min_label_box_px": 19,
        # No sub-box indicator: only the clamped label box is visible, so any
        # duration <= clamp_below_min is indistinguishable ("short class").
        "precise_time_indicator": False,
        "duration": {"clamp_below_min": 30, "clamped_base_band": [5, 30],
                     "base_tol_min": 15, "bonus_tol_min": 5},
        "start": {"base_tol_min": 5, "bonus_tol_min": 2,
                  "clamp_displaces_start": False},
        "multi_day_render": "per_day_banner",     # repeated all-day banner per day
        "recurrence_icon": False,
    },
    "thunderbird": {
        "calibration_status": "measured (2022-01 screenshot)",
        "px_per_min": 1.26,
        "min_label_box_px": 23,
        # No sub-box indicator (uniform fill). Clamp floor ~23 px ~= 20 min, so
        # <=20 min indistinguishable, but 30 min IS resolvable (36 px) -- a lower
        # clamp than Notes (which clamps up to 30 min).
        "precise_time_indicator": False,
        "duration": {"clamp_below_min": 20, "clamped_base_band": [5, 20],
                     "base_tol_min": 15, "bonus_tol_min": 5},
        "start": {"base_tol_min": 5, "bonus_tol_min": 2,
                  "clamp_displaces_start": False},
        "multi_day_render": "per_day_banner",     # measured: gap between Wed/Thu banners
        "recurrence_icon": True,                   # repeat glyph shown on Bench20
    },
}


def derive_timed(duration_min, profile):
    """Return per-client recoverable bands for a timed event."""
    dcfg, scfg = profile["duration"], profile["start"]
    clamp = dcfg["clamp_below_min"]
    clamped = clamp > 0 and duration_min <= clamp
    if clamped:
        dur = {"regime": "clamped",
               "base_band": list(dcfg["clamped_base_band"]),
               "bonus_band": None}
    else:
        dur = {"regime": "linear",
               "base_band": [duration_min - dcfg["base_tol_min"],
                             duration_min + dcfg["base_tol_min"]],
               "bonus_band": [duration_min - dcfg["bonus_tol_min"],
                              duration_min + dcfg["bonus_tol_min"]]}
    start_bonus = (None if (clamped and scfg["clamp_displaces_start"])
                   else scfg["bonus_tol_min"])
    start = {"base_tol_min": scfg["base_tol_min"], "bonus_tol_min": start_bonus}
    return dur, start


if __name__ == "__main__":
    # quick self-check
    for c in CLIENT_PROFILES:
        d, s = derive_timed(15, CLIENT_PROFILES[c])
        print(c, "15min ->", d["regime"], "dur_bonus=", d["bonus_band"],
              "start_bonus=", s["bonus_tol_min"])
