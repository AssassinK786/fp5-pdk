# Changelog

## v1.1 - 2026-11-02

- Repackaged the PDK in the `open_pdks` layout: `fp5A/libs.tech` and
  `fp5A/libs.ref/fp5_osu`.
- Added LibreLane 3.x configuration, tracks, PDN settings, exclusion lists and
  a routed `cnt8` smoke design.
- Added KLayout `.lyt/.lyp/.map` technology files and an OpenRCX ruleset
  (first-order).
- Added Magic technology/startup files, Netgen setup and xschem symbols.
- Added `Makefile`, `tools/check_pdk.sh`, `tools/run_librelane.sh`,
  `LICENSE`, `NOTICE` and `SOURCES`.
- Removed hard-coded `$HOME`/`/home/fpga` paths from flow and validation
  scripts.
- Fixed `klayout/check_cells.sh` to use absolute report paths and fail on
  missing reports; added TIE cell handling.
- Added `write_gds` to the legacy OpenROAD flow.
- Added global Monte Carlo wrappers (`mc_global`), Liberty `pg_pin` blocks and
  a physical `FILL` Liberty cell.
- Added `rpoly2`/`rhr` PCells and hi-res/poly2-contact DRC checks.
- Installed only core cells + TIEHI/TIELO; PAD GDS/ESD views were removed
  from the new reference library (they were not physically complete).
- Added TAP (well/substrate), DECAP (poly-poly) and ENDCAP cells; the LibreLane
  smoke design now inserts 66 TAP, 18 ENDCAP and 301 DECAP cells.
- Verified the LibreLane flow through GDS streamout and KLayout DRC with 0
  DRC/route-DRC/antenna/power-grid violations and 0 setup/hold WNS at tt/ff/ss.
- Added an edge-ring PDN (metal1 rails + metal2/metal3 ring) and ran IR drop:
  worst-case vdd 0.882 V, gnd 0.759 V on the cnt8 example.

## v1.0 - 2026-10-23

- Initial research-complete release: five BSIM3 corners, passives, Monte
  Carlo mismatch, KLayout DRC/LVS, OSU cells, tie cells, legacy Yosys/OpenROAD
  flow and validation decks.
