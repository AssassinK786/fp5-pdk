# FP5A edge-ring PDN for the 3-metal stack.
# The cell rails are wide metal1 stripes.  A metal2/metal3 ring outside the
# core connects all rails without putting metal2/metal3 straps through the
# cell rows (the OSU library has some metal2 pins).
source $::env(SCRIPTS_DIR)/openroad/common/io.tcl
source $::env(SCRIPTS_DIR)/openroad/common/set_global_connections.tcl
set_global_connections

set_voltage_domain -name CORE -power $::env(VDD_NET) -ground $::env(GND_NET)

define_pdn_grid \
    -name stdcell_grid \
    -starts_with POWER \
    -voltage_domain CORE \
    -pins "metal2 metal3"

# VDD rails at y = 30, 90, 150, ...; GND rails at y = 0, 60, 120, ...
add_pdn_stripe -grid stdcell_grid -layer metal1 -width 1.8 -pitch 60 -offset 30 \
    -nets $::env(VDD_NET) -extend_to_core_ring
add_pdn_stripe -grid stdcell_grid -layer metal1 -width 1.8 -pitch 60 -offset 0 \
    -nets $::env(GND_NET) -extend_to_core_ring

add_pdn_ring -grid stdcell_grid -layers {metal2 metal3} \
    -widths {1.2 1.8} -spacings {0.9 0.9} -core_offsets {1.2 1.2} \
    -extend_to_boundary


# Vertical metal3 straps across the core (HORIZONTAL layer => vertical
# stripes crossing every m1 rail), extended to the core ring.
add_pdn_stripe -grid stdcell_grid -layer metal3 -width 2.4 -pitch 48.0 \
    -spacing 2.4 -offset 24.0 -extend_to_core_ring -snap_to_grid

# m1->m3 via stack where a strap crosses a rail; m2 is the intermediate.
add_pdn_connect -grid stdcell_grid -layers {metal1 metal3} \
    -max_columns 3 -max_rows 3

add_pdn_connect -grid stdcell_grid -layers {metal1 metal2}
add_pdn_connect -grid stdcell_grid -layers {metal2 metal3}
