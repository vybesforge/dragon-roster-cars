# dragon-roster-cars

Vybesforge Tail of the Dragon server car roster — one-click install pack.

The **binaries are a release asset** (GB-scale, so they are not tracked in git):
see the `Dragon_Roster_Cars.zip` asset on the
[dragon-roster-cars-v1.0.0 release](../../releases/tag/dragon-roster-cars-v1.0.0).
This repo holds the roster **definition** — which cars each server loads, their
download sources, and the tool that reports it from the live servers.

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

## Install

1. Download `Dragon_Roster_Cars.zip` from the release.
2. Extract into your Assetto Corsa root so the folders land under `content/cars/`.
3. Join with Content Manager — the server's checksums decide whether you match.

## Notes

- Cars are third-party mods; ADL Pro-Am and Matsuri Mayhem packs are **not**
  mirrored here — the servers link to their original download pages.
- Track updates (I-29 Speedway) are Apache-2.0 Vybes Forge work and live in
  `trackupdates_forge`.
