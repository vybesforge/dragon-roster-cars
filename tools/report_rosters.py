#!/usr/bin/env python3
"""Report the live Vybesforge Assetto Corsa car/track rosters.

Reads each server's cfg/server_cfg.ini (CARS=, TRACK=, CONFIG_TRACK=) and
inventories the matching content folders, so the repo state can be compared
with what the servers actually run.

Usage:
    python tools/report_rosters.py --acserver C:\\acserver --out rosters.json
    python tools/report_rosters.py --acserver C:\\acserver --md ROSTERS.md
"""
import argparse
import json
import os
import sys

SERVERS = ("cm1", "cm2", "cm3", "cm4", "cm5")


def read_cfg(path):
    """Parse the handful of INI keys we need (server_cfg.ini is not strict INI)."""
    out = {}
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            s = line.strip()
            if not s or s.startswith(("#", ";", "[")):
                continue
            if "=" in s:
                k, v = s.split("=", 1)
                out.setdefault(k.strip().upper(), v.strip())
    return out


def folder_fingerprint(path):
    """Cheap fingerprint of a content folder: file count + total bytes."""
    n = total = 0
    for dp, _, fs in os.walk(path):
        for f in fs:
            try:
                total += os.path.getsize(os.path.join(dp, f))
                n += 1
            except OSError:
                pass
    return {"files": n, "bytes": total}


def describe(acserver, name):
    cfg = read_cfg(os.path.join(acserver, name, "cfg", "server_cfg.ini"))
    cars = [c for c in cfg.get("CARS", "").split(";") if c]
    track = cfg.get("TRACK", "")
    layout = cfg.get("CONFIG_TRACK", "")
    cars_dir = os.path.join(acserver, name, "content", "cars")
    present = set(os.listdir(cars_dir)) if os.path.isdir(cars_dir) else set()
    return {
        "server": name,
        "track": track,
        "layout": layout,
        "track_version": track_version(os.path.join(acserver, name, "content", "tracks", track)),
        "car_count": len(cars),
        "cars": cars,
        "cars_missing_from_content": [c for c in cars if c not in present],
        "car_content": {c: folder_fingerprint(os.path.join(cars_dir, c))
                        for c in cars if c in present},
    }


def track_version(track_dir):
    """Version string from the track's first ui/*/ui_track.json, if any."""
    ui = os.path.join(track_dir, "ui")
    if not os.path.isdir(ui):
        return None
    for layout in sorted(os.listdir(ui)):
        p = os.path.join(ui, layout, "ui_track.json")
        if os.path.isfile(p):
            try:
                with open(p, encoding="utf-8", errors="replace") as fh:
                    for line in fh:
                        if '"version"' in line:
                            return line.split(":", 1)[1].strip().strip(',"')
            except OSError:
                pass
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--acserver", default=r"C:\acserver")
    ap.add_argument("--out")
    ap.add_argument("--md")
    args = ap.parse_args()

    servers = [describe(args.acserver, s) for s in SERVERS
               if os.path.isdir(os.path.join(args.acserver, s))]
    if not servers:
        sys.exit(f"no cm* servers found under {args.acserver}")

    data = {"servers": servers}
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, sort_keys=True)
        print(f"wrote {args.out}")
    if args.md:
        lines = ["# Live car rosters", "",
                 "Generated from the live servers by `tools/report_rosters.py`.", ""]
        for s in servers:
            lines += [f"## {s['server']} — {s['track']} / {s['layout']} "
                      f"(track v{s['track_version']})", "",
                      f"{s['car_count']} cars:", ""]
            lines += [f"- `{c}`" for c in s["cars"]]
            if s["cars_missing_from_content"]:
                lines += ["", "MISSING CONTENT: " + ", ".join(s["cars_missing_from_content"])]
            lines.append("")
        with open(args.md, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines))
        print(f"wrote {args.md}")
    if not args.out and not args.md:
        for s in servers:
            print(f"{s['server']}: {s['track']}/{s['layout']} v{s['track_version']} "
                  f"— {s['car_count']} cars, missing {len(s['cars_missing_from_content'])}")


if __name__ == "__main__":
    main()
