# Dragon Roster Cars v1.1.0

**Complete pack — supersedes v1.0.0, which was incomplete.** In v1.0.0, 8 of the 18
cars shipped as physics-only stubs (just `data.acd`, no model, no UI, no skins), so a
fresh Content Manager install was missing roughly half the roster:

`chevrolet_corvette_c7`, `iku_mitsubishi_lancer_evo_6_gra`, `mazda_miata_spec_m`,
`prvvy_e30_widebody_4rotor_tt`, `sat_ion06`, `subaru_wrx_2022_sti_aero_400hp`,
`hk51_p1_spec_mr2`, `hk51_p1_spec_rx8`

## Fixed

- All 18 roster cars now contain their full content (2295 entries, every car with at
  least one `.kn5`).
- Adds the custom driver model `content/driver/driver_paul.kn5`.
- Pack is built by `tools/build_pack.py`, which **refuses to pack a car without a
  `.kn5`** and records file count + byte total + SHA-256 per car folder, so this
  failure mode cannot ship silently again.

## Install

1. Download `Dragon_Roster_Cars_v1.1.0.zip` and verify it against the `.sha256`.
2. Extract into your Assetto Corsa root — folders land under `content/cars/` and
   `content/driver/`.
3. Overwrite the v1.0.0 files if you already installed them.

## Notes

- Server and clients must match: the Dragon servers checksum car content, so an
  out-of-date install gets kicked on join.
- Third-party mods remain the property of their authors; this pack is a convenience
  mirror of the roster the Vybesforge servers run.
