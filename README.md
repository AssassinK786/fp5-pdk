# FP5A - free 0.5 um, 5 V research PDK

FP5A is an open, research-grade PDK modelled on the AMI / onsemi C5 0.5 um
process from public data only. It is **not a foundry PDK**: designs cannot be
fabricated from it as-is. It is intended for architecture studies, paper
reproductions, teaching and "what would this be at 0.5 um" questions.

The repository is now packaged in the `open_pdks` layout and has a working
LibreLane configuration. The legacy `models/`, `passives/`, `digital/`,
`klayout/`, `validation/` and `tech/` directories are kept as the source and
reference views.

## Layout

```text
fp5A/
  libs.tech/
    librelane/            LibreLane PDK + standard-cell config, tracks
    klayout/              DRC/LVS decks, .lyt/.lyp/.map, OpenRCX rules
    magic/                Magic technology + startup
    netgen/               Netgen LVS setup
    ngspice/              BSIM3 corners, passives, Monte Carlo
    xschem/               xschemrc + device symbols
  libs.ref/
    fp5_osu/              OSU 0.5 um cells + FP5 tie cells
      gds/ lef/ lib/ spice/ verilog/ cdl/ doc/
```

## Quick start

```bash
# Local checks (models, KLayout DRC/LVS, no external PDK)
make check

# Install into a PDK root
make install PDK_ROOT=$HOME/pdks

# LibreLane smoke design (cnt8 counter)
PDK_ROOT=$HOME/pdks PDK=fp5A ./tools/run_librelane.sh \
    examples/librelane/cnt8/config.yaml
```

The LibreLane run writes the final GDS, DEF, ODB, SPEF and reports under
`examples/librelane/cnt8/runs/RUN_*/final/`. The wrapper skips only the Magic LEF antenna check; PDN, power-grid
connectivity and IR drop run in the flow.

## Verification (2026-11-02)

`make smoke` was run with LibreLane 3.0.14, KLayout 0.30.0 and OpenROAD 26Q3 on
the `cnt8` example. The run completed through GDS streamout and KLayout DRC:
0 KLayout DRC errors, 0 detailed-route DRC errors, 0 antenna violations, 0
setup/hold WNS at all three timing corners, 0 power-grid violations, and
GDS/DEF/SPEF/SDF were written to `examples/librelane/cnt8/runs/RUN_*/final/`.
IR drop was extracted with the edge-ring PDN after tap/decap insertion:
worst-case vdd drop 0.882 V (17.65 %) and gnd drop 0.759 V (15.17 %). `VSRC_LOC_FILES` is not defined, so
the IR numbers are first-order. Cell-level MOS LVS passes (NAND2X1/TIEHI and
the OSU cell logs); analog passive LVS is not yet in the deck.

## What is in the PDK

| item | contents |
|---|---|
| models | BSIM3v3.1 `fp5n`/`fp5p`, corners tt/ff/ss/fs/sf. Typical = MOSIS lot T89Y; corners = +-3 sigma of 105 C5 lots |
| passives | poly / poly2 / hi-res / n-well / n+ / p+ resistors, poly-poly cap, junction diodes, substrate PNP, experimental Schottky |
| mismatch / MC | local `fp5n_mm`/`fp5p_mm`; global `fp5n_g`/`fp5p_g` in `mc_global` |
| DRC/LVS | KLayout DRC + MOS LVS; 33 OSU core cells DRC 0 / LVS match |
| digital | 33 OSU core cells + TIEHI/TIELO + TAP/DECAP/ENDCAP; LEF, GDS, Liberty, SPICE, Verilog, CDL; tt/ff/ss timing |
| analog | KLayout PCells (nmos/pmos/rpoly/rpoly2/rhr/cpoly/gring); xschem symbols; ngspice validation |
| packaging | `open_pdks` tree, Makefile, LibreLane config, KLayout tech files, Magic/Netgen setup |
| validation | device/ring/opamp/bandgap decks in `validation/` |

## Known limits

- **Not fabricable.** No foundry rules, PCM, seal ring, pad frame, ESD or
  reliability data. Do not send this PDK to a foundry.
- PAD GDS views are intentionally not installed yet. The new reference library
  contains core, tie and physical cells only.
- PDN uses a metal1-rail + metal2/metal3 edge-ring topology to avoid vertical
  straps through the cell rows. It is a simple, first-order grid; a full
  multi-strap PDN is future work.
- Digital Liberty views exist for tt (5.0 V), ff (5.5 V) and ss (4.5 V) at
  25 C. There are no fs/sf, 3.3 V or temperature corners yet.
- No antenna-diode/SRAM/IO cells yet; TAP, DECAP and ENDCAP are present.
- OpenRCX rules are a first-order 3-metal template, not a calibrated PEX deck.
- Analog LVS is MOS-only; resistor/capacitor/diode/PNP extraction is not yet
  in the signoff deck.
- Noise, self-heating, aging and passive mismatch are not characterized.
- `check_cells.sh` and the validation scripts are local checks, not CI.
- No ciel/volare release tarball is provided; use `--manual-pdk` with the
  installed `PDK_ROOT`, as in the quick start.

## Sources and license

Public sources are listed in `SOURCES.md`. Original FP5A work is released
under the Apache License 2.0 (`LICENSE`); third-party OSU/qflow material keeps
its own license (`NOTICE`).
