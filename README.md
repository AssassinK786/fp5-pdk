# FP5 - free PDK, 0.5 um, 5 V (personal / research use)
An open, research-grade PDK modelled on the AMI / onsemi C5 0.5 um process, built only from public data.
NOT a foundry PDK: designs cannot be fabricated from it as-is. For architecture studies, paper reproductions and teaching.

| dir | contents |
|---|---|
| models/fp5.lib | BSIM3 (ngspice level 8 / HSPICE 49) corners tt ff ss fs sf, devices fp5n / fp5p. Typical = MOSIS lot T89Y; corners = +-3 sigma of 105 MOSIS C5 lots. Per-corner flat cards: fp5_<corner>_cards.sp |
| passives/fp5_passives.lib | `.lib ... devices` + `.lib ... res_typ / res_low / res_high` (+-3 sigma of 105 lots): poly / poly2 / hi-res / n-well / diffusion resistors, poly-poly cap, diodes, substrate PNP (TC and PNP are estimates) |
| models/fp5_mc.lib | `.lib ... mm`: Monte Carlo mismatch wrappers fp5n_mm / fp5p_mm (A_VT 7.7 / 11.9 mV um, A_beta 1.5 % um; estimates scaled from Eisele 0.5 um) |
| klayout/fp5.lvs | LVS (33/33 OSU cells match) |
| tech/wire_rc.txt | metal / poly sheet R and capacitances (MOSIS T89Y) |
| digital/ | OSU 0.5 um cells: liberty re-characterized with FP5 models (tt 5 V; ff 5.5 V / ss 4.5 V when present), LEF with C5 wire RC, GDS, SPICE, Verilog; flow/ (Yosys synth.sh, OpenROAD pnr.tcl with CTS) |
| klayout/ | GDS layer map + DRC deck (public MOSIS SCMOS SUBM rules, lambda 0.30 um) |
| validation/ | checks vs Baker C5 card, AMI5HS silicon databook (NAND2 ~15 %), MOSIS ring data |

Sources (all public): MOSIS parametric reports (Wayback / course copies), Baker / Electric C5 card, OSU standard cells (qflow),
MOSIS SCMOS rules via qflow SCN3ME_SUBM.30 Magic tech, onsemi C5 datasheet, AMI500 databook (public), papers in the source list.
Excluded on purpose: AMI C5X design-rule manual (marked Confidential). Third-party parts keep their own licences (OSU cells /
qflow files: see the qflow project). Missing vs a foundry PDK: LVS, antenna/density rules, PCells, foundry-measured corners,
statistical/mismatch models, ESD/IO cells characterized, reliability rules.

## 2026-10-21: models recentred
models/fp5.lib: RDSW scaled x 0.268 (N) / x 0.706 (P) in every corner (models/recentre.py) so the typical card matches lot
T89Y's measured Idss (461 / 246 uA/um, W/L 15/0.6, 5 V); the original MOSIS card gave 385 / 224 in ngspice. Corners keep
+-3 sigma (IdN 427..489, IdP 215..277). Old library: models/fp5_pre_recentre.lib.
(Digital libraries re-characterized on these models 2026-10-23.)

## 2026-10-23: v1.0 (research-complete)
- Corner cards regenerated; OSU cells re-characterized tt 5.0 / ff 5.5 / ss 4.5 V (~19 % faster than the stale libs).
- New TIEHI / TIELO tie cells; synth.sh maps constants to them. LEF: unsupported TURN1-3 via rules removed.
- All 33 OSU cells DRC 0 + LVS match (KLayout 0.30.5, klayout/check_cells.sh).
- Digital flow routes end to end (examples/dr_smoke: 0 route DRC). pnr.tcl: signals metal2-3, 4 threads default, verbose route.
- fp5_schottky (EXPERIMENTAL) fitted to Butler 2005 measured data; Butler bandgap and Kerstetter op-amp reproduced (validation/).
- Design manual: docs/FP5_design_manual.md v1.0. Known limits listed in its section 8.
