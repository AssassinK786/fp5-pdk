# FP5A KLayout technology

```text
tech/    fp5A.lyt, fp5A.lyp, fp5A.map, fp5A_layers.txt, fp5A_wire_rc.txt
drc/     fp5A.drc                       MOSIS SCMOS SUBM DRC
lvs/     fp5A.lvs                       MOS LVS
pex/     fp5A.rcx                       first-order OpenRCX rules
pcells/  fp5_pcells.py                  KLayout PCells
```

The decks accept `input`, `report`, and `topcell` (LibreLane) or `top`
(standalone). See `../librelane/config.tcl` for the paths used by LibreLane.
