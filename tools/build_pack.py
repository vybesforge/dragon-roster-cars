#!/usr/bin/env python3
"""Build the Dragon roster car pack zip from a live server's content folder.

Why this exists: the v1.0.0 pack was built by zipping `content/cars/<car>` while
8 of the 18 cars only held `data.acd` (their full files sat in a mis-extracted
`content/cars/content/cars/<car>`). Clients got physics-only stubs. This script
REFUSES to pack a car that has no .kn5, and records file/byte/sha256 per car so
the next pack can be diffed against the roster instead of trusted.

GitHub release assets are capped at 2 GiB, so the roster is split into parts
(`--part`), each written as its own zip; every part extracts into the AC root.

Usage:
    python tools/build_pack.py --acserver C:\\acserver --server cm1 \
        --names-file rosters/cm1-cars.txt --out Dragon_Roster_Cars_v1.1.0_part1.zip \
        --limit-bytes 2000000000 --extra content/driver
"""
import argparse
import hashlib
import json
import os
import sys
import zipfile

FIXED_DATE = (2026, 1, 1, 0, 0, 0)


def car_files(acserver, server, car):
    root = os.path.join(acserver, server, "content", "cars", car)
    if not os.path.isdir(root):
        sys.exit(f"FATAL: car folder missing: {root}")
    files = []
    for dp, _, fs in os.walk(root):
        for f in fs:
            p = os.path.join(dp, f)
            files.append((p, os.path.relpath(p, root).replace(os.sep, "/")))
    if not any(rel.lower().endswith(".kn5") for _, rel in files):
        sys.exit(f"FATAL: {car} has no .kn5 (incomplete car) - refusing to pack a stub")
    return root, sorted(files, key=lambda x: x[1])


def folder_digest(acserver, server, car):
    root = os.path.join(acserver, server, "content", "cars", car)
    h = hashlib.sha256()
    n = total = 0
    for dp, _, fs in os.walk(root):
        for f in sorted(fs):
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, root).replace(os.sep, "/")
            h.update(rel.encode())
            with open(p, "rb") as fh:
                for chunk in iter(lambda: fh.read(1 << 20), b""):
                    h.update(chunk)
            n += 1
            total += os.path.getsize(p)
    return {"files": n, "bytes": total, "sha256": h.hexdigest()}


def add_file(zf, path, arcname):
    info = zipfile.ZipInfo(arcname, FIXED_DATE)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    with open(path, "rb") as src, zf.open(info, "w") as dst:
        while True:
            chunk = src.read(1 << 20)
            if not chunk:
                break
            dst.write(chunk)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--acserver", default=r"C:\acserver")
    ap.add_argument("--server", default="cm1")
    ap.add_argument("--names-file", required=True, help="one car folder per line")
    ap.add_argument("--out", required=True)
    ap.add_argument("--limit-bytes", type=int, default=2_000_000_000,
                    help="stop adding cars once the zip passes this size")
    ap.add_argument("--extra", action="append", default=[],
                    help="extra AC-root-relative folder to include, e.g. content/driver")
    ap.add_argument("--manifest", help="write a JSON manifest of what was packed")
    args = ap.parse_args()

    with open(args.names_file, encoding="utf-8") as fh:
        cars = [ln.strip() for ln in fh if ln.strip() and not ln.startswith("#")]

    manifest = {"server": args.server, "zip": os.path.basename(args.out), "cars": {}}
    packed = []
    with zipfile.ZipFile(args.out, "w", zipfile.ZIP_DEFLATED, allowZip64=True,
                         compresslevel=1) as zf:
        for car in cars:
            root, files = car_files(args.acserver, args.server, car)
            manifest["cars"][car] = folder_digest(args.acserver, args.server, car)
            for p, rel in files:
                add_file(zf, p, f"content/cars/{car}/{rel}")
            packed.append(car)
            print(f"  + {car}: {len(files)} files "
                  f"({manifest['cars'][car]['bytes'] / 2**20:.0f} MiB)", flush=True)
            if os.path.getsize(args.out) >= args.limit_bytes:
                print(f"  reached {args.limit_bytes:,} bytes - stopping after {car}")
                break
        for extra in args.extra:
            base = os.path.join(args.acserver, args.server, *extra.split("/"))
            if not os.path.isdir(base):
                print(f"  (skipping missing extra folder {extra})")
                continue
            for dp, _, fs in os.walk(base):
                for f in sorted(fs):
                    p = os.path.join(dp, f)
                    rel = os.path.relpath(p, base).replace(os.sep, "/")
                    add_file(zf, p, f"{extra}/{rel}")
            print(f"  + {extra}/")

    manifest["packed"] = packed
    manifest["zip_bytes"] = os.path.getsize(args.out)
    if args.manifest:
        with open(args.manifest, "w", encoding="utf-8") as fh:
            json.dump(manifest, fh, indent=2, sort_keys=True)
        print(f"manifest -> {args.manifest}")
    print(f"{os.path.basename(args.out)}: {manifest['zip_bytes'] / 2**30:.2f} GiB, "
          f"{len(packed)} cars")


if __name__ == "__main__":
    main()
