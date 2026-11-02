# cnt8 LibreLane smoke design

8-bit synchronous counter using the FP5A `fp5_osu` library.

```bash
PDK_ROOT=/path/to/pdk-root PDK=fp5A ../../tools/run_librelane.sh config.yaml
```

From the repository root:

```bash
make smoke
```

The wrapper adds `--skip Odb.CheckDesignAntennaProperties` (no Magic cell
views). PDN, power-grid connectivity and IR drop run in the flow.

A successful run produces:

- `final/gds/cnt8.gds`, `final/def/cnt8.def`, `final/odb/cnt8.odb`
- `final/spef/nom/cnt8.nom.spef`
- `final/sdf/<corner>/cnt8*.sdf`
- `final/render/cnt8.png`
- `final/metrics.json` (KLayout DRC, timing, power, IR drop, wire length)

The 2026-11-02 verification run had 0 KLayout DRC errors, 0 detailed-route DRC
errors, 0 antenna violations, 0 setup/hold WNS at tt/ff/ss and 0 power-grid
violations after TAP/DECAP/ENDCAP insertion. Worst-case IR drop: vdd 0.602 V,
gnd 0.565 V.
