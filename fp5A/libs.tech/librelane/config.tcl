# FP5A 0.5 um 5 V research PDK - LibreLane PDK configuration
# This file is evaluated by LibreLane before the standard-cell-library config.
# All paths are relative to PDK_ROOT/PDK so the tree can be installed anywhere.

set ::env(PROCESS) 500
set ::env(DEF_UNITS_PER_MICRON) 1000

if { ![info exists ::env(STD_CELL_LIBRARY)] } {
    set ::env(STD_CELL_LIBRARY) fp5_osu
}

# Cell power/ground pins (LEF names).
set ::env(VDD_PIN) "vdd"
set ::env(GND_PIN) "gnd"
set ::env(VDD_PIN_VOLTAGE) "5.00"
set ::env(GND_PIN_VOLTAGE) "0.00"
set ::env(SCL_POWER_PINS) "vdd"
set ::env(SCL_GROUND_PINS) "gnd"

# Timing corners.  The model cards are tt/ff/ss/fs/sf; the digital views
# currently exist for tt (5.0 V), ff (5.5 V) and ss (4.5 V) at 25 C.
set ::env(DEFAULT_CORNER) "nom_tt_5v00_25c"
set ::env(STA_CORNERS) "nom_tt_5v00_25c nom_ff_5v50_25c nom_ss_4v50_25c"
set ::env(TIMING_VIOLATION_CORNERS) "*"

# One technology LEF for all corners.
set ::env(TECH_LEFS) [dict create]
dict set ::env(TECH_LEFS) "nom_*" \
    "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/$::env(STD_CELL_LIBRARY)/lef/${::env(STD_CELL_LIBRARY)}_tech.lef"

# Floorplan / placement.
set ::env(PLACE_SITE) "core"
set ::env(FP_TRACKS_INFO) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/librelane/tracks.info"
set ::env(FP_TAPCELL_DIST) 0
set ::env(DPL_CELL_PADDING) 0
set ::env(GPL_CELL_PADDING) 0
set ::env(IO_PIN_H_LAYER) "metal3"
set ::env(IO_PIN_V_LAYER) "metal2"

# Routing layers.  The OSU cells use metal1 for internal wiring and pins;
# signals are routed on metal2/metal3 as in the original FP5 flow.
set ::env(METAL_LAYER_NAMES) "metal1 metal2 metal3"
set ::env(RT_MIN_LAYER) "metal2"
set ::env(RT_MAX_LAYER) "metal3"
set ::env(DRT_MIN_LAYER) "metal2"
set ::env(GRT_LAYER_ADJUSTMENTS) "0,0,0"

# Signoff / streamout.
set ::env(PRIMARY_GDSII_STREAMOUT_TOOL) "klayout"
set ::env(OUTPUT_CAP_LOAD) 0.05
set ::env(MAX_FANOUT_CONSTRAINT) 10
set ::env(CLOCK_UNCERTAINTY_CONSTRAINT) 0.05
set ::env(CLOCK_TRANSITION_CONSTRAINT) 0.5
set ::env(TIME_DERATING_CONSTRAINT) 0.05
set ::env(IO_DELAY_CONSTRAINT) 0.2
set ::env(DEFAULT_MAX_TRAN) 2.0

# The OSU library has no tap/endcap/decap cells yet.  Fill is available.
set ::env(FILL_CELLS) "FILL"
set ::env(DECAP_CELLS) ""

