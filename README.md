# dragon-roster-cars

Vybesforge Tail of the Dragon server car roster — one-click install pack.

**Current pack: `Dragon_Roster_Cars_v1.1.0.zip`** (see the v1.1.0 release) — 1.56 GiB,
18 cars, all with full model/UI/skins, plus `content/driver/`. v1.0.0 is **incomplete**:
8 of the 18 cars shipped as physics-only stubs (`data.acd` only), which is why a fresh
install was missing about half the roster. Install v1.1.0.

The **binaries are a release asset** (GB-scale, so they are not tracked in git).
This repo holds the roster **definition** — which cars each server loads, what the
published pack actually contains, and the tools that report and build both.

## What the servers actually run

`ROSTERS.md` (human-readable) and `rosters.json` (machine-readable, with a
file-count/byte fingerprint per car folder) are generated from the live servers by
`tools/report_rosters.py`:

```
python tools/report_rosters.py --acserver C:\acserver --out rosters.json --md ROSTERS.md
```

Current state (regenerate rather than trusting this table — it goes stale):

| Server | Track | Layout | Cars | Pack |
|---|---|---|---|---|
| cm1 | pk_tail_of_the_dragon | 7ol | 18 | Dragon roster (this repo) |
| cm2 | pk_tail_of_the_dragon | 2way | 18 | Dragon roster (this repo) |
| cm3 | pk_tail_of_the_dragon | 5tn | 20 | ADL Pro-Am v1 (grippedupmods.com) |
| cm4 | vf_i29_speedway | main | 25 | Dragon roster (this repo) + Kunos |
| cm5 | vf_i29_speedway | short | 20 | ADL Pro-Am v1 (grippedupmods.com) |

Track downloads live in `vybesforge/trackupdates_forge` releases; the Dragon track
itself (`pk_tail_of_the_dragon` v1.2) is distributed by its original author — see
the server description in Content Manager.

## Building the pack

`PACK_CONTENTS.md` lists exactly what v1.1.0 contains (per-car file count, size and
folder SHA-256). To rebuild:

```
python tools/build_pack.py --acserver C:\acserver --server cm1 ^
    --names-file rosters/cm1-cars.txt ^
    --out Dragon_Roster_Cars_v1.1.0.zip --extra content/driver ^
    --manifest manifest.json
```

`build_pack.py` **refuses to pack a car that has no `.kn5`**, because that is exactly
how v1.0.0 shipped stubs: the server only needs `data.acd`, so a car folder can look
"present and in use" on the server while being unusable on a client. Keep that guard.

> Related pitfall: a pack extracted one level too deep leaves the real files at
> `content/cars/content/cars/<car>` while `content/cars/<car>` holds just `data.acd`.
> Check both paths before packing.

## Install

1. Download `Dragon_Roster_Cars_v1.1.0.zip` from the v1.1.0 release and verify the
   `.sha256`.
2. Extract into your Assetto Corsa root so folders land under `content/cars/` and
   `content/driver/`.
3. Join with Content Manager — the server's checksums decide whether you match.

## Notes

- Cars are third-party mods; ADL Pro-Am and Matsuri Mayhem packs are **not**
  mirrored here — the servers link to their original download pages.
- Track updates (I-29 Speedway) are Apache-2.0 Vybes Forge work and live in
  `trackupdates_forge`.
- GitHub caps release assets at 2 GiB; the full roster compresses to 1.56 GiB, so a
  single-asset pack still fits. `build_pack.py --limit-bytes` splits by car if that
  ever stops being true.
