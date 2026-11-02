# fp5_osu reference library

FP5A standard-cell reference library: the public OSU 0.5 um core cells plus
FP5 tie cells.

## Views

| directory | contents |
|---|---|
| `gds/` | `fp5_osu.gds` (33 core cells), `fp5_tiecells.gds` (TIEHI/TIELO), `fp5_physical.gds` (TAP/DECAP/ENDCAP) |
| `lef/` | `fp5_osu_tech.lef` (technology), `fp5_osu.lef` (38 macros) |
| `lib/` | Liberty: `fp5_osu__tt_5v00_25c.lib`, `__ff_5v50_25c.lib`, `__ss_4v50_25c.lib` |
| `spice/` | `fp5_osu_cells.spice`, `fp5_tiecells.spice`, `fp5_physical.spice` |
| `verilog/` | `fp5_osu.v` |
| `cdl/` | `fp5_osu.cdl` (SPICE/CDL view for LVS) |

## Cell list

AND2X1/2, AOI21X1, AOI22X1, BUFX2/4, CLKBUF1/2/3, DFFNEGX1, DFFPOSX1,
DFFSR, FAX1, FILL, HAX1, INVX1/2/4/8, LATCH, MUX2X1, NAND2X1, NAND3X1,
NOR2X1, NOR3X1, OAI21X1, OAI22X1, OR2X1/2, TBUFX1/2, XNOR2X1, XOR2X1,
TIEHI, TIELO, TAP, DECAP, ENDCAP.

The PAD* cells from the original OSU views are intentionally not installed in
this release; they have no GDS view and no ESD characterization.

## Corners

- `tt`: 5.0 V, 25 C (typical)
- `ff`: 5.5 V, 25 C
- `ss`: 4.5 V, 25 C

The corresponding device-model corners are `tt/ff/ss/fs/sf`; fs/sf digital
views and 3.3 V/temperature views are not yet characterized.

## Use

LibreLane reads this library through
`libs.tech/librelane/fp5_osu/config.tcl`. For standalone simulation, include
`libs.tech/ngspice/fp5.lib` and the passive library, then use the SPICE views.