# Default PDN parameters.  The production PDN for this 3-metal PDK is the
# edge-ring config in pdn_cfg_ring.tcl (selected by tools/run_librelane.sh):
# wide metal1 rails plus a metal2/metal3 ring outside the core.  These values
# are kept for users who choose the standard strap grid instead.
set ::env(PDN_ENABLE_GLOBAL_CONNECTIONS) 1
set ::env(PDN_RAIL_WIDTH) 1.2
set ::env(PDN_RAIL_LAYER) "metal1"
set ::env(PDN_CORE_RING_VWIDTH) 1.2
set ::env(PDN_CORE_RING_HWIDTH) 1.8
set ::env(PDN_CORE_RING_VSPACING) 0.9
set ::env(PDN_CORE_RING_HSPACING) 0.9
set ::env(PDN_CORE_RING_VOFFSET) 1.2
set ::env(PDN_CORE_RING_HOFFSET) 1.5
set ::env(PDN_RAIL_OFFSET) 0
set ::env(PDN_VERTICAL_LAYER) "metal2"
set ::env(PDN_HORIZONTAL_LAYER) "metal3"
set ::env(PDN_VWIDTH) 1.2
set ::env(PDN_HWIDTH) 1.8
set ::env(PDN_VSPACING) 0.9
set ::env(PDN_HSPACING) 0.9
set ::env(PDN_VOFFSET) 1.2
set ::env(PDN_HOFFSET) 1.5
set ::env(PDN_VPITCH) 4.8
set ::env(PDN_HPITCH) 6.0

# Clock tree.
set ::env(CTS_MAX_SLEW) 1.0
set ::env(CTS_MAX_CAP) 1.2
set ::env(CTS_ROOT_BUFFER) "CLKBUF2"
set ::env(CTS_CLK_BUFFERS) "CLKBUF1 CLKBUF2 CLKBUF3"
set ::env(SYNTH_DRIVING_CELL) "BUFX4/Y"
set ::env(SYNTH_CLK_DRIVING_CELL) "CLKBUF2/Y"
set ::env(SYNTH_BUFFER_CELL) "BUFX4/A/Y"
set ::env(SYNTH_TIEHI_CELL) "TIEHI/Y"
set ::env(SYNTH_TIELO_CELL) "TIELO/Y"

# Signoff decks.  KLayout is used for streamout and DRC.  The Magic/Netgen
# files are provided for manual/analog use; the default LibreLane flow is
# configured to use KLayout only until the Magic cell views are generated.
set ::env(KLAYOUT_TECH) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/klayout/fp5A.lyt"
set ::env(KLAYOUT_PROPERTIES) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/klayout/fp5A.lyp"
set ::env(KLAYOUT_DEF_LAYER_MAP) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/klayout/fp5A.map"
set ::env(KLAYOUT_DRC_RUNSET) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/klayout/fp5A.drc"
set ::env(KLAYOUT_LVS_SCRIPT) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/klayout/fp5A.lvs"

set ::env(MAGICRC) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/magic/fp5A.magicrc"
set ::env(MAGIC_TECH) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/magic/fp5A.tech"
set ::env(MAGIC_PDK_SETUP) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/magic/fp5A.tcl"
set ::env(NETGEN_SETUP) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/netgen/fp5A_setup.tcl"

# Interconnect parasitics.  Values are the MOSIS T89Y medians in
# tech/wire_rc.txt: ohm/sq and pF/um at minimum width.
set ::env(LAYERS_RC) [dict create]
foreach layer {metal1 metal2 metal3} {
    dict set ::env(LAYERS_RC) "*" $layer res [dict get {
        metal1 0.09 metal2 0.09 metal3 0.05
    } $layer]
}
dict set ::env(LAYERS_RC) "*" metal1 cap 0.000129
dict set ::env(LAYERS_RC) "*" metal2 cap 0.000077
dict set ::env(LAYERS_RC) "*" metal3 cap 0.000064
set ::env(SIGNAL_WIRE_RC_LAYERS) "metal1 metal2 metal3"
set ::env(VIAS_R) [dict create]
dict set ::env(VIAS_R) "*" via res 1.0
dict set ::env(VIAS_R) "*" via2 res 1.0

# OpenRCX rules.  The file is a first-order 3-metal model derived from
# tech/wire_rc.txt; it is not a foundry-qualified PEX deck.
set ::env(RCX_RULESETS) [dict create]
dict set ::env(RCX_RULESETS) "nom_*" \
    "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/klayout/pex/fp5A.rcx"

# Flow gating variables (RUN_*) belong in the design config, not the PDK.
