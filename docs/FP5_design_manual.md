# FP5A design manual (v1.1, 2026-11-02) - free PDK, 0.5 um, 5 V

FP5A models the AMI / onsemi C5 0.5 um process from public data only. It is not
a foundry PDK and is not fabricable as-is. Use it for architecture studies,
paper reproductions, teaching and "what would this be at 0.5 um" questions.

## 1. Process summary (C5 class, MOSIS lot medians)

| item | value |
|---|---|
| drawn L min / lambda | 0.6 um / 0.30 um (MOSIS SCMOS SUBM) |
| gate oxide | 141 A (lot sigma 1.6 A) |
| VDD | 5 V nominal (3.3 V usable) |
| Vth short / long, N | 0.67 / 0.71 V (sigma 24 mV) |
| Vth short / long, P | -0.91 / -0.96 V (sigma 15 mV) |
| Idsat (W/L 15/0.6, 5 V) N / P | 456 / -245 uA/um |
| metals | 3 Al (M1 0.09, M2 0.09, M3 0.05 ohm/sq) |
| poly / poly2 / hi-res poly | 22.4 / 41 / ~1030 ohm/sq |
| poly1-poly2 cap | 0.85-0.90 fF/um^2 |

## 2. Package layout (open_pdks)

```text
fp5A/
  libs.tech/
    librelane/config.tcl, librelane/fp5_osu/config.tcl, tracks.info
    klayout/tech/fp5A.lyt, tech/fp5A.lyp, tech/fp5A.map, drc/fp5A.drc, lvs/fp5A.lvs, pex/fp5A.rcx
    magic/fp5A.tech, fp5A.magicrc, fp5A.tcl
    netgen/fp5A_setup.tcl
    ngspice/fp5.lib, fp5_mc.lib, fp5_passives.lib, fp5_<corner>_cards.sp
    xschem/xschemrc, symbols/
  libs.ref/fp5_osu/
    techlef/ gds/ lef/ lib/ spice/ verilog/ cdl/ doc/
```

The legacy `models/`, `passives/`, `digital/`, `klayout/`, `validation/` and
`tech/` directories are the source views and are kept for reference.

## 3. Layers (GDS, MOSIS SCMOS numbering)

nwell 42, active 43, pselect 44, nselect 45, poly 46, poly contact 47, active
contact 48, metal1 49, via1 50, metal2 51, via2 61, metal3 62, poly2 56,
poly2 contact 55, glass 52, hi-res 34. Labels: metal1 text 109/0; metal2
110/0; metal3 111/0.

## 4. Design rules (lambda = 0.30 um)

`libs.tech/klayout/drc/fp5A.drc` checks the public MOSIS SCMOS SUBM rules:
widths/spacings/enclosures for nwell, active, poly, select, contacts,
metal1-3, vias, poly2, glass and the hi-res implant. It also has generic
antenna checks. The deck is a subset; density, latch-up, pad/ESD and real
foundry antenna limits are not provided (no public source).

## 5. Devices and models

| device | model / cell | notes |
|---|---|---|
| NMOS / PMOS | `fp5n` / `fp5p` in `libs.tech/ngspice/fp5.lib` | BSIM3v3.1 (ngspice LEVEL 8, HSPICE 49); `.lib "fp5.lib" tt` (ff ss fs sf); give AS/AD/PS/PD |
| mismatch | `fp5n_mm` / `fp5p_mm` in `fp5_mc.lib` `mm` | A_VT 7.7 / 11.9 mV um, A_beta 1.5 % um (estimates) |
| global MC | `fp5n_g` / `fp5p_g` in `fp5_mc.lib` `mc_global` | one lot draw per run, shared by all instances |
| resistors | `rpoly`, `rpoly2`, `rhr`, `rnwell`, `rndiff`, `rpdiff` | `fp5_passives.lib devices` + `res_typ/res_low/res_high` |
| capacitor | `cpoly` (poly1-poly2) | +-57 % at 3 sigma (lot spread 19 %) |
| diodes / PNP | `dnwell`, `dnplus`, `dpplus`, `c5pnp` | PNP is an estimate |
| Schottky | `fp5_schottky` | EXPERIMENTAL, fitted to Butler 2005 data |

Corners: tt/ff/ss/fs/sf = typical and +-3 sigma of 105 MOSIS C5 lots (Vth,
Idsat, tox). Digital timing views: tt 5.0 V, ff 5.5 V, ss 4.5 V at 25 C.

