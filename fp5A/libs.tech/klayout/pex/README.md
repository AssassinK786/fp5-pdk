# FP5A OpenRCX rules

`fp5A.rcx` is a first-order 3-metal OpenRCX ruleset. It is structurally based
on the public GF180MCU 1p3m OpenRCX template and is **not calibrated** to the
FP5A interconnect. The sheet resistances and per-unit capacitances in
`../../../tech/wire_rc.txt` are the intended targets:

| layer | Rsh (ohm/sq) | C at min width (fF/um) |
|---|---|---|
| metal1 | 0.09 | 0.129 |
| metal2 | 0.09 | 0.077 |
| metal3 | 0.05 | 0.064 |

The LibreLane flow uses this file for `OpenROAD.RCX` and produces a SPEF. Treat
the resulting parasitics as first-order only. A calibrated deck requires
field-solver or measured test structures and is outside this release.
