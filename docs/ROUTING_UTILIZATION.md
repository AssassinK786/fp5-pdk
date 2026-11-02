# Routing utilization notes

The `cnt8` example is a small 33-cell design.  The useful proxy for routing
utilization here is **routed wirelength per core area**, together with DRC,
congestion and IR drop.  `design__instance__utilization` is 1 in every variant
because fill insertion fills the empty rows, so it is not a useful routing
metric.

## Measured sweep (same RTL, TAP/DECAP/ENDCAP + edge-ring PDN)

| `FP_CORE_UTIL` | core (um^2) | routed wire (um) | wire/core (1/um) | route DRC | power-grid | vdd/gnd worst drop (V) |
|---:|---:|---:|---:|---:|---:|---:|
| 15 % | 80,352 | 7,103 | 0.088 | 0 | 0 | 0.882 / 0.759 |
| 25 % | 48,384 | 6,564 | 0.136 | 0 | 0 | 0.639 / 0.918 |
| 30 % | 44,352 | 6,058 | 0.137 | 0 | 0 | 0.572 / 0.641 |
| **35 %** | **34,992** | **6,019** | **0.172** | **0** | **0** | **0.602 / 0.565** |
| 40 % | 32,832 | 6,961 | 0.212 | 0 | 0 | 0.673 / 0.700 |

35 % is the chosen default: it has the lowest routed wirelength, 0 route/DRC
errors, and a smaller core than the 15/25/30 % variants.  At 40 % the router
starts taking detours (wirelength rises to 6,961 um) and IR drop increases.

## Levers that matter

1. **Core utilization.**  Raising `FP_CORE_UTIL` from 15 % to 35 % cut core
   area by 56 % and routed wirelength by 15 %.  The first 25 % attempt with
   the 2.4 um TAP and 13 um tap pitch failed legalization; the 4.8 um TAP
   with a 26 um pitch passes.
2. **Tap density.**  `FP_TAPCELL_DIST` is 26 um.  It is a trade-off between
   latch-up coverage and fixed-cell fragmentation.  The 4.8 x 30 um TAP/DECAP
   cells preserve nwell/select continuity and are DRC-clean at row boundaries.
3. **Routing layers.**  `RT_MIN_LAYER=metal2` / `RT_MAX_LAYER=metal3` keep
   global routing on two layers; `DRT_MIN_LAYER=metal1` lets the detailed
   router use local metal1 for pin access.  Metal1 is otherwise occupied by
   the OSU cell internals.
4. **PDN topology.**  Vertical metal2/metal3 straps through the cell rows are
   rejected by the OpenROAD 26Q3 DPL pin-access check.  The edge-ring PDN
   (wide metal1 rails + metal2/metal3 ring outside the core) avoids that and
   still gives 0 power-grid violations.
5. **Fill/decap mix.**  `DECAP_CELLS=DECAP` and `FILL_CELLS=FILL` fill the
   remaining rows.  Decaps are useful for IR, but they do not add routing
   tracks; if the design is routing-limited, reduce the decap fill before
   increasing the core.

## Next experiments

- Try `RT_MIN_LAYER=metal1` / `RT_MAX_LAYER=metal3` on a larger design; metal1
  is likely too congested because the OSU cells use it internally.
- Add a second metal2/metal3 ring or wider ring, then re-check IR drop.
- Tune `GRT_ADJUSTMENT` and `PL_TARGET_DENSITY_PCT` only with a larger block;
  the 33-cell counter has too little logic to separate congestion from
  placement noise.
- Add a per-layer routing-utilization report from OpenROAD's global-route
  congestion report to replace the wirelength/core proxy.
