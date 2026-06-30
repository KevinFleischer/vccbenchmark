#!/usr/bin/env python3
"""
gen_ics.py  --  generate reference/benchmark-week.ics FROM ground_truth.yaml.

Portability target: Outlook + HCL Notes/Domino + Apple Calendar.

Key compatibility decisions
---------------------------
* A full VTIMEZONE for Europe/Berlin is emitted, and every timed event uses
  DTSTART/DTEND;TZID=Europe/Berlin (local wall-clock time + timezone ref).
  RFC 5545 requires valid timezone information for ALL recurrence instances;
  Domino mis-expands recurring events that rely on floating time. This is also
  exactly how Outlook/Exchange itself exports recurring appointments, so it is
  the most broadly understood form. The ICS is only ever imported by the
  benchmark author (in DE), so the fixed zone is correct and safe.
* RECURRENCE_MODE = "rrule" keeps a real RRULE on Bench20, so the calendar
  shows the native recurrence icon (a real visual cue for the benchmark).
  Switch to "expand" to emit explicit per-day instances instead (no RRULE,
  no icon) if a target client still mis-handles the rule.
* All-day events use VALUE=DATE with an EXCLUSIVE DTEND (RFC 5545); all-day
  entries are timezone-independent and carry no TZID.
"""
import yaml
from datetime import date, timedelta

GT = "reference/ground_truth.yaml"
OUT = "reference/benchmark-week.ics"
DTSTAMP = "20220101T000000Z"
TZID = "Europe/Berlin"
RECURRENCE_MODE = "rrule"          # "rrule" | "expand"

# Standard Europe/Berlin VTIMEZONE (EU DST: last Sun Mar / last Sun Oct).
VTIMEZONE = [
    "BEGIN:VTIMEZONE",
    f"TZID:{TZID}",
    "X-LIC-LOCATION:Europe/Berlin",
    "BEGIN:DAYLIGHT",
    "TZOFFSETFROM:+0100",
    "TZOFFSETTO:+0200",
    "TZNAME:CEST",
    "DTSTART:19700329T020000",
    "RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU",
    "END:DAYLIGHT",
    "BEGIN:STANDARD",
    "TZOFFSETFROM:+0200",
    "TZOFFSETTO:+0100",
    "TZNAME:CET",
    "DTSTART:19701025T030000",
    "RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU",
    "END:STANDARD",
    "END:VTIMEZONE",
]


def dt(date_iso, hhmm):
    return str(date_iso).replace("-", "") + "T" + hhmm.replace(":", "") + "00"


def date_compact(date_iso):
    return str(date_iso).replace("-", "")


def excl_end(end_date_inclusive):
    y, m, d = (int(x) for x in str(end_date_inclusive).split("-"))
    return (date(y, m, d) + timedelta(days=1)).strftime("%Y%m%d")


def fold(line):
    out, cur = [], line
    while len(cur.encode()) > 75:
        cut = 75
        while len(cur[:cut].encode()) > 75:
            cut -= 1
        out.append(cur[:cut])
        cur = " " + cur[cut:]
    out.append(cur)
    return "\r\n".join(out)


def vevent_timed(uid, title, date_iso, start, end, rrule=None):
    lines = [
        "BEGIN:VEVENT",
        f"UID:{uid}@vccb.benchmark",
        f"DTSTAMP:{DTSTAMP}",
        f"DTSTART;TZID={TZID}:{dt(date_iso, start)}",
        f"DTEND;TZID={TZID}:{dt(date_iso, end)}",
        f"SUMMARY:{title}",
        "TRANSP:OPAQUE",
    ]
    if rrule:
        byday = ",".join(rrule["byday"])
        lines.append(f"RRULE:FREQ={rrule['freq']};BYDAY={byday};COUNT={rrule['count']}")
    lines.append("END:VEVENT")
    return [fold(x) for x in lines]


def vevent_allday(uid, title, start_date, end_date_inclusive):
    return [fold(x) for x in [
        "BEGIN:VEVENT",
        f"UID:{uid}@vccb.benchmark",
        f"DTSTAMP:{DTSTAMP}",
        f"DTSTART;VALUE=DATE:{date_compact(start_date)}",
        f"DTEND;VALUE=DATE:{excl_end(end_date_inclusive)}",
        f"SUMMARY:{title}",
        "TRANSP:TRANSPARENT",
        "END:VEVENT",
    ]]


def main():
    d = yaml.safe_load(open(GT))
    cal = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//VCCB//Visual Calendar Comprehension Benchmark 0.1//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:VCCB Benchmark Week 2022-01-17",
        f"X-WR-TIMEZONE:{TZID}",
    ]
    cal += VTIMEZONE
    n_vevent = n_visible = 0
    for e in d["events"]:
        c = e["canonical"]
        if e.get("kind") == "all_day":
            cal += vevent_allday(e["id"].lower(), c["title"],
                                 c["start_date"], c["end_date_inclusive"])
            n_vevent += 1; n_visible += 1
        else:
            rec = c["recurrence"]
            if rec and RECURRENCE_MODE == "rrule":
                first = rec["instances"][0]
                cal += vevent_timed(e["id"].lower(), c["title"], first,
                                    c["start"], c["end"], rrule=rec)
                n_vevent += 1; n_visible += len(rec["instances"])
            elif rec:  # expand
                for inst in rec["instances"]:
                    cal += vevent_timed(f"{e['id'].lower()}-{date_compact(inst)}",
                                        c["title"], inst, c["start"], c["end"])
                    n_vevent += 1; n_visible += 1
            else:
                cal += vevent_timed(e["id"].lower(), c["title"],
                                    str(c["date"]), c["start"], c["end"])
                n_vevent += 1; n_visible += 1
    cal.append("END:VCALENDAR")
    with open(OUT, "w", newline="") as f:
        f.write("\r\n".join(cal) + "\r\n")
    print(f"wrote {OUT}  (mode={RECURRENCE_MODE}, {n_vevent} VEVENTs, "
          f"{n_visible} visible blocks)")


if __name__ == "__main__":
    main()
