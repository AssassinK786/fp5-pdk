# cnt8 PDN / IR-drop notes

## VSRC model
`vsrc/vdd.loc`, `vsrc/gnd.loc` place C4-style voltage bumps on the die-edge
PDN ring (x,y in um, bump edge, volts):
- VDD: 5 bumps each on the left (x=14) and right (x=239) ring edges, 5.0 V.
- GND: 5 bumps each on the bottom (y=14) and top (y=422) ring edges, 0.0 V.

This makes `RUN_IRDROP_REPORT` a real measurement; the earlier 0.602 V worst
drop was an artifact of `VSRC_LOC_FILES` being unset (uniform-voltage guess).

## Results (edge-ring PDN, 35% util, TT)
| config | VDD worst | VDD avg | GND worst |
|---|---|---|---|
| no VSRC (old) | 0.602 V | 0.098 V | 0.565 V |
| ring, VSRC pinned | 1.47 V | 0.457 V | 1.32 V |

The honest worst-case drop is ~29% — the edge-ring feeds 60 um-pitch metal1
rails from the perimeter only, so the die-center rails starve.

## Experiments tried
- Horizontal metal3 straps over the core, w=1.8, `-extend_to_core_ring`:
  via2 (m2-m3) enclosure V2.4 at the two columns where straps cross the
  vertical ring — 4 errors, VDD worst IR 0.80 V.
- Same straps with `-extend_to_boundary`: DRC-clean but (a) straps merge each
  metal1 rail's *signal* nets into the power net — the OSU cells run
  horizontally-routed signals on the shared rail (netgen LVS: q[0]/q[4]
  absorbed into gnd), and (b) VDD straps extend to the top/bottom ring edges
  which carry GND. Fundamentally unsafe: m3 is horizontal, parallel to the
  rails, so any core-crossing m3 strap shorts signal nets to power.
- Straps w=3.0 (via2-enclosure fix): 68 errors — strap wider than rail gap
  shorts to neighbouring rails.
- Ring widths {3.0,3.0}: 64 errors — wide ring collides with core/IO ring.
- Wider m1 rails w=3.6: VDD worst drops to 1.12 V but 56 DRC + 3 LVS errors —
  the rails run through cell rows, so widening them shorts into cell metal1.
  Rail width is bounded by the row structure, not free to grow.
- **Blockage-aware vertical metal2 straps** (placed on columns free of the 8
  cell metal2-pin rects, found by scanning the placed DEF): PDN generated and
  connected cleanly, but the straps block *stdcell placement* — metal2 is a
  cell-pin layer, so cells can't sit under a spanning strap (DPL-0036). This
  is a structural limit, not a config bug.
- Denser rail pitch 30 um: breaks GND connectivity — OSU cells put VDD/GND
  pins on alternating rows at 60 um spacing, so a per-30-um rail lands on a
  row of the wrong polarity.

## Conclusion — updated after external research

The proven topology (sky130hd, GF180, Nangate45, IHP SG13G2 all use it) is
follow-pin metal1 rails + straps on the topmost layer cells don't use,
dropped onto the rails by a via stack.  For FP5A that means **vertical
metal3 straps**: OpenROAD draws a stripe perpendicular to the layer's
preferred direction, so HORIZONTAL metal3 yields vertical stripes that cross
every m1 rail once.  No OSU cell uses metal3, so nothing is blocked.

The vertical-m3-strap config (kept in `pdn_cfg_straps_experiment.tcl`):
```tcl
add_pdn_stripe -grid stdcell_grid -layer metal3 -width 1.8 -pitch 48.0 \
    -spacing 2.4 -offset 24.0 -extend_to_core_ring -snap_to_grid
add_pdn_connect -grid stdcell_grid -layers {metal1 metal3} -max_columns 3 -max_rows 3
```
Result: **LVS clean, VDD worst IR 1.47 V -> 0.98 V (avg 0.20 V)** — the right
direction, a real 33% improvement.

Remaining blocker: **8 KLayout V2.4 errors** (metal3 enclosure of via2 <
2 lambda = 0.6 um, per MOSIS SCMOS rule #15.3, verified in
`SCN3ME_SUBM.30.tech`).  Each is at a strap end where the m1->m3 via stack
meets the ring: the via2 needs 0.6 um of m3 on all sides, but the 1.8 um-wide
strap gives ~0.9 um at its sides and **0 um past its end**.  Widening the
strap to 2.4 um fixes the enclosure but then collides with routed metal3
(3 um pitch) — 80 errors.  There is no legal m3 width that both encloses the
stack and fits the routing pitch at strap ends.

This is now a *real* foundry-rule limit, not a topology error: the via array
OpenROAD generates cannot be enclosed by the only m3 width that fits.  The
fix requires either a via-stack generator that staggers the vias within the
strap width, or a 4th metal for the strap.  Kept the strap config as a
documented experiment alongside the clean baseline; to adopt it, the KLayout
deck would need a `pdn`-region waiver or the stack a staggered-cut option.