## 6. Layout cells and PCells

- KLayout PCells (`libs.tech/klayout/pcells/fp5_pcells.py`): nmos, pmos
  (W/L/fingers/tap), rpoly, rpoly2, rhr, cpoly, gring. The poly2/hi-res cells
  use the poly2/p2con and hires layers.
- Standard cells: 33 OSU core cells + TIEHI/TIELO + TAP/DECAP/ENDCAP. All
  core cells DRC 0 and LVS match. PAD cells are intentionally not installed.
- Tie cells are INVX1-derived; `synth.sh` maps constants to them.

## 7. Flows

- Analog: ngspice. `.lib "$PDK_ROOT/fp5A/libs.tech/ngspice/fp5.lib" tt`, then
  `.lib ".../fp5_passives.lib" devices` and `res_typ`.
- Digital (LibreLane 3.x):
  ```bash
  make install PDK_ROOT=$HOME/pdks
  PDK_ROOT=$HOME/pdks PDK=fp5A ./tools/run_librelane.sh \
      examples/librelane/cnt8/config.yaml
  ```
  The wrapper runs KLayout streamout/DRC, PDN/IR drop and skips only the Magic
  LEF antenna check. `examples/librelane/cnt8` is a routed 8-bit counter; final
  GDS/DEF/ODB/SPEF are in `runs/RUN_*/final/`. The default `FP_CORE_UTIL` is
  35 % with `FP_TAPCELL_DIST` 26 um; TAP/DECAP/ENDCAP are inserted automatically.
- Legacy digital: `digital/flow/synth.sh` + `digital/flow/pnr.tcl` (Yosys /
  OpenROAD). `pnr.tcl` now writes a GDS as well as DEF/ODB.
- DRC: `klayout -b -r libs.tech/klayout/drc/fp5A.drc -rd input=x.gds -rd report=x.lyrdb`.
- LVS: `klayout -b -r libs.tech/klayout/lvs/fp5A.lvs -rd input=x.gds -rd schematic=x.sp -rd top=CELL`.

## 8. Validation

Device VGS/gm within 10 % of the Baker C5 card; OSU NAND2 FO1 within ~15 % of
the AMI5HS silicon databook; ring oscillators ~2.4x faster than MOSIS measured
(unpublished ring layout parasitics); Kerstetter op-amp reproduced at tt/ff/ss;
Butler 2005 Schottky bandgap reproduced. See `validation/README.md`.

## 9. Known gaps vs a foundry PDK

- Not fabricable: no mask data, PCM, seal ring, pad opening, ESD/latch-up,
  density, reliability or yield rules.
- PAD GDS/ESD cells are not installed. No antenna-diode, SRAM/ROM,
  scan/clock-gating/level-shifter cells; TAP/DECAP/ENDCAP are present.
- PDN uses a metal1-rail + metal2/metal3 edge-ring topology with VSRC bumps
  pinned on the die-edge ring (`cnt8/vsrc/`). With sources pinned, worst-case
  VDD IR drop is ~1.47 V (29%) at 35% util — the ring starves 60 um-pitch
  rails. Vertical metal3 straps (the proven sky130/gf180 pattern — metal3 is
  HORIZONTAL so stripes run vertically over the rails, and no OSU cell uses
  m3) cut it to ~0.98 V LVS-clean, but the m1->m3 via stacks at strap ends
  violate KLayout V2.4 (m3 enclosure of via2 = 2 lambda): the only m3 width
  that fits the 3 um routing pitch can't enclose the stack. See
  `cnt8/PDN_NOTES.md` + `pdn_cfg_straps_experiment.tcl`.
- Digital Liberty views: tt/ff/ss fully characterized at 25 C, plus fs/sf at
  5 V derived by `digital/char_corners.py` (uniform delay/power derate from a
  measured INVX1 FO1 ratio — corner-consistent magnitude, not per-cell
  rechar). No 3.3 V or temperature corners yet.
- OpenRCX rules are calibrated to `tech/wire_rc.txt` (MOSIS T89Y) — sheet R
  and isolated-wire C match exactly; lateral coupling uses a w/(w+sep)
  analytic model. Regenerate with `validation/pex/gen_rcx.py`.
- Analog LVS is MOS-only; passives/diodes/PNP extraction is not yet in the
  signoff deck.
- Noise, self-heating, aging and passive mismatch are not characterized.
- Magic cell views (`.mag`) are not generated; Magic technology and Netgen
  setup are provided for manual/extraction use.
