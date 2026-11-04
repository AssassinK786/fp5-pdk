# PEX calibration for fp5A.rcx

`gen_rcx.py` regenerates `fp5A/libs.tech/klayout/pex/fp5A.rcx` — an OpenRCX
rules deck calibrated to the MOSIS T89Y 3-metal data in `tech/wire_rc.txt`.

## What it does
- Replaces the old GF180MCU structural template (wrong widths, wrong values,
  explicitly uncalibrated) with FP5A geometry: min widths 0.9/0.9/1.5 um,
  sheet R 0.09/0.09/0.05 ohm/sq.
- Writes the exact section structure OpenROAD's parser expects (verified
  against `src/rcx/src/extRCmodel.cpp` and sky130hs `rcx_patterns.rules`):
  per-metal RESOVER grid, OVER per lower context, UNDER/DIAGUNDER per upper
  context, OVERUNDER for the middle metal, `WIDTH Table 0 entries` on the top
  metal's UNDER/DIAGUNDER.
- Values are per-nanometre (fF/nm, ohm/nm) — the deck unit, not per-um.
  Isolated-wire ground C and sheet R match `wire_rc.txt` exactly; lateral
  coupling uses a `w/(w+sep)` analytic falloff (estimate).

## Deck grammar (from OpenROAD source)
- cap tables (OVER/UNDER/OVERUNDER): `sep_um  coupling  fringe  res`
- RESOVER: `dist1_um  dist2_um  0  res`  (2-D neighbour-spacing grid)
- DIAGUNDER: `sep_um  0  diag_cap  0`  (diagonal cap in the fringe slot)

## Validation
`run_librelane.sh` on cnt8 passes LVS + KLayout DRC with the generated deck
and produces a SPEF (~2.8 fF per typical signal net — sane for 0.5 um short
wires vs the GF180 deck's incorrect values).

## Limitations
Coupling magnitudes and the falloff are analytic estimates, not field-solved.
A FasterCap/reference-extractor calibration (the real open_pdks flow) is
future work. Treat SPEF coupling terms as first-order.
