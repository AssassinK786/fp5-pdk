# FP5A standard-cell-library configuration (LibreLane)
# The library is the OSU 0.5 um cell set (33 core cells) plus FP5 tie cells.
# PAD views are intentionally not installed yet; see the design manual.

set ::env(LIB) [dict create]
dict set ::env(LIB) "*_tt_5v00_25c" \
    "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/$::env(STD_CELL_LIBRARY)/lib/fp5_osu__tt_5v00_25c.lib"
dict set ::env(LIB) "*_ff_5v50_25c" \
    "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/$::env(STD_CELL_LIBRARY)/lib/fp5_osu__ff_5v50_25c.lib"
dict set ::env(LIB) "*_ss_4v50_25c" \
    "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/$::env(STD_CELL_LIBRARY)/lib/fp5_osu__ss_4v50_25c.lib"
dict set ::env(LIB) "*_fs_5v00_25c" \
    "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/$::env(STD_CELL_LIBRARY)/lib/fp5_osu__fs_5v00_25c.lib"
dict set ::env(LIB) "*_sf_5v00_25c" \
    "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/$::env(STD_CELL_LIBRARY)/lib/fp5_osu__sf_5v00_25c.lib"

set ::env(CELL_LEFS) \
    "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/$::env(STD_CELL_LIBRARY)/lef/$::env(STD_CELL_LIBRARY).lef"
set ::env(CELL_GDS) [glob \
    "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/$::env(STD_CELL_LIBRARY)/gds/*.gds"]
set ::env(CELL_VERILOG_MODELS) \
    "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/$::env(STD_CELL_LIBRARY)/verilog/$::env(STD_CELL_LIBRARY).v"
set ::env(CELL_SPICE_MODELS) [list \
    "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/$::env(STD_CELL_LIBRARY)/spice/fp5_osu_cells.spice" \
    "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/$::env(STD_CELL_LIBRARY)/spice/fp5_tiecells.spice" \
    "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/$::env(STD_CELL_LIBRARY)/spice/fp5_physical.spice"]
set ::env(CELL_CDLS) \
    "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/$::env(STD_CELL_LIBRARY)/cdl/$::env(STD_CELL_LIBRARY).cdl"

set ::env(SYNTH_EXCLUDED_CELL_FILE) \
    "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/librelane/$::env(STD_CELL_LIBRARY)/synth_excluded.cells"
set ::env(PNR_EXCLUDED_CELL_FILE) \
    "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/librelane/$::env(STD_CELL_LIBRARY)/pnr_excluded.cells"

# Cell-level synthesis mapping.
set ::env(SYNTH_DRIVING_CELL) "BUFX4/Y"
set ::env(SYNTH_CLK_DRIVING_CELL) "CLKBUF2/Y"
set ::env(SYNTH_BUFFER_CELL) "BUFX4/A/Y"
set ::env(SYNTH_TIEHI_CELL) "TIEHI/Y"
set ::env(SYNTH_TIELO_CELL) "TIELO/Y"
set ::env(CTS_ROOT_BUFFER) "CLKBUF2"
set ::env(CTS_CLK_BUFFERS) "CLKBUF1 CLKBUF2 CLKBUF3"

# The OSU cell set has no tap/endcap/decap views yet.
set ::env(FILL_CELLS) "FILL"
set ::env(DECAP_CELLS) "DECAP"

set ::env(PLACE_SITE) "core"
set ::env(FP_TAPCELL_DIST) 26
set ::env(CELL_PAD_EXCLUDE) ""
set ::env(WELLTAP_CELL) "TAP"
set ::env(ENDCAP_CELL) "ENDCAP"
