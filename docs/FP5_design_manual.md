# FP5 design manual (v1.0, 2026-10-23) - free PDK, 0.5 um, 5 V (PERSONAL USE, not a foundry PDK)
FP5 models the AMI / onsemi C5 0.5 um process from public data only. It is not fabricable as-is. Use it for architecture studies,
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

## 2. Layers (GDS, MOSIS SCMOS numbering) - klayout/layers.txt
nwell 42, active 43, pselect 44, nselect 45, poly 46, poly contact 47, active contact 48, metal1 49, via1 50, metal2 51,
via2 61, metal3 62, poly2 56, poly2 contact 55, glass 52, hi-res 34. Labels: metal1 text 109/0.

## 3. Design rules (lambda = 0.30 um) - klayout/fp5.drc
| rule | value | rule | value |
|---|---|---|---|
| W.1 nwell width | 12 | W.2 nwell space | 6 |
| W.3/W.4 n+ to nwell / nwell enclosure of p+ | 6 / 6 | A.1/A.2 active width / space | 3 / 3 |
| P.1/P.2 poly width / space | 2 / 3 | P.4 field poly to active | 1 |
| P.5 S/D extension past gate | 3 | P.6 gate end cap | 2 |
| S.2 select enclosure of active | 2 | C.1/C.2 contact size / space | 2 / 3 |
| C.3/C.4/C.9 enclosure by active / poly / metal1 | 1 | C.7 poly contact to active | 2 |
| C.8 active contact to gate | 2 | M1.1/M1.2 metal1 width / space | 3 / 3 |
| V1.1-V1.4 via1 2, space 3, enclosed 1 by M1 and M2 | | M2.1/M2.2 | 3 / 3 |
| V2.1-V2.4 via2 2, space 3, M2 1, M3 2 | | M3.1/M3.2 | 5 / 3 |
| E.1/E.2 poly2 width / space | 5 / 3 | G.1 glass opening | 10 |
| ANT.1-3 antenna ratio (GENERIC) | 400 | | |
Not provided: density, latch-up tap spacing, pad / ESD rules (no public source; the AMI C5X manual is confidential and unused).

## 4. Devices and models
| device | model / cell | notes |
|---|---|---|
| NMOS / PMOS | fp5n / fp5p in models/fp5.lib, `.lib "fp5.lib" tt` (ff ss fs sf) | BSIM3v3.1 (ngspice LEVEL 8, HSPICE 49); give AS/AD/PS/PD |
| mismatch | fp5n_mm / fp5p_mm in models/fp5_mc.lib `mm` | A_VT 7.7 / 11.9 mV um, A_beta 1.5 % um (estimates) |
| resistors | rpoly, rpoly2, rhr, rnwell, rndiff, rpdiff | passives/fp5_passives.lib `devices` + `res_typ / res_low / res_high` |
| capacitor | cpoly (poly1-poly2) | +-57 % at 3 sigma (lot spread 19 %) |
| diodes, substrate PNP | dnwell, dnplus, dpplus, c5pnp | PNP is an estimate |
| Schottky (EXPERIMENTAL) | fp5_schottky (metal1 on n-well, 0.25 um2 unit; area factor = contacts) | fit to Butler 2005 measured MOSIS 0.5 um data: n 1.07, Rs 2.58 k, -0.56 mV/C; not an SCMOS device |
Corners: tt / ff / ss / fs / sf = typical and +-3 sigma of 105 MOSIS C5 lots (Vth, Idsat, tox). Timing libraries: ff 5.5 V,
tt 5.0 V, ss 4.5 V.

## 5. Layout cells
- PCells (klayout/pcells/fp5_pcells.py, library "FP5"): nmos, pmos (W, L, fingers, tap), rpoly, cpoly, gring. DRC clean; LVS extracts the
  drawn W/L/fingers. Body taps (tap=True default) and gring guard ring (p+ or n+ in n-well) included. TODO: poly2 and hi-res resistor PCells.
- Standard cells: OSU 0.5 um (digital/gds, lef, lib, spice, verilog); all 33 cells DRC 0 + LVS match with KLayout 0.30.5
  (klayout/check_cells.sh). Liberty re-characterized 2026-10-23 on the recentred models (tt/ff/ss); TBUFX1/X2 timing scaled from OSU.
- Tie cells TIEHI / TIELO (digital/tiecells: GDS, SPICE; also in LEF/lib/verilog): INVX1 with the gate strapped to a rail in
  metal1, DRC 0 / LVS match. synth.sh maps constants to them (setundef -zero + hilomap).

## 6. Flows
- Analog: ngspice with `.lib` lines above.
- Digital: `digital/flow/synth.sh TOP outdir rtl.v` then `TOP=.. NET=outdir/TOP.v OUT=outdir openroad -no_init -exit
  digital/flow/pnr.tcl` (floorplan, place, CTS, repair, global + detailed route; signals on metal2-3, metal1 for pins;
  THREADS env, default 4; NO_DR=1 skips detailed route). Source digital/flow/env.sh first. Regression: examples/dr_smoke (8-bit
  counter, routed, 0 route DRC, 15 s); examples/avr_regress (AVR core, placed timing 22.6 ns at 30 ns; detailed route optional, 30+ min).
- DRC: `klayout -b -r klayout/fp5.drc -rd input=x.gds -rd report=x.lyrdb`; LVS: `klayout -b -r klayout/fp5.lvs -rd input=x.gds
  -rd schematic=x.sp -rd top=CELL`.

## 7. Validation (validation/README.md)
Device VGS / gm within 10 % of the Baker C5 card; OSU NAND2 FO1 within ~15 % of the AMI5HS silicon databook (82 ps); ring
oscillators ~2.4x faster than MOSIS measured (unpublished ring layout parasitics, same for every lot); Kerstetter rail-to-rail op-amp
reproduced at tt/ff/ss; Butler 2005 Schottky bandgap reproduced (supply current 24.2 vs 23.75 uA, trim resistor 54.0 vs 54.8 kohm;
TC bracket -860..+1230 ppm/C contains the measured -107..+500 ppm/C).

## 8. Known gaps vs a foundry PDK
Measured foundry corners and statistical models (corners are +-3 sigma of MOSIS lot data; mismatch is an estimate);
density / ESD / latch-up / reliability rules; antenna limits are GENERIC (MOSIS publishes none); parasitic extraction deck
(OpenRCX tech); I/O pad cells characterized; noise models; resistor TCs and substrate PNP are estimates; Schottky is experimental;
no poly2 / hi-res resistor PCells.
